from typing import Optional
import numpy as np

def image_check(image_frame: np.ndarray, anti_spoof_service=None, face_detect_service=None) -> Optional[list]:
    h, w = image_frame.shape[:2]
    if anti_spoof_service:
        img_is_real, img_score = anti_spoof_service.analyze_image(image_frame, (0, 0, w, h))
        if img_score >= anti_spoof_service.threshold and not img_is_real:
            return {'success': False,"error": {'message':"ANTI SPOOFING"}}
    if face_detect_service:
        faces = face_detect_service.detect_faces(image_frame)
        if not (faces): return {'success': False,"error": {'message':"NO FACE DETECTED"}}
        return faces
