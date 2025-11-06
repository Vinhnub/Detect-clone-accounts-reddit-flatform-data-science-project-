from datetime import datetime, timedelta, timezone
import time
import sqlite3
import json
from get_data.constants import *
from database.database_access import Database
from termcolor import colored
import pyodbc 
import pandas as pd
import matplotlib.pyplot as plt 

class DatabaseFetcher:
    def __init__(self):
        self.__sqlite_database = Database()
        self.__cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=VINHNUB\SQLEXPRESS;"
                      "Database=spam_account_detect_database;"
                      "Trusted_Connection=yes;") 
        self.__cursor = self.__cnxn.cursor()
        self.__r_user_table = pd.read_sql("select * from r_user", self.__cnxn) # parse_dates=["created"], index_col="created"
        self.__user_achievement_table = pd.read_sql("select * from user_achievement", self.__cnxn)
        self.__post_table = pd.read_sql("select * from post", self.__cnxn) # parse_dates=["created"], index_col="created"
        self.__comment_table = pd.read_sql("select * from comment", self.__cnxn) # parse_dates=["created"], index_col="created"

    def import_from_sqlite_folder(self, folder_path: str):
        count_files = 0
        for filename in os.listdir(folder_path):
            if filename.endswith(".db"):
                count_files += 1
                db_path = os.path.join(folder_path, filename)
                try:
                    sqlite_conn = sqlite3.connect(db_path)
                    tables = pd.read_sql_query(
                        "SELECT name FROM sqlite_master WHERE type='table';",
                        sqlite_conn
                    )

                    for table_name in tables["name"]:
                        try:
                            df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)
                            df.to_sql(table_name, self.__cnxn, if_exists='append', index=False)
                        except Exception as e:
                            print(e)
                    sqlite_conn.close()

                except Exception as e:
                    print(e)

        if count_files == 0:
            print("Cannot found any file .db")
        else:
            print(f"Successfully {count_files} file.")


    def get_r_user_table(self):
        return self.__r_user_table
    
    def get_user_achievement_table(self):
        return self.__user_achievement_table
    
    def get_post_table(self):
        return self.__post_table
    
    def get_comment_table(self):
        return self.__comment_table
    
    def get_size(self):
        print(f"user_achievement: {len(self.__user_achievement_table)}")
        print(f"r_user: {len(self.__r_user_table)}")
        print(f"post: {len(self.__post_table)}")
        print(f"comment: {len(self.__comment_table)}")

# oData = DatabaseFetcher()

# comments = oData.get_comment_table()
# posts = oData.get_post_table()
# users = oData.get_r_user_table()
# achievements = oData.get_user_achievement_table()
# print("===============================================================")
# print(users)
# print("===============================================================")
# print(achievements)
# print("===============================================================")
# print(posts)
# print("===============================================================")
# print(comments)
# print("===============================================================")
# oData.get_size()
# comments = comments.sort_values(by=['score'], ascending=False)
# condition_1 = comments['score'] >= 100
# condition_2 = comments['body'].str.len() >= 1000
# print(comments[condition_2][['id', 'subreddit', 'body', 'score', 'username']])
# filter = comments.groupby('username')['score'].sum().reset_index()
# print(filter)
# comments['created'] = pd.to_datetime(comments['created'])
# comments.set_index('created', inplace=True)
# se_comments = comments.copy()
# se_comments['weekday'] = se_comments.index.weekday
# weekday_counts = se_comments.groupby('weekday')['id'].count().to_frame(name='count')
# weekday_counts.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# print(weekday_counts)
# users_premium = users['premium'] == True
# print(users[users_premium])
# old_user = (pd.Timestamp.now() - users['created']) >= pd.Timedelta(days=1000)
# print(users[old_user])
# print(comments.tail())