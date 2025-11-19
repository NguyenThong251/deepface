import redis
import json
import numpy as np
from typing import Dict
from src.config.redis import redis_config

class RedisService:

    expiration_time = 600
    prefix = "ERP:TempFaceInfo:"
    prefix_embeddings = "ERP:FaceInfo:"

    def __init__(self):
        self.client = redis.Redis(**redis_config)


    def delete_temp_embeddings(self, user_id: str):
        try:
            redis_key = f"{self.prefix}{user_id}"
            self.client.delete(redis_key)
            return True
        except Exception as e:
            return False

    def save_temp_embeddings(self, user_id: str, embeddings):
        try:
            redis_key = f"{self.prefix}{user_id}"
            emb = np.array(embeddings, dtype=np.float32)
            data_str = json.dumps(emb.tolist())
            return self.client.setex(redis_key, self.expiration_time, data_str)
        except Exception as e:
            return False


    def get_temp_embeddings(self, user_id: str):
        try:
            redis_key = f"{self.prefix}{user_id}"
            data = self.client.get(redis_key)
            data = data.decode("utf-8")
            arr = np.array(json.loads(data), dtype=np.float32)
            return arr
        except Exception as e:
            return None
    
    def save_embeddings(self, user_id: str, embeddings):
        try:
            redis_key = f"{self.prefix_embeddings}{user_id}"
            emb = np.array(embeddings, dtype=np.float32)
            data_str = json.dumps(emb.tolist())
            
            return self.client.set(redis_key, data_str)
        except Exception as e:
            return False
    
    def get_embeddings(self, user_id: str):
        try:
            redis_key = f"{self.prefix_embeddings}{user_id}"
            data = self.client.get(redis_key)
            data = data.decode("utf-8")
            arr = np.array(json.loads(data), dtype=np.float32)
            return arr
        except Exception as e:
            return None

    def delete_embeddings(self, user_id: str):
        try:
            redis_key = f"{self.prefix_embeddings}{user_id}"
            self.client.delete(redis_key)
            return True
        except Exception as e:
            return False

    def save_bulk_embeddings(self, embeddings_map: Dict[str, np.ndarray]):
        try:
            result = {"saved": [], "failed": []}
            for user_id, embeddings in embeddings_map.items():
                if embeddings is None:
                    continue
                saved = self.save_embeddings(user_id, embeddings)
                if saved:
                    result["saved"].append(user_id)
                else:
                    result["failed"].append(user_id)
            return result
        except Exception:
            return {"saved": [], "failed": list(embeddings_map.keys())}