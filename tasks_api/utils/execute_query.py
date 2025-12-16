import sqlite3
from tasks_api.core.config import DATABASE_PATH

def execute_query(query: str, params: tuple = ()):
    """Выполняет запрос к базе данных"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if query.upper().startswith("SELECT") or "RETURNING" in query.upper().split():
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
            conn.commit()
            return result
    except Exception as e:
        print(e)