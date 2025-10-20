from datetime import datetime, timedelta, timezone
import time
import sqlite3
import json
import os
from termcolor import colored
import pyodbc 
import pandas as pd
import matplotlib.pyplot as plt 

from sqlalchemy import create_engine
import urllib

class DatabaseFetcher:
    def __init__(self):
        self.__connection_string = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=VINHNUB\\SQLEXPRESS;"
            "Database=spam_account_detect_database;"
            "Trusted_Connection=yes;"
        )
        self.__cnxn = pyodbc.connect(self.__connection_string)
        self.__cursor = self.__cnxn.cursor()

        params = urllib.parse.quote_plus(self.__connection_string)
        self.__engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

        self.__r_user_table = pd.read_sql("SELECT * FROM r_user", self.__cnxn)
        self.__user_achievement_table = pd.read_sql("SELECT * FROM user_achievement", self.__cnxn)
        self.__post_table = pd.read_sql("SELECT * FROM post", self.__cnxn)
        self.__comment_table = pd.read_sql("SELECT * FROM comment", self.__cnxn)

    def import_from_sqlite_folder(self, folder_path: str):
        count_files = 0
        for filename in os.listdir(folder_path):
            if not filename.endswith(".db"):
                continue

            count_files += 1
            db_path = os.path.join(folder_path, filename)
            print(f"\n==============================")
            print(f"🔹 Import from file: {filename}")
            print(f"==============================")

            try:
                sqlite_conn = sqlite3.connect(db_path)
                tables = pd.read_sql_query(
                    "SELECT name FROM sqlite_master WHERE type='table';", sqlite_conn
                )["name"].tolist()

                import_order = ["r_user", "achievement", "post", "comment", "user_achievement"]

                for table_name in import_order:
                    if table_name not in tables:
                        continue

                    try:
                        df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)

                        if table_name == "r_user" and "username" in df.columns:
                            existing = pd.read_sql("SELECT username FROM r_user", self.__cnxn)
                            df = df[~df["username"].isin(existing["username"])]

                        elif table_name == "achievement" and "achievement_name" in df.columns:
                            existing = pd.read_sql("SELECT achievement_name FROM achievement", self.__cnxn)
                            df = df[~df["achievement_name"].isin(existing["achievement_name"])]

                        elif table_name == "post" and "id" in df.columns:
                            existing = pd.read_sql("SELECT id FROM post", self.__cnxn)
                            df = df[~df["id"].isin(existing["id"])]

                        elif table_name == "comment" and "id" in df.columns:
                            existing = pd.read_sql("SELECT id FROM comment", self.__cnxn)
                            df = df[~df["id"].isin(existing["id"])]

                        elif table_name == "user_achievement" and {"username", "achievement_name"}.issubset(df.columns):
                            existing = pd.read_sql("SELECT username, achievement_name FROM user_achievement", self.__cnxn)
                            merged = df.merge(existing, on=["username", "achievement_name"], how="left", indicator=True)
                            df = merged[merged["_merge"] == "left_only"].drop(columns="_merge")

                            valid_users = pd.read_sql("SELECT username FROM r_user", self.__cnxn)["username"].tolist()
                            valid_achievements = pd.read_sql("SELECT achievement_name FROM achievement", self.__cnxn)["achievement_name"].tolist()

                            invalid_users = df[~df["username"].isin(valid_users)]
                            invalid_achievements = df[~df["achievement_name"].isin(valid_achievements)]

                            if not invalid_users.empty:
                                print(f"⚠️ Skipped {len(invalid_users)} rows in user_achievement: username not found in r_user")

                            if not invalid_achievements.empty:
                                print(f"⚠️ Skipped {len(invalid_achievements)} rows in user_achievement: achievement_name not found in achievement")

                            df = df[
                                df["username"].isin(valid_users)
                                & df["achievement_name"].isin(valid_achievements)
                            ]

                        if len(df) > 0:
                            df.to_sql(table_name, self.__engine, if_exists="append", index=False)
                            print(f"✅ Imported {len(df)} rows to table {table_name}")
                        else:
                            print(f"⚠️ Do not have data for table {table_name}")

                    except Exception as e:
                        print(f"❌ Error import table {table_name}: {e}")

                sqlite_conn.close()

            except Exception as e:
                print(f"❌ Error read file {filename}: {e}")

        if count_files == 0:
            print("⚠️ Cannot found any .db file.")
        else:
            print(f"\n🎯 Successfully processed {count_files} SQLite file(s).")



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

oData = DatabaseFetcher()

comments = oData.get_comment_table()
posts = oData.get_post_table()
users = oData.get_r_user_table()
achievements = oData.get_user_achievement_table()
print("===============================================================")
print(users)
print("===============================================================")
print(achievements)
print("===============================================================")
print(posts)
print("===============================================================")
print(comments)
print("===============================================================")
oData.get_size()
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