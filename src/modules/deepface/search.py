from typing import Any, Dict
import numpy as np

from src.services.facial_recognition import FacialRecognitionService
from src.services.qdrant import QdrantService
from src.services.detect_face import DetectFaceService
from src.utils.imgbase64 import decode_base64_image


class SearchController:
    def __init__(self):
        self.facial_recognition_service = FacialRecognitionService()
        self.qdrant_service = QdrantService()
        self.face_detect_service = DetectFaceService()

    def search_user(self, data: Dict[str, Any]):
        try:
            image_frame = data.get("image")
            if not image_frame: return {'success': False,"error": {'message':"VALIDATION FAILED"}}

            image = decode_base64_image(image_frame)
            faces = self.face_detect_service.detect_face(image)
            if isinstance(faces, dict) and faces.get('success') is False:
                return faces
            face = faces[0]
            x, y, w, h = int(face.x), int(face.y), int(face.w), int(face.h)
            face_crop = image[y:y+h, x:x+w]
            face_embedding = self.facial_recognition_service.compute_embedding(face_crop)
            result = self.qdrant_service.search_vector(collection_name="faces",query_vector=face_embedding)

            print(result[0])

            if not result[0]:
                return {'success': False,"error": {'message':"NO FACE FOUND"}}
            
            return {'success': True,"result":"OK " + result[0].payload.get("name")}
        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM ERROR' + str(e)}}