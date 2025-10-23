
import io, numpy as np
from mysql.connector import pooling
from src.config.sql import db_config

class SQLService: 
    def __init__(self):
        self.connection_pool = pooling.MySQLConnectionPool(**db_config)

    def get_connection(self):
        return self.connection_pool.get_connection()

    def get_face_info(self, user_id) -> None:
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT image_face FROM face WHERE user_id=%s", (user_id,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass
            
    def create_face_info(self, user_id, image_face: str) -> bool:
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO face (user_id, image_face) VALUES (%s, %s)", (user_id, image_face))
            connection.commit()
            return True
        except Exception as e:
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

    def delete_face_info(self, user_id) -> bool:
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM face WHERE user_id=%s", (user_id,))
            connection.commit()
            return True
        except Exception as e:
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass