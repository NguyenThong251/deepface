import os
import numpy as np
from ultralytics import YOLO

class FacePartition:
    def __init__(self, model_path: str = None):
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolov8n.pt")
        self.model = YOLO(self.model_path)
    
    def has_mouth(self, img: np.ndarray):
        res = self.model(img, agnostic_nms=True, verbose=False)[0]
        boxes = getattr(res, "boxes", None)

        if boxes is None or len(boxes) == 0:
            return [], boxes

        labels = []
        for cls_tensor, conf_tensor in zip(boxes.cls, boxes.conf):
            cls_id = int(cls_tensor)
            label = self.model.names[cls_id].lower()
            labels.append(label)

        nose_count = labels.count("nose")
        mouth_count = labels.count("mouth")
        eye_count = labels.count("eye")
        eyebrow_count = labels.count("eyebrow")
        if nose_count >= 1 and mouth_count >= 1 and eye_count >= 2 and eyebrow_count >= 2 :
            return False
        else:
            return True

