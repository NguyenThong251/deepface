from typing import Any, Dict

from src.services.detect_face import DetectFaceService
from src.services.redis import RedisService
from src.services.sql import SQLService
from src.utils.imgbase64 import decode_base64_image

class ProcessController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.redis_service = RedisService()
        self.sql_service = SQLService()
    
    def process_image(self, data: Dict[str, Any]):
        try:

            user_id = data.get("userId")
            image_frame = data.get("frame")

            if not all((user_id, image_frame)): 
                return {'success': False,"error": {
                    'code':"VALIDATION_FAILED",
                    'message':"User required" if not user_id else "Image required"}}

            if self.sql_service.get_face_info(user_id): 
                return {'success': False,
                        "error": {'code':"ALREADY_REGISTERED",
                        'message':"User has registered face"}}

            image = decode_base64_image(image_frame)

            res_detect = self.face_detect_service.detect_face(image, anti_spoof_service=True)
            if isinstance(res_detect, dict) and res_detect.get('success') is False:
                return res_detect

            res_redis = self.redis_service.create_temp_image(user_id, image_frame)
            if not res_redis: 
                return {'success': False,
                    "error": {'code':"SAVE_FAILED", 
                    'message':"Failed to save Redis"}}

            return {'success': True, 
                    'result': {'code': 'OK','message': True}} 

        except Exception as e:
            return {'success': False,"error": {'message': {str(e)}}}
