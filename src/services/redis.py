import redis
import json
import numpy as np
from typing import Dict
from src.config.redis import redis_config

class RedisService:

    # update  
    expiration_time = 600
    prefix_temp_embeddings = "ERP:TempFaceInfo:"
    prefix_embeddings = "ERP:FaceInfo:"
    prefix_user_info = "ERP:User:"
    #####

    def __init__(self):
        self.client = redis.Redis(**redis_config)


    def delete_temp_embeddings(self, user_id: str):
        try:
            redis_key = f"{self.prefix_temp_embeddings}{user_id}"
            self.client.delete(redis_key)
            return True
        except Exception as e:
            return False

    def save_temp_embeddings(self, user_id: str, embeddings):
        try:
            redis_key = f"{self.prefix_temp_embeddings}{user_id}"
            emb = np.array(embeddings, dtype=np.float32)
            data_str = json.dumps(emb.tolist())
            return self.client.setex(redis_key, self.expiration_time, data_str)
        except Exception as e:
            return False


    def get_temp_embeddings(self, user_id: str):
        try:
            redis_key = f"{self.prefix_temp_embeddings}{user_id}"
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

    # update 
    def delete_user_info(self, user_id: str):
        try:
            redis_key = f"{self.prefix_user_info}{user_id}"
            self.client.delete(redis_key)
            return True
        except Exception:
            return False
    #####


    def get_module_info(self, user_role: str, module_name: str):
        try:
            redis_key = f"ERP:ModuleInfo:{user_role}"
            data = self.client.hget(redis_key, module_name)
            data = data.decode("utf-8")
            return json.loads(data)
        except Exception as e:
            return None
    #####