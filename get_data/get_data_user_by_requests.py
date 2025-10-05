import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta, timezone
import time
import json
from constants import *
from termcolor import colored
import pyodbc 


auth = HTTPBasicAuth(CLIENT_ID, SECRET)
data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}
headers = {"User-Agent": USER_AGENT}

res = requests.post("https://www.reddit.com/api/v1/access_token",
                    auth=auth, data=data, headers=headers)
res.raise_for_status()
token = res.json()["access_token"]

headers = {
    "Authorization": f"bearer {token}",
    "User-Agent": USER_AGENT
}


cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=VINHNUB\SQLEXPRESS;"
                      "Database=spam_account_detect_database;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()


def print_error(s):
    print(colored(s, "red"))

def to_utc7(ts):
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.astimezone(timezone(timedelta(hours=7)))

def fetch_user_content(username, kind="submitted", limit=10000):
    url = f"https://oauth.reddit.com/user/{username}/{kind}"
    all_items = []
    after = None

    while True:
        params = {"limit": 100}
        if after:
            params["after"] = after

        try:
            r = requests.get(url, headers=headers, params=params)
        except:
            continue
        if r.status_code != 200:
            print("Lỗi:", r.status_code, r.text)
            time.sleep(60)
            continue
        data = r.json()["data"]

        children = data["children"]
        if not children:
            break

        all_items.extend(children)

        after = data.get("after")
        if not after:
            break

        if limit and len(all_items) >= limit:
            all_items = all_items[:limit]
            break

    return all_items

def get_user_info(username):
    url = f"https://oauth.reddit.com/user/{username}/about"
    trophies_url = f"https://oauth.reddit.com/api/v1/user/{username}/trophies"
    while True: 
        try:
            r = requests.get(url, headers=headers)
        except:
            continue
        if r.status_code != 200:
            print("Lỗi:", r.status_code, r.text)
            time.sleep(60)
            continue
        
        try:
            r2 = requests.get(trophies_url, headers=headers)
        except:
            continue
        if r2.status_code != 200:
            print("Lỗi:", r2.status_code, r2.text)
            time.sleep(60)
            continue

        data = r.json()["data"]   

        print("\n=== User infomation ===")
        print("Username :", data["name"])
        print("Link Karma:", data["link_karma"])
        print("Comment Karma:", data["comment_karma"])
        print("Total Karma:", data["total_karma"])
        print("Created at  :", to_utc7(data["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"))
        print("Has verified email:", "Yes" if data["has_verified_email"] else "No")
        print("Premium  :", 0 if data.get("is_premium") is None else 1)

        try:
            cursor.execute("""
        INSERT INTO r_user (username, link_karma, comment_karma, created, premium, verified_email) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, 
            data["name"], 
            data["link_karma"], 
            data["comment_karma"], 
            to_utc7(data["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
            0 if data.get("is_premium") is None else 1,
            data["has_verified_email"])
        
            cursor.commit()
        except Exception as e:
            print_error(e)
  
        trophies = r2.json()["data"]["trophies"]

        print("\n=== Trophies ===")
        if trophies:
            for t in trophies:
                trophy = t["data"]
                print("-", trophy["name"])
                try:
                    cursor.execute("""
                INSERT INTO achiverment (achiverment_name) 
                VALUES (?)
                """, 
                    trophy["name"])
                    cursor.execute("""
                INSERT INTO user_achiverment (username, achiverment_name) 
                VALUES (?, ?)
                """,
                    username,
                    trophy["name"])
                    cursor.commit()
                except:
                    pass

        else:
            print("Do not have achiverment.")
        break

def get_data_user(username):
    print(f"Đang lấy submissions của {username} ...")
    posts = fetch_user_content(username, "submitted")

    for i, item in enumerate(posts, 1):
        sub = item["data"]
        # print(f"--- Post {i} ---")
        # print("Id:", sub["id"])
        # print("Subreddit:", sub["subreddit"])
        # print("Title    :", sub["title"])
        # print("Content  :", sub.get("selftext") or "[No text / Link post]")
        # print("URL      :", sub["url"])
        # print("Score    :", sub["score"])
        # print("Created  :", to_utc7(sub["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"))
        # print()

        try:
            cursor.execute("""
        INSERT INTO post (id, subcredit, title, [content], p_url, score, created, username) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, 
            sub["id"], 
            sub["subreddit"],
            sub["title"], 
            sub.get("selftext") or "",
            sub["url"], 
            sub["score"],
            to_utc7(sub["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
            username)
            cursor.commit()
        except:
            pass

    # ---- Lấy comments ----
    print(f"\nĐang lấy comments của {username} ...")
    comments = fetch_user_content(username, "comments")

    for i, item in enumerate(comments, 1):
        c = item["data"]
        # print(f"--- Comment {i} ---")
        # print("Id:", c["id"])
        # print("Subreddit:", c["subreddit"])
        # print("Body     :", c["body"])
        # print("Score    :", c["score"])
        # print("Created  :", to_utc7(c["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"))
        # print()

        try:
            cursor.execute("""
        INSERT INTO comment (id, body, subcredit, score, created, username) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, 
            c["id"], 
            c["body"], 
            c["subreddit"],
            c["score"],
            to_utc7(c["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
            username)
            cursor.commit()
        except:
            pass

    print(f"Tổng cộng: {len(posts)} submissions, {len(comments)} comments.")

# with open("users.txt", "r", encoding="utf-8") as file:
#     all_user = file.readlines()
#     for user in all_user:
#         user = user.strip()
#         #get_user_info(user)
#         get_data_user(user)
get_user_info("s9phea")
#get_data_user("13tarry")
