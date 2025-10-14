from typing import Any, Dict
import numpy as np
from flask import jsonify

from src.services.detect_face import DetectFaceService
from src.services.anti_spoof import AntiSpoofService
from src.services.redis import RedisService
from src.utils.imgbase64 import decode_base64_image


class ProcessController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.anti_spoof_service = AntiSpoofService()
        self.redis_service = RedisService()
    
    def process_image(self, data: Dict[str, Any]):
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
            self.redis_service.create_temp_image(employee_id, img[y:y+h, x:x+w])

            res = self.redis_service.get_temp_image(employee_id)
            return jsonify({"success": "OK"}), 200
            
        except Exception as e:
            return {'error': {'code': 'SYSTEM ERROR'}}, 500
