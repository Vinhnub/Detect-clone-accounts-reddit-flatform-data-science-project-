from database.database_fetcher import  DatabaseFetcher
import seaborn as sns
import matplotlib.pyplot as plt

oFetcher = DatabaseFetcher()
query = "SELECT * FROM r_user"
r_user = oFetcher.execute(query)
query = "SELECT username, score FROM post"
posts = oFetcher.execute(query)
query = "SELECT username, score FROM comment"
comments = oFetcher.execute(query)


post_score = posts.groupby("username")["score"].mean().reset_index(name="avg_post_score")
comment_score = comments.groupby("username")["score"].mean().reset_index(name="avg_comment_score")

df = (
    users.merge(post_score, on="username", how="left")
         .merge(comment_score, on="username", how="left")
)

df[["avg_post_score", "avg_comment_score"]] = df[["avg_post_score", "avg_comment_score"]].fillna(0)

sns.lmplot(data=df, x="link_karma", y="avg_post_score", height=5, aspect=1.3, scatter_kws={"alpha":0.6})
plt.title("Mối quan hệ giữa Link Karma và điểm Post trung bình")
plt.xlabel("Link Karma")
plt.ylabel("Điểm Post trung bình")

sns.lmplot(data=df, x="comment_karma", y="avg_comment_score", height=5, aspect=1.3, scatter_kws={"alpha":0.6})
plt.title("Mối quan hệ giữa Comment Karma và điểm Comment trung bình")
plt.xlabel("Comment Karma")
plt.ylabel("Điểm Comment trung bình")

plt.show()
