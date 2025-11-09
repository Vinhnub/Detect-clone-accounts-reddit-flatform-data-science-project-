import requests
from requests.auth import HTTPBasicAuth
from datetime import timedelta, timezone, datetime
import time
from termcolor import colored
import logging
from utils.secrets import *
from model.logistic_regression import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import numpy as np
import re


class RedditCrawler:
    custom_stop_words = list(ENGLISH_STOP_WORDS.union({
        'http', 'https', 'www', 'com', 'amp',
        'u', 'r', 'imgur', 'jpg', 'png', 'gif',
        'click', 'buy', 'join', 'discord', 'telegram', 'follow',
        'free', 'giveaway', 'offer', 'limited', 'subscribe'
    }))

    def __init__(self):
        self.__auth = auth = HTTPBasicAuth(CLIENT_ID, SECRET)
        self.__data = {"grant_type": "password",
                       "username": USERNAME,
                       "password": PASSWORD}
        self._get_token()
        self.__time_error = 0
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
                    self.__time_error += 1
                    if self.__time_error >= NUMBER_RETRY:
                        self.__time_error = 0
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
        all_posts = {}
        for i, item in enumerate(posts, 1):
            sub = item["data"]
            all_posts[sub["id"]] = {
                "username": username,
                "subreddit": sub["subreddit"],
                "title": sub["title"],
                "content": sub.get("selftext") or "",
                "p_url": sub["url"],
                "score": sub["score"],
                "created": self.to_utc7(sub["created_utc"]).strftime("%Y-%m-%d %H:%M:%S")
            }
        data_filtered = pd.DataFrame.from_dict(all_posts, orient='index').reset_index()
        data_filtered = data_filtered.rename(columns={'index': 'post_id'})
        return data_filtered
        #self.log(f" Got {len(posts)} posts!", "info")

    def get_user_comment(self, username):
        self.log(f" Getting comments of {username} ...", "normal")
        comments = self._fetch_user_content(username, "comments")
        all_comments = {}
        for i, item in enumerate(comments, 1):
            c = item["data"]
            all_comments[c["id"]] = {
                "content": c["body"],
                "subreddit": c["subreddit"],
                "score": c["score"],
                "created": self.to_utc7(c["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
                "username": username
            }
        data_filtered = pd.DataFrame.from_dict(all_comments, orient='index').reset_index()
        data_filtered = data_filtered.rename(columns={'index': 'comment_id'})
        return data_filtered
        #self.log(f" Got {len(comments)} comments.", "info")

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
                if r.status_code == 404 or r.status_code == 400 or r.status_code == 400:
                    self.__time_error += 1
                    if self.__time_error == NUMBER_RETRY:
                        self.__time_error = 0
                        self.print_error(f" Error!")
                        return
                time.sleep(60)
                continue
            else:
                break
        data = r.json()["data"]
        user_data = {
            "username": data["name"],
            "link_karma": data["link_karma"],
            "comment_karma": data["comment_karma"],
            "created": self.to_utc7(data["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
            "premium": data["is_gold"],
            "verified_email": data["has_verified_email"]
        }
        return user_data
        #self.log(f" Done!", "info")

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
                    self.__time_error += 1
                    if self.__time_error == NUMBER_RETRY:
                        self.__time_error = 0
                        self.print_error(f"Error!")
                        return
                time.sleep(60)
                continue
            else:
                break
        trophies = r.json()["data"]["trophies"]
        user_achievement = {}
        if trophies:

            count = 1
            for t in trophies:
                trophy = t["data"]
                user_achievement[count] = {
                    "username": username,
                    "achievement_name": trophy["name"]
                }
                count += 1
        else:
            pass
            #self.log(f" Do not have achievement.", "normal")
        #self.log(f" Done!", "info")
        data_filtered = pd.DataFrame.from_dict(user_achievement, orient='index').reset_index()
        data_filtered = data_filtered.rename(columns={'index': 'number'})
        return data_filtered

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
                if r.status_code == 401:  # token overdue
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
                    user_data = self.get_user_info(author) #dictionary
                    user_achiverments = self.get_user_achievement(author) #dataframe
                    user_posts = self.get_user_post(author) #dataframe
                    user_comments = self.get_user_comment(author) #dataframe
                    # print(user_data)
                    # print(user_achiverments)
                    # print(user_posts)
                    # print(user_comments)

                    user_feature = pd.DataFrame([{
                        "link_karma": user_data["link_karma"],
                        "comment_karma": user_data["comment_karma"],
                        "verified_email": user_data["verified_email"],
                        "total_posts" : len(user_posts),
                        "total_comments" : len(user_comments),
                        "avg_post_score" : 0 if len(user_posts) == 0 else user_posts["score"].mean(),
                        "avg_comment_score" : 0 if len(user_comments) == 0 else user_comments["score"].mean(),
                        "total_achievements" : len(user_achiverments),
                        "tf_idf_post_content" : 0 if len(user_posts) == 0 else self.cal_content_duplicate_ratio(user_posts),
                        "tf_idf_comment" : 0 if len(user_comments) == 0 else self.cal_content_duplicate_ratio(user_comments),
                        "subreddit_count" : self.subreddit_count(user_posts, user_comments),
                        "comment_per_post" : 0 if len(user_posts) == 0 else len(user_comments)/len(user_posts),
                        "karma_ratio" : 0 if user_data["comment_karma"] == 0 else user_data["link_karma"]/user_data["comment_karma"],
                    }])
                    spam_prob = pipeline.predict_proba(user_feature)[:,1]
                    spam_label = pipeline.predict(user_feature)

                    self.log(f"Got {author}", "info")
                    self.log(f"Spam Probility: {spam_prob}", "info")
                    self.log(f"Spam Label: {spam_label}", "info")
                    if number_user_get >= max_users:
                        running = False
                        break

            #self.log(f" Got {number_user_get} users!", "info")
            time.sleep(60)

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'[^a-z\s]', '', text)
        return text.strip()

    def cal_content_duplicate_ratio(self, data):
        texts = data['content'].tolist()
        texts = [self.clean_text(t) for t in texts if isinstance(t, str) and t.strip()]

        if not texts:
            dup_score = 0
        else:
            try:
                vectorizer = TfidfVectorizer(stop_words=custom_stop_words, lowercase=True)
                tfidf_matrix = vectorizer.fit_transform(texts)

                if tfidf_matrix.shape[0] == 1:
                    dup_score = 0
                else:
                    sim = cosine_similarity(tfidf_matrix)
                    np.fill_diagonal(sim, 0)
                    dup_score = sim.mean()
            except:
                dup_score = 0
        return dup_score


    def subreddit_count(self, posts, comments):
        if len(posts) == 0 and len(comments) == 0:
            return 0
        if len(posts) == 0:
            result = len(list(set(comments["subreddit"].to_list())))
            return result
        if len(comments) == 0:
            result = len(list(set(posts["subreddit"].to_list())))
            return result
        result = pd.concat([posts["subreddit"], comments["subreddit"]], ignore_index=True)
        return len(list(set(result.to_list())))

    def print_error(self, s):
        self.log(s, level="error")

    def to_utc7(self, ts):
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.astimezone(timezone(timedelta(hours=7)))


oBot = RedditCrawler()
oBot.fetch_user(100)
