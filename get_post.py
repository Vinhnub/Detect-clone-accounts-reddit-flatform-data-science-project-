import praw
reddit = praw.Reddit(
    client_id="lytAsA6BedHXqb4liYC61Q",
    client_secret="g8nwEjE3ap5GbjVVyK6HY39sAvAMZg",
    user_agent="laydata by u/Kaya177",
)
target_user = "decartai"
user = reddit.redditor(target_user)


print(f"Đang lấy bài viết của user: {target_user}")
for submission in user.submissions.new(limit=None):
    print("Tiêu đề:", submission.title)
    print("Score:", submission.score)
    print("Upvotes:", submission.ups)
    print("Comments:", submission.num_comments)
    print("Thời gian:", submission.created_utc)
    print("-" * 40)
