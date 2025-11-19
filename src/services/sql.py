from datetime import datetime
import numpy as np
import json

from mysql.connector import pooling
from src.config.sql import db_config

class SQLService: 
    def __init__(self):
        self.connection_pool = pooling.MySQLConnectionPool(**db_config)

    def get_connection(self):
        return self.connection_pool.get_connection()

    def get_face_info(self, user_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT image_face FROM vtiger_timekeeping_face WHERE owner = %s", (user_id,))
            row = cursor.fetchone()
            data = row[0] if row else None
            arr = np.array(json.loads(data), dtype=np.float32)
            return arr if row else None
        except Exception as e:
            return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

    def get_all_face_info(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT owner, image_face FROM vtiger_timekeeping_face")
            rows = cursor.fetchall()
            result = {}
            for owner, image_face in rows or []:
                if image_face is None:
                    continue
                try:
                    arr = np.array(json.loads(image_face), dtype=np.float32)
                    result[str(owner)] = arr
                except Exception:
                    continue
            return result
        except Exception:
            return {}
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
            cursor.execute("INSERT INTO vtiger_timekeeping_face (owner, image_face, created_at) VALUES (%s, %s, %s)", (user_id, image_face, datetime.now()))
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