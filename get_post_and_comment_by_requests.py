import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta, timezone

CLIENT_ID = "nX_QTy5GUIfPao80akP1Mw"
SECRET = "oMjRLSYCrqvP_Uvt2pyEnIu1tOjV6g"
USERNAME = "Strange_Buffalo_7001"
PASSWORD = "Vinh1255@@"
USER_AGENT = "Strange_Buffalo_7001"

def to_utc7(ts):
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.astimezone(timezone(timedelta(hours=7)))

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

# ---- Hàm lấy toàn bộ submissions/comments ----
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
            continue
        
        try:
            r2 = requests.get(trophies_url, headers=headers)
        except:
            continue
        if r2.status_code != 200:
            print("Lỗi:", r2.status_code, r2.text)
            continue

        data = r.json()["data"]

        print("\n=== User infomation ===")
        print("Username :", data["name"])
        print("Link Karma:", data["link_karma"])
        print("Comment Karma:", data["comment_karma"])
        print("Total Karma:", data["total_karma"])
        print("Created at  :", to_utc7(data["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"))
        trophies = r2.json()["data"]["trophies"]

        print("\n=== Achiverment ===")
        if trophies:
            for t in trophies:
                trophy = t["data"]
                print("-", trophy["name"])
        else:
            print("Do not have achiverment.")
        break

def get_data_user(username):
    print(f"Đang lấy submissions của {username} ...")
    posts = fetch_user_content(username, "submitted")

    for i, item in enumerate(posts, 1):
        sub = item["data"]
        print(f"--- Post {i} ---")
        print("Subreddit:", sub["subreddit"])
        print("Title    :", sub["title"])
        print("Content  :", sub.get("selftext") or "[No text / Link post]")
        print("URL      :", sub["url"])
        print("Score    :", sub["score"])
        print("Created  :", to_utc7(sub["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"))
        print()

    # ---- Lấy comments ----
    print(f"\nĐang lấy comments của {username} ...")
    comments = fetch_user_content(username, "comments")

    for i, item in enumerate(comments, 1):
        c = item["data"]
        print(f"--- Comment {i} ---")
        print("Subreddit:", c["subreddit"])
        print("Body     :", c["body"])
        print("Score    :", c["score"])
        print("Created  :", to_utc7(c["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"))
        print()

    print(f"Tổng cộng: {len(posts)} submissions, {len(comments)} comments.")

# with open("users.txt", "r", encoding="utf-8") as file:
#     all_user = file.readlines()
#     for line in all_user:
#         line = line.strip()
#         get_data_user(line)
get_data_user("laonnia")