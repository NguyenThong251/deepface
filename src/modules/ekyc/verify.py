from typing import Any, Dict

from src.services.detect_face import DetectFaceService
from src.services.facial_recognition import FacialRecognitionService
from src.services.sql import SQLService
from src.utils.imgbase64 import decode_base64_image
from src.utils.face_crop import face_crop

from src.services.redis import RedisService

class VerifyController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.facial_recognition_service = FacialRecognitionService()
        self.redis_service = RedisService()
        self.sql_service = SQLService()
    def verify_user(self, data: Dict[str, Any]):
        try:
            user_id = data.get("userId")
            image_frame = data.get("frame")
            device = data.get("device")
            if not all((user_id, image_frame)): 
                return {'success': False,"error": {
                    'code':"VALIDATION_FAILED",
                    'message':"User required" if not user_id else "Image required"}}

            image = decode_base64_image(image_frame)
            faces = self.face_detect_service.detect_face(image, anti_spoof_service=True)
            image_face1 = face_crop(image, faces)


            source = None 
            image_face2 = self.redis_service.get_embeddings(user_id)
            if image_face2 is None:
                image_face2 = self.sql_service.get_face_info(user_id)
                if image_face2 is None:
                    return {'success': False,
                            "error": {'code':"NOT_REGISTERED",
                            'message':"Face not registered"}}
                else:
                    source = "my_db"
                    self.redis_service.save_embeddings(user_id, image_face2)

            verify_result = self.facial_recognition_service.verify(
                img1_path=image_face1,
                img2_path=image_face2,
                device=device,
            )
        

            message = 'Authentication successful' if verify_result else 'Facial authentication failed'
            code = 'OK' if verify_result else 'FAILED'
            result_data = {'code': code,'message': message}
            if source:
                result_data['source'] = source
            return {'success': verify_result,'result': result_data}
                
        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}
