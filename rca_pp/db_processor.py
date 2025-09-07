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
        """Actual database extraction logic"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            db_data = {
                'db_path': str(db_path),
                'tables': {},
                'total_tables': len(tables)
            }
            
            for table in tables:
                try:
                    cursor.execute(f"PRAGMA table_info([{table}])")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                    row_count = cursor.fetchone()[0]
                    
                    sample_data = []
                    if row_count > 0:
                        cursor.execute(f"SELECT * FROM [{table}] LIMIT 5")
                        sample_data = cursor.fetchall()
                    
                    cursor.execute(f"PRAGMA index_list([{table}])")
                    indexes = [idx[1] for idx in cursor.fetchall()]
                    
                    db_data['tables'][table] = {
                        'columns': columns,
                        'row_count': row_count,
                        'indexes': indexes,
                        'sample_data_count': len(sample_data),
                        'sample_data': sample_data if row_count <= 100 else []
                    }
                except Exception as e:
                    logger.error(f"Error processing table {table}: {e}")
                    db_data['tables'][table] = {'error': str(e)}
            return db_data
        finally:
            conn.close()