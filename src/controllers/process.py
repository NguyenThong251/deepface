from typing import Any, Dict
import numpy as np
from flask import jsonify

from src.services.detect_face import DetectFaceService
from src.services.anti_spoof import AntiSpoofService
from src.services.redis import RedisService
from src.services.sql import SQLService
from src.utils.imgbase64 import decode_base64_image
from src.utils.imgcheck import image_check

class ProcessController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.anti_spoof_service = AntiSpoofService()
        self.redis_service = RedisService()
        self.sql_service = SQLService()
    
    def process_image(self, data: Dict[str, Any]):
        try:

            employee_id = data.get("employee_id")
            image_frame = data.get("image")

            if not all((employee_id, image_frame)): return {'success': False,"error": {'message':"VALIDATION FAILED"}}
            if self.sql_service.face_user_exists(employee_id): 
                return {'success': False,"error": {'message':"FACE USER EXISTS"}}

            image = decode_base64_image(image_frame)
            image_check(image, self.anti_spoof_service, self.face_detect_service)

            res = self.redis_service.create_temp_image(employee_id, image_frame)
            if not res: return {'success': False,"error": {'message':"SAVE REDIS FAILED"}}

            return {'success': True, 'result': {'message': 'OK'}}
            
        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM ERROR'}}
