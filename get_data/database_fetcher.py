from datetime import datetime, timedelta, timezone
import time
import json
from constants import *
from termcolor import colored
import pyodbc 
import pandas as pd
import matplotlib.pyplot as plt 

class DatabaseFetcher:
    def __init__(self):
        self.__cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=VINHNUB\SQLEXPRESS;"
                      "Database=spam_account_detect_database;"
                      "Trusted_Connection=yes;")
        self.__cursor = self.__cnxn.cursor()
        self.__r_user_table = pd.read_sql("select * from r_user", self.__cnxn) # parse_dates=["created"], index_col="created"
        self.__user_achiverment_table = pd.read_sql("select * from user_achiverment", self.__cnxn)
        self.__post_table = pd.read_sql("select * from post", self.__cnxn) # parse_dates=["created"], index_col="created"
        self.__comment_table = pd.read_sql("select * from comment", self.__cnxn) # parse_dates=["created"], index_col="created"


    def get_r_user_table(self):
        return self.__r_user_table
    
    def get_user_achiverment_table(self):
        return self.__user_achiverment_table
    
    def get_post_table(self):
        return self.__post_table
    
    def get_comment_table(self):
        return self.__comment_table
    
    def get_size(self):
        print(f"user_achiverment: {len(self.__user_achiverment_table)}")
        print(f"r_user: {len(self.__r_user_table)}")
        print(f"post: {len(self.__post_table)}")
        print(f"comment: {len(self.__comment_table)}")

oData = DatabaseFetcher()

comments = oData.get_comment_table()
posts = oData.get_post_table()
users = oData.get_r_user_table()
achiverments = oData.get_user_achiverment_table()
# print("===============================================================")
# print(users[:5])
# print("===============================================================")
# print(achiverments[:5])
# print("===============================================================")
# print(posts[:5])
# print("===============================================================")
# print(comments[:5])
# print("===============================================================")
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