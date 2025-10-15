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
            employee_id = data.get("employee_id")
            if not employee_id: return {'success': False,"error": {'message':"VALIDATION FAILED"}}

            image_face = self.redis_service.get_temp_image(employee_id)
            if image_face is None: return {'success': False,"error": {'message':"FACE NOT FOUND"}}
            
            res = self.sql_service.create_face_info(employee_id , image_face)
            if res is None: return {'success': False,"error": {'message':"SAVE SQL FAILED"}}

            return {'success': True, 'result': {'message': 'OK'}}
            
        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM ERROR'}}
