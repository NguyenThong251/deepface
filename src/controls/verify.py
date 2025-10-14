from typing import Any, Dict
from flask import jsonify

from src.services.detect_face import DetectFaceService
from src.services.facial_recognition import FacialRecognitionService
from src.services.anti_spoof import AntiSpoofService
from src.utils.imgbase64 import decode_base64_image

class VerifyController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.anti_spoof_service = AntiSpoofService()
        self.facial_recognition_service = FacialRecognitionService()
    
    def verify_user(self, data: Dict[str, Any]):
        try:
            img1_path = data.get("img1_path")
            img2_path = data.get("img2_path")
            
            if not all((img1_path, img2_path)): return jsonify({"error":{"code":"VALIDATION FAILED"}}), 200

            img1 = decode_base64_image(img1_path)
            img2 = decode_base64_image(img2_path)

            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]

            img_is_real, img_score = self.anti_spoof_service.analyze_image(img1, (0, 0, w1, h1))
            if img_score >= self.anti_spoof_service.threshold and not img_is_real:
                return jsonify({"error":{"code":"ANTI SPOOFING"}}), 200


            faces1 = self.face_detect_service.detect_faces(img1)
            faces2 = self.face_detect_service.detect_faces(img2)
            
            if not all((faces1, faces2)): return jsonify({"error":{"code":"NO FACE DETECTED"}}), 200

            face1 = faces1[0]
            face2 = faces2[0]
            
            # Get face coordinates
            face1_area = (int(face1.x), int(face1.y), int(face1.w), int(face1.h))
            face2_area = (int(face2.x), int(face2.y), int(face2.w), int(face2.h))
            
            # Extract face regions
            x1, y1, w1, h1 = face1_area
            x2, y2, w2, h2 = face2_area
            
            verify_result = self.facial_recognition_service.verify(
                img1_path=img1[y1:y1+h1, x1:x1+w1],
                img2_path=img2[y2:y2+h2, x2:x2+w2]
            ) 
            
            return jsonify({"success": {'result': verify_result}}), 200
            
        except Exception as e:
            return {'error': {'code': 'SYSTEM ERROR'}}, 200
