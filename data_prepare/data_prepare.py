# format: link_karma, comment_karma, verified_email, totol_posts, totol_comments, avg_post_score, avg_comment_score
# total_achievements, tf_idf_post_content, tf_idf_comment, subreddit_count
from database.database_fetcher import DatabaseFetcher
import pandas as pd
import numpy as np

oDatabase = DatabaseFetcher()
data = {}

users = oDatabase.get_r_user_table()
comments = oDatabase.get_comment_table()
posts = oDatabase.get_post_table()
user_achievements = oDatabase.get_user_achievement_table()

duplicate_score = pd.read_csv("data_prepare/duplicate_score.csv")

def get_post_and_comment_data(user):
    global comments, posts
    user_post = posts[posts["username"] == user]
    user_comment = comments[comments["username"] == user]
    user_post_sub = user_post["subreddit"]
    user_comment_sub = user_comment["subreddit"]
    result = pd.concat([user_post_sub, user_comment_sub], ignore_index=True)
    return len(user_post), len(user_comment), user_post["score"].mean(), user_comment["score"].mean(), len(list(set(result.to_list())))

def cal_total_achievements(user):
    global user_achievements
    user_achievement = user_achievements[user_achievements["username"] == user]
    return len(user_achievement)

def avg_interval(data_check, max_gap_days=1):
    df = data_check.copy()
    if len(df) == 0:
        return 10000000
    df["created"] = pd.to_datetime(df["created"])
    df = df.sort_values("created")
    df["delta_seconds"] = df["created"].diff().dt.total_seconds()
    max_delta = max_gap_days * 24 * 3600
    filtered_deltas = df["delta_seconds"][df["delta_seconds"] <= max_delta]
    if len(filtered_deltas) <= 10:
        return 10000000
    return filtered_deltas.mean()


list_users = users["username"].tolist()

count = 1


for user in list_users:
    if user not in data:
        print(f"{count}. {user}")
        count += 1
        data[user] = {
            "link_karma": np.nan,
            "comment_karma": np.nan,
            "verified_email": np.nan,
            "total_posts" : np.nan,
            "total_comments" : np.nan,
            "avg_post_score" : np.nan,
            "avg_comment_score" : np.nan,
            "total_achievements" : np.nan,
            "tf_idf_post_content" : np.nan,
            "tf_idf_comment" : np.nan,
            "subreddit_count" : np.nan,
            "comment_per_post" : np.nan,
            "karma_ratio" : np.nan,
            "avg_post_interval": np.nan,
            "avg_comment_interval": np.nan,
        }
        data[user]["link_karma"] = users.loc[users["username"] == user, "link_karma"].iloc[0]
        data[user]["comment_karma"] = users.loc[users["username"] == user, "comment_karma"].iloc[0]
        data[user]["verified_email"] = 1 if users.loc[users["username"] == user, "verified_email"].iloc[0] else 0
        result = get_post_and_comment_data(user)
        data[user]["total_posts"] = result[0]
        data[user]["total_comments"] = result[1]
        data[user]["avg_post_score"] = result[2]
        data[user]["avg_comment_score"] = result[3]
        data[user]["total_achievements"] = cal_total_achievements(user)
        data[user]["subreddit_count"] = result[4]
        data[user]["comment_per_post"] = 0 if result[0] == 0 else result[1]/result[0]
        data[user]["karma_ratio"] = 0 if data[user]["comment_karma"] == 0 else data[user]["link_karma"]/data[user]["comment_karma"]
        data[user]["avg_post_interval"] = avg_interval(posts[posts["username"] == user])
        data[user]["avg_comment_interval"] = avg_interval(comments[comments["username"] == user])
        tf_idf_post_content = duplicate_score.loc[duplicate_score["username"] == user, "post"]
        if not tf_idf_post_content.empty:
            data[user]["tf_idf_post_content"] = tf_idf_post_content.iloc[0]
        tf_idf_comment = duplicate_score.loc[duplicate_score["username"] == user, "comment"]
        if not tf_idf_comment.empty:
            data[user]["tf_idf_comment"] = tf_idf_comment.iloc[0]
    else:
        continue
data_filtered = pd.DataFrame(columns=['username', 'post', 'comment'])
data_filtered = pd.DataFrame.from_dict(data, orient='index').reset_index()
data_filtered = data_filtered.rename(columns={'index': 'username'})

data_filtered.to_csv("data_prepare/data_training.csv", index=False)
