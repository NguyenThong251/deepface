from models.face_detection.Yolo import YoloDetectorClientV12n

class DetectFaceService:
    def __init__(self):
        self.detector = YoloDetectorClientV12n()
        
    def detect_faces(self, img):
        return self.detector.detect_faces(img)
