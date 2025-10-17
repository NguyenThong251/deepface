from typing import Any, Dict
import numpy as np

from src.services.sql import SQLService
from src.services.redis import RedisService

class RegisterController:
    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()
    
    def register_user(self, data: Dict[str, Any]):
        try:
            user_id = data.get("user_id")
            if not user_id: return {'success': False,"error": {'message':"VALIDATION_FAILED"}}

            if self.sql_service.face_user_exists(user_id): 
                return {'success': False,"error": {'message':"FACE_USER_EXISTS"}}

            image_face = self.redis_service.get_temp_image(user_id)
            if image_face is None: return {'success': False,"error": {'message':"FACE_NOT_FOUND"}}

            res_sql = self.sql_service.create_face_info(user_id , image_face)
            if res_sql is False: return {'success': False,"error": {'message':"SAVE_SQL_FAILED"}}
            
            self.redis_service.delete_temp_image(user_id)

            return {'success': True, 'result': {'message': 'OK'}}
            
        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM_ERROR'}}
