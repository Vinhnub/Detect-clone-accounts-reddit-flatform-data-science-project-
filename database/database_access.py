import sqlite3
import os

class Database:
    def __init__(self, path="database/data.db"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.__conn = sqlite3.connect(path)
        self.__cursor = self.__conn.cursor()
        self._execute_script("database/query.sql")

    def _execute_script(self, script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        self.__cursor.executescript(sql_script)
        self.__conn.commit()

    def close(self):
        self.__conn.close()
