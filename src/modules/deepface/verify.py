from typing import Any, Dict

from src.services.detect_face import DetectFaceService
from src.services.facial_recognition import FacialRecognitionService
from src.services.sql import SQLService
from src.utils.imgbase64 import decode_base64_image

class VerifyController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.facial_recognition_service = FacialRecognitionService()
        self.sql_service = SQLService()
    def verify_user(self, data: Dict[str, Any]):
        try:
            user_id = data.get("user_id")
            image_frame = data.get("image")

            if not all((user_id, image_frame)): 
                return {'success': False,"error": {
                    'code':"VALIDATION_FAILED",
                    'message':"User required" if not user_id else "Image required"}}

            image_face_info = self.sql_service.get_face_info(user_id)
            if not image_face_info: 
                return {'success': False,
                        "error": {'code':"NOT_REGISTERED", 
                        'message':"Face not registered"}}

            image1 = decode_base64_image(image_frame)
            # faces1 = self.face_detect_service.detect_face(image1, anti_spoof_service=True)
            faces1 = self.face_detect_service.detect_face(image1)
            if isinstance(faces1, dict) and faces1.get('success') is False:
                return faces1
            face1 = faces1[0]
            x1, y1, w1, h1 = int(face1.x), int(face1.y), int(face1.w), int(face1.h)

            image2 = decode_base64_image(image_face_info)
            faces2 = self.face_detect_service.detect_face(image2)
            face2 = faces2[0]
            x2, y2, w2, h2 = int(face2.x), int(face2.y), int(face2.w), int(face2.h)

            verify_result = self.facial_recognition_service.verify(
                img1_path=image1[y1:y1+h1, x1:x1+w1],
                img2_path=image2[y2:y2+h2, x2:x2+w2]
            )
        
            return {'success': True,
                    'result': {'code': 'OK','message': verify_result}}
                
        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}
