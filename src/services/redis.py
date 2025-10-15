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

    def create_temp_image(self, employee_id: str, image_frame) -> bool:
        try:
            redis_key = f"{self.prefix}{employee_id}"
            self.client.setex(redis_key, self.expiration_time, image_frame)
            return True
        except Exception as e:
            return False

    def get_temp_image(self, employee_id: str):
        try:
            redis_key = f"{self.prefix}{employee_id}"
            return self.client.get(redis_key)
        except Exception as e:
            return False




