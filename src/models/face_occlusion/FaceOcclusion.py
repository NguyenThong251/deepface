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
        score = float(probs.top1conf)
        print(class_id, score)


        return class_id == 1 and score > 0.7

        # if boxes is None or len(boxes) == 0:
        #     return [], boxes

        # labels = []
        # for cls_tensor, conf_tensor in zip(boxes.cls, boxes.conf):
        #     cls_id = int(cls_tensor)
        #     label = self.model.names[cls_id].lower()
        #     labels.append(label)

        # nose_count = labels.count("nose")
        # mouth_count = labels.count("mouth")
        # eye_count = labels.count("eye")
        # eyebrow_count = labels.count("eyebrow")

        # if nose_count >= 1 and mouth_count >= 1 and eye_count >= 2 :
        #     return False
        # else:
        #     return True
