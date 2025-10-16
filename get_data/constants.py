import os

CLIENT_ID = os.environ["CLIENT_ID"]
SECRET = os.environ["SECRET"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
USER_AGENT = os.environ["USER_AGENT"]


MAX_SIZE_BODY = 8000
NUMBER_RETRY = 2
LOG_FILE = "reddit_crawler.log" 