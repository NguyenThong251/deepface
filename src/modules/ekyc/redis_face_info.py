from typing import Any, Dict
import os
from dotenv import load_dotenv
from src.services.sql import SQLService
from src.services.redis import RedisService


class RedisFaceInfoController:

    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()

    def redis_face_info(self, data: Dict[str, Any]):
        try:
            load_dotenv()
            accesskey = data.get("accesskey")
            if accesskey != os.getenv("ACCESSKEY"):
                return {'code': 'FAILED', 'message': 'Invalid access key'}

            face_info_map = self.sql_service.get_all_face_info()

            if not face_info_map:
                return {'code': 'USER_NOT_EXIST', 'message': 'Face info not found'}

            save_result = self.redis_service.save_bulk_embeddings(face_info_map)
            failed_users = save_result.get("failed", [])

            if failed_users:
                return {'code': 'FAILED', 'message': 'Failed to cache some face info'}

            return {'code': 'OK', 'message': 'Face info cached successfully'}
        except Exception as e:
            return {'code': 'ERROR', 'message': str(e)}