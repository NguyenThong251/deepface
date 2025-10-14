from typing import Any, Dict
import numpy as np
from flask import jsonify

from src.services.detect_face import DetectFaceService
from src.services.anti_spoof import AntiSpoofService
from src.utils.imgbase64 import decode_base64_image


class RegisterController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.anti_spoof_service = AntiSpoofService()
    
    def register_user(self, data: Dict[str, Any]):
        try:
            img_path = data.get("image_path")
            if not img_path: return jsonify({"error":{"code":"VALIDATION FAILED"}}), 200

            img = decode_base64_image(img_path)
            h, w = img.shape[:2]
            img_is_real, img_score = self.anti_spoof_service.analyze_image(img, (0, 0, w, h))
            if img_score >= self.anti_spoof_service.threshold and not img_is_real:
                return jsonify({"error":{"code":"ANTI SPOOFING"}}), 200

            faces = self.face_detect_service.detect_faces(img)
            if not (faces): return jsonify({"error":{"code":"NO FACE DETECTED"}}), 200

            face = faces[0]
          


            
            return jsonify({"success": "OK"}), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
