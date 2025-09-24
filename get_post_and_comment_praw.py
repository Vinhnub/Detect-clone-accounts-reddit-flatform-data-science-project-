import praw
from datetime import datetime, timedelta, timezone

# Kết nối Reddit API
reddit = praw.Reddit(
    client_id="nX_QTy5GUIfPao80akP1Mw",
    client_secret="oMjRLSYCrqvP_Uvt2pyEnIu1tOjV6g",
    user_agent="myApp",
    username="Strange_Buffalo_7001",   # cần nếu muốn truy cập private sub
    password="Vinh1255@@" 
)

reddit.validate_on_submit = True
reddit.config.allow_nsfw = True

username = "decartai"
user = reddit.redditor(username)

# Hàm chuyển timestamp sang UTC+7
def to_utc7(ts):
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)  # thời gian gốc (UTC)
    return dt.astimezone(timezone(timedelta(hours=7)))  # đổi sang UTC+7

# Lấy submissions (bài post)
count = 1
for submission in user.submissions.new(limit=None):
    print(f"--- Post {count} ---")
    print("Subreddit:", submission.subreddit)
    print("Title    :", submission.title)
    print("Content  :", submission.selftext if submission.selftext else "[No text / Link post]")
    print("URL      :", submission.url)
    print("Score    :", submission.score)
    print("Created  :", to_utc7(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S"))
    print()
    count += 1

# Lấy comments
count = 1
for comment in user.comments.new(limit=None):
    print(f"--- Comment {count} ---")
    print("Subreddit:", comment.subreddit)
    print("Body     :", comment.body)
    print("Score    :", comment.score)
    print("Created  :", to_utc7(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S"))
    print()
    count += 1
