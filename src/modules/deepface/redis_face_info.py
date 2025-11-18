from typing import Any, Dict

from src.services.sql import SQLService
from src.services.redis import RedisService


class RedisFaceInfoController:

    def __init__(self):
        self.sql_service = SQLService()
        self.redis_service = RedisService()

    def redis_face_info(self, data: Dict[str, Any]):
        try:

            face_info_map = self.sql_service.get_all_face_info()

            if not face_info_map:
                return {'success': False,"error": {'code':"USER_NOT_EXIST", 'message':"Face info not found"}}

            save_result = self.redis_service.save_bulk_embeddings(face_info_map)
            failed_users = save_result.get("failed", [])

            response_payload = {
                'code': 'OK' if not failed_users else 'PARTIAL_SAVE',
                'message': True if not failed_users else 'Failed to cache some face info',
                'totalRequested': len(face_info_map),
                'saved': save_result.get("saved", []),
            }

            if failed_users:
                response_payload['failedUsers'] = failed_users
                return {'success': False,"error": response_payload}

            return {'success': True, 'result': response_payload}
        except Exception as e:
            return {'success': False,"error": {'message': str(e)}}