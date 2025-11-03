from typing import Any, Dict

from src.services.detect_face import DetectFaceService
from src.utils.imgbase64 import decode_base64_image

class MaskController:
    def __init__(self):
        self.face_detect_service = DetectFaceService()
    
    def detect_mask(self, data: Dict[str, Any]):
        try:
            image_frame = data.get("frame")
            if not image_frame: return {'success': False,"error": {'message':"VALIDATION FAILED"}}

            image = decode_base64_image(image_frame)
            mask_detected = self.face_detect_service.detect_mask(image)
            if mask_detected:
                return {'success': False, 'result': {'code': 'MASK_DETECTED','message': False}}
            else:
                return {'success': True, 'result': {'code': 'OK','message': True}}

        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM ERROR' + str(e)}}
