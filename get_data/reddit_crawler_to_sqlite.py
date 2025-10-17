import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta, timezone
import time
from get_data.constants import *
from termcolor import colored
import logging
from database.database_access import Database
#from get_data.secrets import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--db", default="database/data.db")
args = parser.parse_args()


class RedditCrawlerSQLite:
    def __init__(self):
        self.__auth = auth = HTTPBasicAuth(CLIENT_ID, SECRET)
        self.__data = {"grant_type": "password",
                       "username": USERNAME,
                       "password": PASSWORD}
        self._get_token()
        self.__database = Database(path=args.db)
        self.__conn = self.__database.get_conn()
        self.__cursor = self.__database.get_cursor()
        self.__count_time_error = 0
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def log(self, msg, level="info"):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_str = colored(f"[{now_str}]", "yellow")

        # Terminal
        if level == "info":
            print(time_str, colored(msg, "green"))
            logging.info(msg)
        elif level == "error":
            print(time_str, colored(msg, "red"))
            logging.error(msg)
        elif level == "normal":
            print(time_str, msg)
            logging.info(msg)
        else:
            print(time_str, msg)
            logging.info(msg)

    def _get_token(self):
        while True:
            try:
                res = requests.post("https://www.reddit.com/api/v1/access_token",
                    auth=self.__auth, data=self.__data, headers={"User-Agent": USER_AGENT})
                if res.status_code != 200:
                    self.print_error(f"{res.status_code} {res.text}")
                    time.sleep(60)
                    continue
                self.__token = res.json()["access_token"]   
                self.__headers = {"Authorization": f"bearer {self.__token}",
                                  "User-Agent": USER_AGENT}
                break
            except Exception as e:
                self.print_error(e)
        

    def _fetch_user_content(self, username, kind="submitted", limit=10000):
        url = f"https://oauth.reddit.com/user/{username}/{kind}.json"
        all_items = []
        after = None

        while True:
            params = {"limit": 100}
            if after:
                params["after"] = after

            try:
                r = requests.get(url, headers=self.__headers, params=params)
            except Exception as e:
                self.print_error(e)
                continue
            if r.status_code != 200:
                self.print_error(f"{r.status_code} {r.text}")
                if r.status_code == 401:
                    self._get_token()
                if r.status_code == 404 or r.status_code == 400:
                    self.__count_time_error += 1
                    if self.__count_time_error >= NUMBER_RETRY:
                        self.__count_time_error = 0
                        self.print_error(f" Error!")
                        return all_items
                time.sleep(60)
                continue
            data = r.json()["data"]
            # pretty_json = json.dumps(r.json(), indent=4, sort_keys=True)
            # print(pretty_json)


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

    def get_user_post(self, username):
        self.log(f" Getting submissions of {username} ...", "normal")
        posts = self._fetch_user_content(username, "submitted")
        for i, item in enumerate(posts, 1):
            sub = item["data"]
            try:
                self.__cursor.execute("""
                INSERT INTO post (id, subreddit, title, [content], p_url, score, created, username) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                (sub["id"], 
                sub["subreddit"],
                sub["title"], 
                sub.get("selftext") or "",
                sub["url"], 
                sub["score"],
                self.to_utc7(sub["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
                username))
                self.__conn.commit()
            except Exception as e:
                self.print_error(e)
        self.log(f" Got {len(posts)} posts!", "info")

    def get_user_comment(self, username):
        self.log(f" Getting comments of {username} ...", "normal")
        comments = self._fetch_user_content(username, "comments")

        for i, item in enumerate(comments, 1):
            c = item["data"]
            try:
                self.__cursor.execute("""
                INSERT INTO comment (id, body, subreddit, score, created, username) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, 
                (c["id"], 
                c["body"], 
                c["subreddit"],
                c["score"],
                self.to_utc7(c["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
                username))
                self.__conn.commit()
            except Exception as e:
                self.print_error(e)

        self.log(f" Got {len(comments)} comments.", "info")

    def get_user_info(self, username):
        self.log(f" Getting information of {username}...", "normal")
        url = f"https://oauth.reddit.com/user/{username}/about.json"
        while True: 
            try:
                r = requests.get(url, headers=self.__headers)
            except Exception as e:
                self.print_error(e)
                continue
            if r.status_code != 200:
                self.print_error(f"{r.status_code} {r.text}")
                if r.status_code == 401:
                    self._get_token()
                if r.status_code == 404 or r.status_code == 400:
                    self.__count_time_error += 1
                    if self.__count_time_error == NUMBER_RETRY:
                        self.__count_time_error = 0
                        self.print_error(f" Error!")
                        return
                time.sleep(60)
                continue
            else:
                break
        data = r.json()["data"]
        try:
            self.__cursor.execute("""
            INSERT INTO r_user (username, link_karma, comment_karma, created, premium, verified_email) 
            VALUES (?, ?, ?, ?, ?, ?)
            """, 
            (data["name"], 
            data["link_karma"], 
            data["comment_karma"], 
            self.to_utc7(data["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
            data["is_gold"],
            data["has_verified_email"]))
            self.__conn.commit()
        except Exception as e:
            self.print_error(e)

        self.log(f" Done!", "info")

    def get_user_achievement(self, username):
        self.log(f" Getting achievement of {username}...", "normal")
        trophies_url = f"https://oauth.reddit.com/api/v1/user/{username}/trophies.json"
        while True: 
            try:
                r = requests.get(trophies_url, headers=self.__headers)
            except:
                continue
            if r.status_code != 200:
                self.print_error(f"{r.status_code} {r.text}")
                if r.status_code == 401:
                    self._get_token()
                if r.status_code == 404 or r.status_code == 400:
                    self.__count_time_error += 1
                    if self.__count_time_error == NUMBER_RETRY:
                        self.__count_time_error = 0
                        self.print_error(f"Error!")
                        return   
                time.sleep(60)
                continue
            else:
                break
        trophies = r.json()["data"]["trophies"]

        if trophies:
            for t in trophies:
                trophy = t["data"]
                try:
                    self.__cursor.execute("""
                INSERT INTO achievement (achievement_name) 
                VALUES (?)
                """, (trophy["name"],))
                except Exception as e:
                    pass
                try:
                    self.__cursor.execute("""
                INSERT INTO user_achievement (username, achievement_name) 
                VALUES (?, ?)
                """, (username, trophy["name"]))
                except Exception as e:
                    self.print_error(e)
                self.__conn.commit()
        else:
            self.log(f" Do not have achievement.", "normal")
        self.log(f" Done!", "info")

    def fetch_user(self, max_users, subreddit="all"):
        number_user_get = 0
        dicts = {}
        url = f"https://oauth.reddit.com/r/{subreddit}/new.json"
        running = True

        while running:
            params = {"limit": 100}

            try:
                r = requests.get(url, headers=self.__headers, params=params)
            except Exception as e:
                time.sleep(10)
                self.print_error(e)

            if r.status_code != 200:
                self.print_error(f"{r.status_code} {r.text}")
                if r.status_code == 401: # token overdue
                    self._get_token()
                time.sleep(60)
                continue

            data = r.json()["data"]
            children = data["children"]

            for child in children:
                author = child["data"]["author"]
                if author not in ("[deleted]", "AutoModerator") and author not in dicts:  
                    dicts[author] = 1
                    number_user_get += 1
                    print(f"================ User {number_user_get} ================")
                    self.get_user_info(author)
                    self.get_user_achievement(author)
                    self.get_user_post(author)
                    self.get_user_comment(author)
                    if number_user_get >= max_users:
                        running = False
                        break

            self.log(f" Got {number_user_get} users!", "info")
            time.sleep(60)  
        
        self.__database.close()

    def print_error(self, s):
        self.log(s, level="error")

    def to_utc7(self, ts):
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.astimezone(timezone(timedelta(hours=7)))
    
oBot = RedditCrawlerSQLite()
oBot.fetch_user(100)
    