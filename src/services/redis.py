import redis

from src.config.redis import redis_config



class RedisService:
    def __init__(self):
        self.client = redis.Redis(**redis_config)





    # def store_temp_image(self, user_id: str, challenge: str, image_frame: str) -> None:
    #     try:
    #         redis_key = f"ERP:TempFaceInfo:{user_id}"
    #         temp_data = self.client.get(redis_key)
    #         temp_images = json.loads(temp_data) if temp_data else {}
    #         temp_images[challenge] = image_frame
    #         self.client.setex(redis_key, self.REDIS_TEMP_EXPIRE, json.dumps(temp_images))
    #         return True
    #     except Exception as e:
    #         return False