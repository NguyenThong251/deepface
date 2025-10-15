
import io, numpy as np, mysql.connector
from src.config.sql import db_config

class SQLService: 
    def __init__(self):
        self.db = mysql.connector.connect(**db_config)

    def get_face_info(self, employee_id) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT face_image FROM face WHERE employ_id = %s", (employee_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            return False
            
    def create_face_info(self, employee_id, image_face: str) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO face (employ_id, face_image) VALUES (%s, %s)", (employee_id, image_face))
            self.db.commit()
            return True
        except Exception as e:
            return False
    
    def face_user_exists(self, employee_id) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM face WHERE employ_id = %s", (employee_id,))
            return cursor.fetchone()
        except Exception as e:
            return False
