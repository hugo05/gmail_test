#testPassword10


import sqlite3
from constants import DB_NAME

class DB:
    _connection = None

    @classmethod
    def _get_connection(cls):
        if cls._connection is None:
            cls._connection = sqlite3.connect(DB_NAME)
        return cls._connection

    @classmethod
    def _get_cursor(cls):
        conn = cls._get_connection()
        return conn.cursor()

    @classmethod
    def get_data(cls, query, data=()):
        conn = cls._get_connection()
        cursor = cls._get_cursor()
        try:
            cursor.execute(query, data)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            cursor.close()

    @classmethod
    def insert_data(cls, query, data=()):
        conn = cls._get_connection()
        cursor = cls._get_cursor()
        try:
            cursor.execute(query, data)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            cursor.close()

        return False
