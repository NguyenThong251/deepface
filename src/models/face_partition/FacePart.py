import os
import numpy as np
from ultralytics import YOLO

class FacePartition:
    def __init__(self, model_path: str = None):
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolov8n.pt")
        self.model = YOLO(self.model_path)
    
    def has_mouth(self, img: np.ndarray, conf_thres: float = 0.5):
        res = self.model(img, agnostic_nms=True, verbose=False)[0]
        boxes = getattr(res, "boxes", None)

        if boxes is None or len(boxes) == 0:
            return [], boxes

        labels = []
        for cls_tensor, conf_tensor in zip(boxes.cls, boxes.conf):
            conf = float(conf_tensor)
            if conf < conf_thres:
                continue

            cls_id = int(cls_tensor)
            label = self.model.names[cls_id].lower()
            labels.append(label)
        if "mouth" not in labels or "eye" not in labels:
            return True
        else:
            return False

