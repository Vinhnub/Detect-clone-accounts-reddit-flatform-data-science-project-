import requests
import time

def fetch_pushshift(author, kind='comment', max_items=None):
    """
    Lấy toàn bộ comment hoặc submission của 1 user từ Pushshift
    author: username Reddit
    kind: 'comment' hoặc 'submission'
    max_items: số lượng tối đa muốn lấy (None = lấy tất cả)
    """
    base_url = f"https://api.pushshift.io/reddit/search/{kind}/"
    all_data = []
    params = {
        "author": author,
        "size": 500,  # max mỗi lần
        "sort": "desc",
        "sort_type": "created_utc"
    }
    last_created = None

    while True:
        if last_created:
            params["before"] = last_created
        response = requests.get(base_url, params=params)
        if response.status_code == 403:
            print("403 Forbidden – thử sleep 10 giây và retry")
            time.sleep(10)
            continue
        if response.status_code != 200:
            print("Error:", response.status_code)
            break
        data = response.json().get("data", [])
        if not data:
            break
        all_data.extend(data)
        last_created = data[-1]["created_utc"]
        print(f"Lấy được {len(all_data)} {kind}...")
        if max_items and len(all_data) >= max_items:
            all_data = all_data[:max_items]
            break
        time.sleep(1)  # tránh spam server
    return all_data

def print_user_activity(username):
    # Lấy toàn bộ submissions
    print(f"Đang lấy submissions của {username}...")
    submissions = fetch_pushshift(username, kind='submission')
    for i, s in enumerate(submissions, 1):
        print(f"--- Submission {i} ---")
        print("Subreddit:", s.get("subreddit"))
        print("Title    :", s.get("title"))
        print("Content  :", s.get("selftext") or "[No text / Link post]")
        print("URL      :", s.get("url"))
        print("Created  :", s.get("created_utc"))
        print()

    # Lấy toàn bộ comments
    print(f"Đang lấy comments của {username}...")
    comments = fetch_pushshift(username, kind='comment')
    for i, c in enumerate(comments, 1):
        print(f"--- Comment {i} ---")
        print("Subreddit:", c.get("subreddit"))
        print("Body     :", c.get("body"))
        print("Created  :", c.get("created_utc"))
        print()

    print(f"Tổng cộng: {len(submissions)} submissions, {len(comments)} comments.")

# Ví dụ chạy
username = "julman99"
print_user_activity(username)
