import os
from tasks_api.core.config import DATABASE_PATH, DATABASE_SCRIPT_PATH
import sqlite3

def check_database():
    """Проверяет наличие базы данных, при отсутствии создает"""
    if os.path.exists(DATABASE_PATH):
        print("База данных уже существует")
        return

    print("База данных не найдена: создание новой")
    with open(DATABASE_SCRIPT_PATH, "r") as f:
        script = f.read()

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.executescript(script)

    print("База данных успешно созданна")