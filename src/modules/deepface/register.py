from typing import Any, Dict
import numpy as np

from src.services.sql import SQLService
from src.services.redis import RedisService

class RegisterController:
    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()
    
    def register_user(self, data: Dict[str, Any]):
        try:
            user_id = data.get("userId")
            if not user_id: return {'success': False,"error": {'code':"VALIDATION_FAILED",
                'message':"User required"}}

            if self.sql_service.get_face_info(user_id): 
                return {'success': False,"error": {'code':"ALREADY_REGISTERED",
                'message':"User has registered face"}}

            image_face = self.redis_service.get_temp_image(user_id)
            if image_face is None: return {'success': False,"error": {'code':"NO_TEMP_IMAGES",
                'message':"Image not found"}}

            res_sql = self.sql_service.create_face_info(user_id , image_face)
            if res_sql is False: return {'success': False,"error": {'code':"SAVE_FAILED",
                'message':"Failed to save to database"}}
            
            self.redis_service.delete_temp_image(user_id)

            return {'success': True, 'result': {'code': 'OK',
                'message': True}}
            
        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}


# TEST QDRANT

# from typing import Any, Dict
# import numpy as np

# from src.services.sql import SQLService
# from src.services.redis import RedisService
# from src.services.qdrant import QdrantService
# from src.services.detect_face import DetectFaceService
# from src.services.facial_recognition import FacialRecognitionService
# from src.utils.imgbase64 import decode_base64_image


# class RegisterController:
#     def __init__(self):
#         self.sql_service = SQLService()
#         self.redis_service = RedisService()
#         self.qdrant_service = QdrantService()
#         self.face_detect_service = DetectFaceService()
#         self.facial_recognition_service = FacialRecognitionService()

#     def register_user(self, data: Dict[str, Any]):
#         try:
#             user_id = data.get("user_id")
#             name = data.get("name")
#             # test

#             image_frame = data.get("image")
#             if not user_id: return {'success': False,"error": {'message':"VALIDATION FAILED"}}
            
#             # vector database
#             imagergb_face = decode_base64_image(image_frame)
#             faces = self.face_detect_service.detect_face(imagergb_face)
#             if isinstance(faces, dict) and faces.get('success') is False:
#                 return faces
#             face = faces[0]
#             x, y, w, h = int(face.x), int(face.y), int(face.w), int(face.h)
#             face_crop = imagergb_face[y:y+h, x:x+w]
#             face_embedding = self.facial_recognition_service.compute_embedding(face_crop)

#             face_vector = self.qdrant_service.insert_vector(collection_name="faces",point_id=int(user_id),vector=face_embedding,payload={"user_id": int(user_id), "name": name})
#             # vector database

#             return {'success': True, 'result': {'message': 'OK'}}
            
#         except Exception as e:
#             return {'success': False,"error": {'message': 'SYSTEM ERROR' + str(e)}}



