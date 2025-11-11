import pandas as pd

def label_user(row):
    if (
        row["total_posts"] > 10 and
        row["comment_per_post"] < 0.3 and
        row["karma_ratio"] > 5 and
        row["subreddit_count"] > 10
    ):
        return 1

    if (
        row["total_posts"] > 20 and
        row["avg_post_score"] < 3 and
        row["link_karma"] < 20 and
        row["tf_idf_post_content"] > 0.2
    ):
        return 1

    if (
        row["total_comments"] > 30 and
        row["avg_comment_score"] < 3 and
        row["comment_karma"] < 20 and
        row["tf_idf_comment"] > 0.1
    ):
        return 1

    if (
        (0 < row["avg_post_interval"] and row["avg_post_interval"] < 1000 and row["total_posts"] > 50) or
        (0 < row["avg_comment_interval"] and row["avg_comment_interval"] < 1000 and row["total_comments"] > 50)
    ):
        return 1

    if row["tf_idf_comment"] > 0.2 or row["tf_idf_post_content"] > 0.3:
        return 1

    soft_score = 0
    soft_score += 1 if row["link_karma"] < 10 else 0
    soft_score += 1 if row["comment_karma"] < 10 else 0
    soft_score += 1 if row["verified_email"] == 0 else 0
    soft_score += 1 if row["link_karma"] < 10 and row["comment_karma"] > 100 else 0
    soft_score += 1 if row["link_karma"] > 100 and row["comment_karma"] < 10 else 0

    return 1 if soft_score >= 3 else 0

data = pd.read_csv("data_prepare/data_training.csv")
data["label"] = data.apply(label_user, axis=1)
data.to_csv("data_prepare/data_training.csv", index=False)