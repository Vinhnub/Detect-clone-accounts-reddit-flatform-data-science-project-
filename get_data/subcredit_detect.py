import praw

reddit = praw.Reddit(
    client_id="nX_QTy5GUIfPao80akP1Mw",
    client_secret="oMjRLSYCrqvP_Uvt2pyEnIu1tOjV6g",
    user_agent="myApp"
)

username = "bajie90"
user = reddit.redditor(username)

subreddits = set()

# Lấy từ submissions
for submission in user.submissions.new(limit=None):
    subreddits.add(str(submission.subreddit))

# Lấy từ comments
for comment in user.comments.new(limit=None):
    subreddits.add(str(comment.subreddit))

print("User từng hoạt động ở các subreddit sau:")
print(subreddits)
