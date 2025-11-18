from datetime import datetime
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
            cursor.execute("SELECT images FROM vtiger_timekeeping_face WHERE owner = %s", (user_id,))
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
            res_sql = cursor.execute("INSERT INTO vtiger_timekeeping_face (owner, images, created_at) VALUES (%s, %s, %s)", (user_id, image_face, datetime.now()))
            res = connection.commit()
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
            cursor.execute("DELETE FROM vtiger_timekeeping_face WHERE owner=%s", (user_id,))
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