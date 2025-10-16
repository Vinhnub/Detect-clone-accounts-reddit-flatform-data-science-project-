import sqlite3

class Database:
    def __init__(self, path="database/data.db"):
        self.__conn = sqlite3.connect(path)
        self.__cursor = self.__conn.cursor()

    def get_conn(self):
        return self.__conn
    
    def get_cursor(self):
        return self.__cursor
    
    def close(self):
        self.__conn.close()