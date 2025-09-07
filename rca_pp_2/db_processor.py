"""
Database Processing Utilities
"""
import sqlite3
import time
import logging

logger = logging.getLogger(__name__)

class DatabaseProcessor:
    MAX_RETRIES = 3
    RETRY_DELAY = 1

    @staticmethod
    def extract_db_data(db_path: str) -> dict[str, any]:
        """Robust database extraction with retries"""
        for attempt in range(DatabaseProcessor.MAX_RETRIES):
            try:
                return DatabaseProcessor._extract_data(db_path)
            except sqlite3.OperationalError as e:
                if "locked" in str(e) and attempt < DatabaseProcessor.MAX_RETRIES - 1:
                    logger.warning(f"Database locked, retrying ({attempt+1}/{DatabaseProcessor.MAX_RETRIES})")
                    time.sleep(DatabaseProcessor.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"Database error after {attempt+1} attempts: {e}")
                    return {'db_path': str(db_path), 'error': str(e)}
            except Exception as e:
                logger.exception(f"Critical database error: {e}")
                return {'db_path': str(db_path), 'error': str(e)}
        return {'db_path': str(db_path), 'error': "Max retries exceeded"}

    @staticmethod
    def _extract_data(db_path: str) -> dict[str, any]:
        """Actual database extraction logic with FULL row extraction for small tables"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            db_data = {
                'db_path': str(db_path),
                'tables': {},
                'total_tables': len(tables),
                'potential_issues': []  # Initialize issues list
            }
            
            for table in tables:
                try:
                    cursor.execute(f"PRAGMA table_info([{table}])")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                    row_count = cursor.fetchone()[0]
                    
                    # Fetch ALL rows for small tables
                    sample_data = []
                    if 0 < row_count <= 100:
                        cursor.execute(f"SELECT * FROM [{table}]")
                        sample_data = cursor.fetchall()
                    
                    cursor.execute(f"PRAGMA index_list([{table}])")
                    indexes = [idx[1] for idx in cursor.fetchall()]
                    
                    table_data = {
                        'columns': columns,
                        'row_count': row_count,
                        'indexes': indexes,
                        'sample_data_count': len(sample_data),
                        'sample_data': sample_data
                    }
                    
                    # Detect potential issues
                    if row_count == 0:
                        db_data['potential_issues'].append(f"Empty table: {table}")
                    if not indexes:
                        db_data['potential_issues'].append(f"No indexes on table: {table}")
                    
                    db_data['tables'][table] = table_data
                    
                except Exception as e:
                    logger.error(f"Error processing table {table}: {e}")
                    db_data['tables'][table] = {'error': str(e)}
                    db_data['potential_issues'].append(f"Table error: {table} - {str(e)}")
                    
            # Detect overall database issues
            if not tables:
                db_data['potential_issues'].append("No tables found in database")
                
            return db_data
        finally:
            conn.close()