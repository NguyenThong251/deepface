from typing import Any, Dict
from src.services.detect_face import DetectFaceService
from src.services.redis import RedisService
from src.services.sql import SQLService
from src.utils.imgbase64 import decode_base64_image
from src.utils.face_crop import face_crop

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

            face_info =  self.sql_service.get_face_info(user_id)
            if face_info is not None:
                return {'success': False,
                        "error": {'code':"ALREADY_REGISTERED",
                        'message':"User has registered face"}}

            image_base64 = decode_base64_image(image_frame)

            faces = self.face_detect_service.detect_face(image_base64, anti_spoof_service=True)
            image_face = face_crop(image_base64, faces)
            res_occlusion = self.face_detect_service.detect_face_occlusion(image_face)
            if isinstance(res_occlusion, dict) and res_occlusion.get('success') is False:
                return res_occlusion

            res_redis = self.redis_service.save_temp_embeddings(user_id, image_face)
            if not res_redis: 
                return {'success': False,
                    "error": {'code':"SAVE_FAILED", 
                    'message':"Failed to save Redis"}}

            return {'success': True, 
                    'result': {'code': 'OK','message': True}} 

        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}
