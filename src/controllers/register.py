from typing import Any, Dict
import numpy as np
from flask import jsonify

from src.services.sql import SQLService
from src.services.redis import RedisService

class RegisterController:
    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()
    
    def register_user(self, data: Dict[str, Any]):
        try:
            employee_id = data.get("employee_id")
            if not employee_id: return jsonify({"error":{"code":"VALIDATION FAILED"}}), 200

            image_face = self.redis_service.get_temp_image(employee_id)
            
            if image_face is None: return jsonify({"error":{"code":"FACE NOT FOUND"}}), 200
            # problem here
            self.sql_service.create_face_info(employee_id , image_face)

            return jsonify({"success": "OK"}), 200
            
        except Exception as e:
            return {'error': {'code': 'SYSTEM ERROR'}}, 500
