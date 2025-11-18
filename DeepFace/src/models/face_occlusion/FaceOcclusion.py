import os
import numpy as np
from ultralytics import YOLO

class FaceOcclusion:
    def __init__(self, model_path: str = None):
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best.pt")
        self.model = YOLO(self.model_path)
    
    def detect_face_occlusion(self, img: np.ndarray) -> bool:
        res = self.model.predict(img, verbose=False, show=False)[0]
        probs = res.probs
        class_id = int(probs.top1)
        return class_id == 1 