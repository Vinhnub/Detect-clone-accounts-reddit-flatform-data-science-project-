import praw
from datetime import datetime


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

# Tài khoản muốn kiểm tra
username = "tunghg789kt3"
user = reddit.redditor(username)


print("===== THÔNG TIN USER =====")
print("Tên:", user.name)
print("Link Karma:", user.link_karma)
print("Comment Karma:", user.comment_karma)
# ---- Premium ----
print(f"🔹 Reddit Premium: {user.is_gold}")


# Ngày tạo tài khoản
created_date = datetime.utcfromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M:%S')
print("Ngày tạo tài khoản:", created_date)


# Subreddit hoạt động
print("\n===== SUBREDDIT HOẠT ĐỘNG =====")
subreddits = {}
for submission in user.submissions.new(limit=None):  
    subreddits[submission.subreddit.display_name] = subreddits.get(submission.subreddit.display_name, 0) + 1
for comment in user.comments.new(limit=None):        
    subreddits[comment.subreddit.display_name] = subreddits.get(comment.subreddit.display_name, 0) + 1


for sub, count in subreddits.items():
    print(f"- {sub}: {count} lần đóng góp")


# Lượt đóng góp
print("\n===== LƯỢT ĐÓNG GÓP  =====")
print("Tổng số bài viết đã lấy:", len(list(user.submissions.new(limit=None))))
print("Tổng số comment đã lấy:", len(list(user.comments.new(limit=None))))


# Thành tựu
print("\n===== THÀNH TỰU =====")
try:
    trophies = user.trophies()
    for trophy in trophies:
        print("-", trophy.name)
except Exception as e:
    print("Không lấy được trophies:", e)