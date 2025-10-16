import numpy as np
from typing import Optional

from src.models.face_detection.Yolo import YoloDetectorClientV12n
from src.models.spoofing.FasNet import Fasnet

class DetectFaceService:
    def __init__(self, threshold: float = 0.9):
        self.detector = YoloDetectorClientV12n()
        self.spoof = Fasnet()
        self.threshold = threshold

    def detect_face(self, img: np.ndarray, face_detect_service: bool = True,  anti_spoof_service: bool = False) -> Optional[list | dict]:
        h, w = img.shape[:2]
        if anti_spoof_service is True:
            img_is_real, img_score = self.spoof.analyze(img, (0, 0, w, h))
            if img_score <= self.threshold or not img_is_real:
                return {'success': False,"error": {'message':"ANTI SPOOFING"}}
        if face_detect_service is True:
            faces = self.detector.detect_faces(img)
            if not faces:
                return {'success': False,"error": {'message':"NO FACE DETECTED"}}
        return faces

