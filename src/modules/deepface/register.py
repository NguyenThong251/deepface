from typing import Any, Dict
import numpy as np

from src.services.sql import SQLService
from src.services.redis import RedisService
from src.services.qdrant import QdrantService
from src.services.detect_face import DetectFaceService
from src.services.facial_recognition import FacialRecognitionService
from src.utils.imgbase64 import decode_base64_image


class RegisterController:
    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()
        self.qdrant_service = QdrantService()
        self.face_detect_service = DetectFaceService()
        self.facial_recognition_service = FacialRecognitionService()

    def register_user(self, data: Dict[str, Any]):
        try:
            user_id = data.get("user_id")
            # test
            img_test = data.get("image_test")
            if not user_id: return {'success': False,"error": {'message':"VALIDATION FAILED"}}

            if self.sql_service.face_user_exists(user_id): 
                return {'success': False,"error": {'message':"FACE USER EXISTS"}}

            image_face = self.redis_service.get_temp_image(user_id)
            

            # vector database
            imagergb_face = decode_base64_image(img_test)
            faces = self.face_detect_service.detect_face(imagergb_face)
            if isinstance(faces, dict) and faces.get('success') is False:
                return faces
            face = faces[0]
            x, y, w, h = int(face.x), int(face.y), int(face.w), int(face.h)
            face_crop = imagergb_face[y:y+h, x:x+w]
            face_embedding = self.facial_recognition_service.compute_embedding(face_crop)

            face_vector = self.qdrant_service.insert_vector(collection_name="faces",point_id=int(user_id),vector=face_embedding,payload={"user_id": int(user_id)})
            # vector database

            if image_face is None: return {'success': False,"error": {'message':"FACE NOT FOUND"}}

            res_sql = self.sql_service.create_face_info(user_id , image_face)
            if res_sql is False: return {'success': False,"error": {'message':"SAVE SQL FAILED"}}
            
            self.redis_service.delete_temp_image(user_id)

            return {'success': True, 'result': {'message': 'OK'}}
            
        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM ERROR' + str(e)}}
