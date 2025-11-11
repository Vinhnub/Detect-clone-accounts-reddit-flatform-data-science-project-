from scipy.stats import ttest_ind
import pandas as pd

df = pd.read_csv("data_prepare/data_training.csv")

for col in ["link_karma",
            "comment_karma",
            "verified_email",
            "total_posts" ,
            "total_comments" ,
            "avg_post_score" ,
            "avg_comment_score" ,
            "total_achievements" ,
            "tf_idf_post_content" ,
            "tf_idf_comment" ,
            "subreddit_count" ,
            "comment_per_post" ,
            "karma_ratio",
            "avg_post_interval",
            "avg_comment_interval"]:
    spam = df[df["label"] == 1][col]
    not_spam = df[df["label"] == 0][col]
    stat, p = ttest_ind(spam, not_spam)
    print(col, "p-value:", p)
