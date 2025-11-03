import os
import numpy as np
from ultralytics import YOLO

class MaskYoloDetectorClient:
    def __init__(self, model_path: str = None):
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best.pt")
        self.model = YOLO(self.model_path)
    
    def detect_mask(self, img: np.ndarray) -> bool:
        res = self.model.predict(img, verbose=False, show=False)[0]
        boxes = getattr(res, "boxes", None)
        if not boxes or len(boxes) == 0:
            return False
        if boxes[0].cls[0] == 0:
            return True
        return False

