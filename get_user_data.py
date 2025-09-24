import praw
from datetime import datetime


# Khai báo thông tin API của bạn
reddit = praw.Reddit(
    client_id="PXxWBAYDZbd5NopuLDGapA",        # thay bằng client_id của bạn
    client_secret="KyyTOoPofMECMknM5EdXkKEyZM3qLg",# thay bằng client_secret của bạn
    user_agent="test_app"
)


# Tài khoản muốn kiểm tra
username = "bigbellysnoops"
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


# Followers
try:
    followers = list(user.followers())
    print("Số lượng follower:", len(followers))
except Exception as e:
    print("Không thể lấy số lượng follower (API hạn chế):", e)


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