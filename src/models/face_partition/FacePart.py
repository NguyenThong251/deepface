# import os
# import numpy as np
# from ultralytics import YOLO

# class FacePartition:
#     def __init__(self, model_path: str = None):
#         self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolov8m.pt")
#         self.model = YOLO(self.model_path)
    
#     def has_mouth(self, img: np.ndarray, conf_thres: float = 0.65):
#         res = self.model(img, agnostic_nms=True, verbose=False)[0]
#         boxes = getattr(res, "boxes", None)

#         if boxes is None or len(boxes) == 0:
#             return True

#         labels = []
#         mouth_boxes = []
#         mouth_confidences = []
        
#         all_boxes_xyxy = boxes.xyxy.cpu().numpy() if boxes.xyxy is not None else []
        
#         for idx, (cls_tensor, conf_tensor) in enumerate(zip(boxes.cls, boxes.conf)):
#             conf = float(conf_tensor)
#             if conf < conf_thres:
#                 continue
                
#             cls_id = int(cls_tensor)
#             label = self.model.names[cls_id].lower()
#             labels.append(label)
            
#             if label == "mouth":
#                 mouth_confidences.append(conf)
#                 if idx < len(all_boxes_xyxy):
#                     mouth_box = all_boxes_xyxy[idx]
#                     mouth_boxes.append(mouth_box)

#         nose_count = labels.count("nose")
#         mouth_count = labels.count("mouth")
#         eye_count = labels.count("eye")
#         eyebrow_count = labels.count("eyebrow")
        
#         if mouth_count == 0:
#             if nose_count > 0 or eye_count > 0:
#                 return True
        
#         has_all_parts = nose_count >= 1 and mouth_count >= 1 and eye_count >= 2 and eyebrow_count >= 2
        
#         if not has_all_parts:
#             if nose_count >= 1 and eye_count >= 2 and mouth_count == 0:
#                 return True
#             if mouth_count == 0:
#                 return True
#             if eyebrow_count < 2 or eye_count < 2:
#                 if mouth_count == 0:
#                     return True
        
#         upper_lip_count = labels.count("upper_lip") + labels.count("upperlip")
#         lower_lip_count = labels.count("lower_lip") + labels.count("lowerlip")
        
#         if upper_lip_count > 0 or lower_lip_count > 0:
#             if upper_lip_count == 0 or lower_lip_count == 0:
#                 return True
        
#         if mouth_boxes and mouth_confidences:
#             h, w = img.shape[:2]
#             img_area = h * w
            
#             nose_boxes = []
#             eye_boxes = []
#             for idx, (cls_tensor, conf_tensor) in enumerate(zip(boxes.cls, boxes.conf)):
#                 conf = float(conf_tensor)
#                 if conf < conf_thres:
#                     continue
#                 cls_id = int(cls_tensor)
#                 label = self.model.names[cls_id].lower()
#                 if label == "nose" and idx < len(all_boxes_xyxy):
#                     nose_boxes.append(all_boxes_xyxy[idx])
#                 elif label == "eye" and idx < len(all_boxes_xyxy):
#                     eye_boxes.append(all_boxes_xyxy[idx])
            
#             max_mouth_conf = max(mouth_confidences) if mouth_confidences else 0
#             avg_mouth_conf = sum(mouth_confidences) / len(mouth_confidences) if mouth_confidences else 0
            
#             mouth_conf_threshold = conf_thres + 0.2
#             if max_mouth_conf < mouth_conf_threshold:
#                 return True
            
#             if avg_mouth_conf < conf_thres + 0.15:
#                 return True
            
#             for mouth_box in mouth_boxes:
#                 x1, y1, x2, y2 = mouth_box
#                 mouth_width = x2 - x1
#                 mouth_height = y2 - y1
#                 mouth_area = mouth_width * mouth_height
#                 mouth_center_y = (y1 + y2) / 2
#                 mouth_center_x = (x1 + x2) / 2
                
#                 mouth_area_ratio = mouth_area / img_area
#                 if mouth_area_ratio < 0.003:
#                     return True
                
#                 if mouth_height > 0:
#                     aspect_ratio = mouth_width / mouth_height
#                     if aspect_ratio < 1.0 or aspect_ratio > 5.0:
#                         return True
                    
#                     if aspect_ratio < 1.2 or aspect_ratio > 4.5:
#                         return True
                
#                 if nose_boxes:
#                     for nose_box in nose_boxes:
#                         nx1, ny1, nx2, ny2 = nose_box
#                         nose_width = nx2 - nx1
#                         nose_height = ny2 - ny1
#                         nose_area = nose_width * nose_height
#                         nose_center_y = (ny1 + ny2) / 2
#                         nose_center_x = (nx1 + nx2) / 2
                        
#                         distance_to_nose_y = abs(mouth_center_y - nose_center_y)
#                         distance_to_nose_x = abs(mouth_center_x - nose_center_x)
                        
#                         if distance_to_nose_y < nose_height * 2.5:
#                             if mouth_height > 0 and nose_height > 0:
#                                 mouth_nose_height_ratio = mouth_height / nose_height

#                                 if mouth_nose_height_ratio < 0.4:
#                                     return True
                        
#                         if nose_area > 0:
#                             mouth_nose_area_ratio = mouth_area / nose_area
#                             if mouth_nose_area_ratio < 0.4:
#                                 return True
                            
#                             if mouth_nose_area_ratio < 0.4:
#                                 if max_mouth_conf < conf_thres + 0.25:
#                                     return True
                
#                 if eye_boxes and len(eye_boxes) >= 2:
#                     eye_areas = []
#                     eye_heights = []
#                     for eye_box in eye_boxes:
#                         ex1, ey1, ex2, ey2 = eye_box
#                         eye_width = ex2 - ex1
#                         eye_height = ey2 - ey1
#                         eye_area = eye_width * eye_height
#                         eye_areas.append(eye_area)
#                         eye_heights.append(eye_height)
                    
#                     avg_eye_area = sum(eye_areas) / len(eye_areas) if eye_areas else 0
#                     avg_eye_height = sum(eye_heights) / len(eye_heights) if eye_heights else 0
                    
#                     if avg_eye_area > 0:
#                         mouth_eye_area_ratio = mouth_area / avg_eye_area
#                         if mouth_eye_area_ratio < 0.6:
#                             return True
                    
#                     if avg_eye_height > 0 and mouth_height > 0:
#                         mouth_eye_height_ratio = mouth_height / avg_eye_height
#                         if mouth_eye_height_ratio < 0.7:
#                             return True
                
#                 if mouth_width < 20 or mouth_height < 10:
#                     return True
                
#                 margin_ratio = 0.05
#                 if (mouth_center_x < w * margin_ratio or 
#                     mouth_center_x > w * (1 - margin_ratio) or
#                     mouth_center_y < h * margin_ratio or 
#                     mouth_center_y > h * (1 - margin_ratio)):
#                     if max_mouth_conf < conf_thres + 0.2:
#                         return True
        
#         return False

import os
import numpy as np
from ultralytics import YOLO

class FacePartition:
    def __init__(self, model_path: str = None):
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolov8m.pt")
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

        if nose_count >= 1 and mouth_count >= 1 and eye_count >= 2 :
            return False
        else:
            return True
