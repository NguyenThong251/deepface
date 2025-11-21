# src\modules\ekyc\userexist.py
from typing import Any, Dict

from src.services.sql import SQLService
from src.services.redis import RedisService
from src.utils.permissions import is_user_admin


class UserExistController:
    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()
    
    def check_permission(self, data: Dict[str, Any]):
        user_role = data.get("user_role") 
        if not user_role:
            return {'success': False,"error": {'code': 'PERMISSION_DENIED',
                'message': 'User role required'}}

        module_info = self.redis_service.get_module_info(user_role, "Timekeeping")
        if not module_info:
            return {'success': False,"error": {'code': 'MODULE_NOT_FOUND',
                'message': 'Module not found'}}

        if not is_user_admin(module_info):
            return {'success': False,"error": {'code': 'PERMISSION_DENIED',
                'message': 'Permission denied'}}

        return None 
    
    def user_exist(self, data: Dict[str, Any]):
        try:
            user_id = data.get("userId")
            if not user_id: return {'success': False,"error": {'code':"VALIDATION_FAILED", 'message':"User required"}}

            face_info = self.sql_service.get_face_info(user_id)
            if face_info is not None: 
                return {'success': True, 'result': {'code': 'OK', 'message': True}}

            return {'success': False, 'error': {'code': 'USER_NOT_EXIST',
                'message': 'User not exist'}}
            
        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}


# update permission và check user exist
    def delete_face_info(self, data: Dict[str, Any]):
        try:
            permission_error = self.check_permission(data)
            if permission_error:
                return permission_error 
            user_id = data.get("userId")
            if not user_id: return {'success': False,"error": {'code':"VALIDATION_FAILED", 'message':"User required"}}

            face_info = self.sql_service.get_face_info(user_id)
            if face_info is None:
                return {'success': False,"error": {'code': 'USER_NOT_EXIST',
                    'message': 'User not exist'}}

            if not self.sql_service.delete_face_info(user_id):
                return {'success': False,"error": {'code': 'DELETE_FAILED',
                    'message': 'Failed to delete face info'}}
            self.redis_service.delete_embeddings(user_id)
            self.redis_service.delete_user_info(user_id)
            return {'success': True, 'result': {'code': 'OK',
                'message': 'Face info deleted'}}
        except Exception as e:
            return {'success': False, "error": {'message': str(e)}}
#####