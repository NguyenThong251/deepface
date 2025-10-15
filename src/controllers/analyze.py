from typing import Any, Dict
import numpy as np
from flask import jsonify

from src.services.detect_face import DetectFaceService
from src.services.anti_spoof import AntiSpoofService
from src.utils.imgbase64 import decode_base64_image


class AnalyzeController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
        self.anti_spoof_service = AntiSpoofService()
    
    def analyze_image(self, data: Dict[str, Any]):
        try:
            img_path = data.get("image_path")
            if not img_path: return {'success': False,"code":"VALIDATION FAILED"}

            img = decode_base64_image(img_path)
            h, w = img.shape[:2]
            img_is_real, img_score = self.anti_spoof_service.analyze_image(img, (0, 0, w, h))
            if img_score >= self.anti_spoof_service.threshold and not img_is_real:
                return {'success': False,"code":"ANTI SPOOFING"}

            faces = self.face_detect_service.detect_faces(img)
            if not faces:
                return {'success': False,"code":"NO FACE DETECTED"}

            results = []
            for face in faces:
                x, y, ww, hh = int(face.x), int(face.y), int(face.w), int(face.h)
                is_real, score = self.anti_spoof_service.analyze_image(img, (x, y, ww, hh))
                
                results.append({
                    "box": {"x": x, "y": y, "w": ww, "h": hh},
                    "det_conf": float(face.confidence),
                    "is_real": bool(is_real),
                    "spoof_score": float(score)
                })

            any_spoof = any(
                self.anti_spoof_service.is_spoof(r["spoof_score"], r["is_real"]) 
                for r in results
            )
            final_label = "spoof" if any_spoof else "live"

            return jsonify({
                "image_level": {
                    "is_real": not any_spoof,
                    "spoof_score": float(img_score),
                    "threshold": self.anti_spoof_service.threshold,
                    "label": final_label
                },
                "faces": results
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
