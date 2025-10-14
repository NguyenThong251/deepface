import io
import numpy as np
import mysql.connector
from typing import Optional
from src.config.sql import db_config

class SQLService: 
    def __init__(self):
        self.db = mysql.connector.connect(**db_config)

    def get_face_info(self, employee_id: str) -> Optional[tuple]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM face WHERE employee_id = %s", (employee_id,))
            return cursor.fetchone()
        except Exception as e:
            return False

    # def create_face_info(self, employee_id: str, image_face) -> None:
    def create_face_info(self, employee_id, image_face) -> None:
        try:
            bio = io.BytesIO()
            np.savez_compressed(bio, arr=image_face)
            blob = bio.getvalue()

            cursor = self.db.cursor()
            cursor.execute("INSERT INTO face (employee_id, image_face) VALUES (%s, %s)", (employee_id, blob))
            self.db.commit()
            return True
        except Exception as e:
            return False


    # def insert_temp_image(self, employee_id: str, image_frame: str) -> None:
    #     try:
    #         cursor = self.db.cursor()
    #         cursor.execute("INSERT INTO temp_image (employee_id, image_frame) VALUES (%s, %s)", (employee_id, image_frame))
    #         self.db.commit()
    #         return True
    #     except Exception as e:
    #         return False