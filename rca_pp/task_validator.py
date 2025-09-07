"""
Task-Specific Validation System
"""
import logging
from .models import TaskResult

logger = logging.getLogger(__name__)

class TaskValidator:
    VALIDATORS = {
        "shopping": "validate_shopping_task",
        "login": "validate_login_task",
        "form_submission": "validate_form_submission"
    }
    
    @staticmethod
    def validate_shopping_task(task_result: TaskResult) -> bool:
        """Validate shopping task success criteria"""
        for content in task_result.reasoning_files.values():
            content_lower = content.lower()
            if "order confirmed" in content_lower or "purchase successful" in content_lower:
                return True
            if "successfully added to cart" in content_lower and "payment processed" in content_lower:
                return True
        
        for html_data in task_result.html_files:
            content = html_data.get('content', '').lower()
            if "thank you for your order" in content:
                return True
            if "order-confirmation" in content:
                return True
        
        for db_path, db_data in task_result.db_data.items():
            if 'orders' in db_data.get('tables', {}):
                orders = db_data['tables']['orders']
                if orders.get('row_count', 0) > 0:
                    return True
            if 'cart' in db_data.get('tables', {}):
                cart = db_data['tables']['cart']
                if cart.get('row_count', 0) >= 2:
                    return True
        
        return False

    @staticmethod
    def validate_task(task_result: TaskResult) -> bool:
        """Main validation entry point"""
        validator_name = TaskValidator.VALIDATORS.get(task_result.task_type)
        if validator_name:
            validator = getattr(TaskValidator, validator_name, None)
            if validator:
                logger.info(f"Running {validator_name} validation for {task_result.task_id}")
                return validator(task_result)
        
        return any(
            "success" in content.lower() and "failed" not in content.lower()
            for content in task_result.reasoning_files.values()
        )