import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


data_path = r"C:\Code\github\exported_data\data_2025-10-17_16-02-05"  


r_user = pd.read_csv(os.path.join(data_path, "r_user.csv"))
achievement = pd.read_csv(os.path.join(data_path, "achievement.csv"))
user_achievement = pd.read_csv(os.path.join(data_path, "user_achievement.csv"))
post = pd.read_csv(os.path.join(data_path, "post.csv"))
comment = pd.read_csv(os.path.join(data_path, "comment.csv"))

print("Dữ liệu đã đọc xong!")
print("r_user:", r_user.shape)
print("achievement:", achievement.shape)
print("user_achievement:", user_achievement.shape)
print("post:", post.shape)
print("comment:", comment.shape)

# ------------------------------------------------------------
# ---Phân tích số lượng achievement mỗi user--
# ------------------------------------------------------------

# Đếm số lượng achievement theo username
achievement_count = (
    user_achievement.groupby("username")["achievement_name"]
    .count()
    .reset_index(name="achievement_count")
)

# Gộp với bảng r_user để phân tích thêm nếu cần
merged = achievement_count.merge(r_user, on="username", how="left")

# Histogram
plt.figure(figsize=(8, 5))
sns.histplot(merged["achievement_count"], bins=10, kde=True, color="skyblue")
plt.title("Phân phối số lượng achievement mỗi user", fontsize=13)
plt.xlabel("Số lượng achievement")
plt.ylabel("Số lượng user")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# --- Phân phối tỉ lệ post/comment của từng user ---
# ------------------------------------------------------------

# Đếm số lượng post và comment theo username
post_count = post.groupby("username")["id"].count().reset_index(name="post_count")
comment_count = comment.groupby("username")["id"].count().reset_index(name="comment_count")

# Gộp hai bảng
user_activity = pd.merge(post_count, comment_count, on="username", how="outer").fillna(0)

# Tính tỉ lệ post/comment
user_activity["ratio_post_comment"] = user_activity["post_count"] / (user_activity["comment_count"] + 1)

# Histogram tỉ lệ post/comment
plt.figure(figsize=(8, 5))
sns.histplot(user_activity["ratio_post_comment"], bins=30, color="orange", kde=True)
plt.title("Phân phối tỉ lệ Post/Comment của từng user", fontsize=13)
plt.xlabel("Tỉ lệ Post / Comment")
plt.ylabel("Số lượng user")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Violin plot
plt.figure(figsize=(8, 5))
sns.violinplot(y=user_activity["ratio_post_comment"], color="lightgreen")
plt.title("Phân phối (violin plot) tỉ lệ Post/Comment của user", fontsize=13)
plt.ylabel("Tỉ lệ Post/Comment")
plt.tight_layout()
plt.show()
