from typing import Any, Dict
from flask import jsonify

from src.services.detect_face import DetectFaceService
from src.services.facial_recognition import FacialRecognitionService
from src.services.anti_spoof import AntiSpoofService
from src.utils.imgbase64 import decode_base64_image
from src.services.sql import SQLService

class VerifyController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.anti_spoof_service = AntiSpoofService()
        self.facial_recognition_service = FacialRecognitionService()
        self.sql_service = SQLService()
    def verify_user(self, data: Dict[str, Any]):
        try:
            employee_id = data.get("employee_id")
            image_frame = data.get("image")
            if not all((employee_id, image_frame)): return jsonify({"error":{"code":"VALIDATION FAILED"}}), 200

            img = decode_base64_image(image_frame)
            h, w = img.shape[:2]
            img_is_real, img_score = self.anti_spoof_service.analyze_image(img, (0, 0, w, h))
            if img_score >= self.anti_spoof_service.threshold and not img_is_real:
                return jsonify({"error":{"code":"ANTI SPOOFING"}}), 200

            faces = self.face_detect_service.detect_faces(img)
            if not (faces): return jsonify({"error":{"code":"NO FACE DETECTED"}}), 200
            
            face = faces[0]
            x, y, w, h = int(face.x), int(face.y), int(face.w), int(face.h)

            imgae_face_info = self.sql_service.get_face_info(employee_id)
            if not imgae_face_info: return jsonify({"error":{"code":"FACE NOT FOUND"}}), 200


            verify_result = self.facial_recognition_service.verify(
                img1_path=img[y:y+h, x:x+w],
                img2_path=imgae_face_info
            ) 
            
            return jsonify({"success": {'result': verify_result}}), 200
            
        except Exception as e:
            return {'error': {'code': 'SYSTEM ERROR'}}, 500
