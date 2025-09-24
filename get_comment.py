import requests
from datetime import datetime, timedelta
import time

USERNAME = "decartai"  # đổi thành user bạn muốn lấy
LIMIT = 100         # số comment lấy mỗi lần request (max 100)

def convert_time(utc_timestamp):
    """Chuyển UNIX timestamp sang giờ Việt Nam (UTC+7)"""
    dt_utc = datetime.utcfromtimestamp(utc_timestamp)
    return dt_utc + timedelta(hours=7)

def get_all_comments(username):
    comments = []
    after = None  # dùng để pagination

    while True:
        url = f"https://www.reddit.com/user/{username}/comments.json?limit={LIMIT}"
        if after:
            url += f"&after={after}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Lỗi API:", response.status_code)
            break

        data = response.json()["data"]
        children = data["children"]
        if not children:
            break

        for c in children:
            comment_data = c["data"]
            comments.append({
                "datetime": convert_time(comment_data["created_utc"]),
                "body": comment_data.get("body", ""),
                "score": comment_data.get("score", 0)
            })

        after = data.get("after")
        if not after:
            break

        time.sleep(1)  # tránh bị rate-limit

    return comments

# Lấy tất cả comment
all_comments = get_all_comments(USERNAME)

# In ra
for c in all_comments:
    print(f"[{c['datetime']}] Score: {c['score']} | Comment: {c['body'][:120]}...")
