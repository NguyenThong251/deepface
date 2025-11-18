from typing import Any, Dict
import numpy as np

from src.services.sql import SQLService
from src.services.redis import RedisService

class UserExistController:
    def __init__(self):
        self.sql_service = SQLService()
    
    def user_exist(self, data: Dict[str, Any]):
        try:
            user_id = data.get("userId")
            if not user_id: return {'success': False,"error": {'code':"VALIDATION_FAILED", 'message':"User required"}}

            if self.sql_service.get_face_info(user_id): return {'success': True, 'result': {'code': 'OK', 'message': True}}

            return {'success': False, 'error': {'code': 'USER_NOT_EXIST',
                'message': 'User not exist'}}
            
        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}



    def delete_face_info(self, user_id) -> bool:
        try:
            user_id = data.get("userId")
            if not user_id: return {'success': False,"error": {'code':"VALIDATION_FAILED", 'message':"User required"}}

            if not self.sql_service.delete_face_info(user_id):
                return {'success': False,"error": {'code': 'DELETE_FAILED',
                    'message': 'Failed to delete face info'}}
            return {'success': True, 'result': {'code': 'OK',
                'message': 'Face info deleted'}}
        except Exception as e:
            return False