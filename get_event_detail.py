import requests
from datetime import datetime, timedelta
import time

# ---------- CONFIG ----------
POPULAR_LIMIT = 10       # số subreddit nổi bật lấy
POST_LIMIT = 50          # số post mỗi subreddit
KEYWORDS = ["r/place", "pixel art", "reddit event", "challenge", "art challenge"]
USER_AGENT = "Mozilla/5.0"
# ----------------------------

def convert_time(utc_timestamp):
    """Chuyển UNIX timestamp sang giờ Việt Nam (UTC+7)"""
    dt_utc = datetime.utcfromtimestamp(utc_timestamp)
    return dt_utc + timedelta(hours=7)

def get_popular_subreddits(limit=POPULAR_LIMIT):
    url = f"https://www.reddit.com/subreddits/popular.json?limit={limit}"
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []
    return [s["data"]["display_name"] for s in r.json()["data"]["children"]]

def get_subreddit_posts(subreddit, limit=POST_LIMIT):
    headers = {"User-Agent": USER_AGENT}
    all_posts = []

    # 1️⃣ Lấy sticky post
    try:
        r = requests.get(f"https://www.reddit.com/r/{subreddit}/about/sticky.json", headers=headers)
        if r.status_code == 200:
            data = r.json().get("data", {})
            if data:
                all_posts.append({
                    "title": data.get("title"),
                    "url": data.get("url"),
                    "created": convert_time(data.get("created_utc", 0)),
                    "score": data.get("score", 0),
                    "num_comments": data.get("num_comments", 0),
                    "subreddit": subreddit,
                    "event_flag": True
                })
    except:
        pass

    # 2️⃣ Lấy post mới
    r = requests.get(f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}", headers=headers)
    if r.status_code == 200:
        for c in r.json()["data"]["children"]:
            data = c["data"]
            title = data.get("title", "")
            flair = data.get("link_flair_text", "") or ""
            award_count = sum([a.get("count",0) for a in data.get("all_awardings",[])])
            # Kiểm tra keyword/flair/award để đánh dấu event
            event_flag = any(k.lower() in title.lower() for k in KEYWORDS) or \
                         any(k.lower() in flair.lower() for k in KEYWORDS) or \
                         award_count >= 5
            all_posts.append({
                "title": title,
                "url": data.get("url"),
                "created": convert_time(data.get("created_utc")),
                "score": data.get("score", 0),
                "num_comments": data.get("num_comments", 0),
                "subreddit": subreddit,
                "event_flag": event_flag
            })
    return all_posts

def search_keyword_posts(keyword, limit=50):
    """Tìm post theo keyword trên tất cả Reddit"""
    url = f"https://www.reddit.com/search.json?q={keyword}&sort=new&limit={limit}"
    headers = {"User-Agent": USER_AGENT}
    posts = []
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        for c in r.json()["data"]["children"]:
            data = c["data"]
            posts.append({
                "title": data.get("title"),
                "url": data.get("url"),
                "created": convert_time(data.get("created_utc")),
                "score": data.get("score", 0),
                "num_comments": data.get("num_comments", 0),
                "subreddit": data.get("subreddit"),
                "event_flag": True
            })
    return posts

# ---------------------------
# Main
# ---------------------------
subreddits = get_popular_subreddits()
print(f"Subreddits nổi bật: {subreddits}\n")

all_event_posts = []

for sr in subreddits:
    print(f"--- Lấy post từ r/{sr} ---")
    posts = get_subreddit_posts(sr)
    all_event_posts.extend(posts)
    for p in posts:
        flag = "EVENT" if p["event_flag"] else "Post"
        print(f"[{flag}] [{p['created']}] r/{p['subreddit']} | {p['title']} | Score:{p['score']} | Comments:{p['num_comments']} | Link:{p['url']}")
    print("\n")
    time.sleep(1)

# 4️⃣ Search keyword trên toàn Reddit
for kw in KEYWORDS:
    print(f"--- Tìm post theo keyword: {kw} ---")
    posts = search_keyword_posts(kw)
    all_event_posts.extend(posts)
    for p in posts:
        print(f"[EVENT] [{p['created']}] r/{p['subreddit']} | {p['title']} | Score:{p['score']} | Comments:{p['num_comments']} | Link:{p['url']}")
    time.sleep(1)

print(f"\nTổng số post / event lấy được: {len(all_event_posts)}")
