import io
import redis
import numpy as np
from typing import Optional
from src.config.redis import redis_config

class RedisService:

    expiration_time = 300
    prefix = "ERP:TempFaceInfo:"

    def __init__(self):
        self.client = redis.Redis(**redis_config)

    def create_temp_image(self, employee_id: str, image_frame: np.ndarray) -> None:
        try:
            redis_key = f"{self.prefix}{employee_id}"
            bio = io.BytesIO(); 
            np.savez_compressed(bio, arr=image_frame)
            self.client.setex(redis_key, self.expiration_time, bio.getvalue())
            return True
        except Exception as e:
            return False

    def get_temp_image(self, employee_id: str) -> Optional[np.ndarray]:
        try:
            redis_key = f"{self.prefix}{employee_id}"
            payload = self.client.get(redis_key)
            if payload is None:
                return None
            buf = io.BytesIO(payload)
            data = np.load(buf, allow_pickle=False)
            return data["arr"]
        except Exception as e:
            return False




