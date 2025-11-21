# src\modules\ekyc\register.py
from typing import Any, Dict
import numpy as np
import json

from src.services.sql import SQLService
from src.services.redis import RedisService

from src.services.detect_face import DetectFaceService
from src.services.facial_recognition import FacialRecognitionService
from src.utils.imgbase64 import decode_base64_image
from src.utils.face_crop import face_crop

class RegisterController:
    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()

        self.face_detect_service = DetectFaceService()
        self.facial_recognition_service = FacialRecognitionService()

    # update 
    def register_user(self, data: Dict[str, Any]):
        try:
            user_id = data.get("userId")
            if not user_id: return {'success': False,"error": {'code':"VALIDATION_FAILED",
                'message':"User required"}}

            face_info = self.sql_service.get_face_info(user_id)
            if face_info is not None:
                return {'success': False,"error": {'code':"ALREADY_REGISTERED",
                'message':"User has registered face"}}

            image_face = self.redis_service.get_temp_embeddings(user_id)
            if image_face is None: return {'success': False,"error": {'code':"NO_TEMP_IMAGES",
                'message':"Image not found"}}

            face_embedding = self.facial_recognition_service.compute_embedding(image_face)

            res_save_redis = self.redis_service.save_embeddings(user_id, face_embedding)
            if res_save_redis is False: return {'success': False,"error": {'code':"SAVE_FAILED",
                'message':"Failed to save to Redis"}}

            emb = np.array(face_embedding, dtype=np.float32)
            embedding_str = json.dumps(emb.tolist())
            res_sql = self.sql_service.create_face_info(user_id , embedding_str)
            if res_sql is False: return {'success': False,"error": {'code':"SAVE_FAILED",
                'message':"Failed to save to database"}}
            
            self.redis_service.delete_temp_embeddings(user_id)
            self.redis_service.delete_user_info(user_id)

            return {'success': True, 'result': {'code': 'OK',
                'message': True}}
            
        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}
    #####

