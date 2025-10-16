
import io, numpy as np, mysql.connector
from src.config.sql import db_config

class SQLService: 
    def __init__(self):
        self.db = mysql.connector.connect(**db_config)

    def get_face_info(self, user_id) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT image_face FROM face WHERE user_id = %s", (user_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            return False
            
    def create_face_info(self, user_id, image_face: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO face (user_id, image_face) VALUES (%s, %s)", (user_id, image_face))
            self.db.commit()
            return True
        except Exception as e:
            return False
    
    def face_user_exists(self, user_id) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM face WHERE user_id = %s", (user_id,))
            return cursor.fetchone()
        except Exception as e:
            return False
