<<<<<<< HEAD:data_visualization/Trung/Lab.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess
from datetime import datetime
import shutil
import numpy as np


thu_muc_goc = r"C:\Code\github\exported_data"   
thu_muc_repo = r"C:\Code\github"                


all_r_user, all_achievement, all_user_achievement, all_post, all_comment = [], [], [], [], []

# ==============================================
# Đọc và gộp toàn bộ dataset
# ==============================================
for thu_muc_con in os.listdir(thu_muc_goc):
    duong_dan = os.path.join(thu_muc_goc, thu_muc_con)
    if not os.path.isdir(duong_dan):
        continue

    print(f" Đang gộp dữ liệu từ: {thu_muc_con}")

    try:
        r_user = pd.read_csv(os.path.join(duong_dan, "r_user.csv"))
        achievement = pd.read_csv(os.path.join(duong_dan, "achievement.csv"))
        user_achievement = pd.read_csv(os.path.join(duong_dan, "user_achievement.csv"))
        post = pd.read_csv(os.path.join(duong_dan, "post.csv"))
        comment = pd.read_csv(os.path.join(duong_dan, "comment.csv"))

        # Thêm cột tên dataset
        for df in [r_user, achievement, user_achievement, post, comment]:
            df["dataset_name"] = thu_muc_con

        all_r_user.append(r_user)
        all_achievement.append(achievement)
        all_user_achievement.append(user_achievement)
        all_post.append(post)
        all_comment.append(comment)

    except Exception as e:
        print(f" Lỗi khi đọc {thu_muc_con}: {e}")

# --- Gộp toàn bộ lại ---
r_user = pd.concat(all_r_user, ignore_index=True)
achievement = pd.concat(all_achievement, ignore_index=True)
user_achievement = pd.concat(all_user_achievement, ignore_index=True)
post = pd.concat(all_post, ignore_index=True)
comment = pd.concat(all_comment, ignore_index=True)

print("\n Đã gộp tất cả dữ liệu xong!")
print(f"r_user: {r_user.shape}")
print(f"achievement: {achievement.shape}")
print(f"user_achievement: {user_achievement.shape}")
print(f"post: {post.shape}")
print(f"comment: {comment.shape}")

# ==============================================
# Biểu đồ 1: Số lượng thành tựu của người dùng
# ==============================================
so_luong_thanh_tuu = (
    user_achievement.groupby("username")["achievement_name"]
    .count()
    .reset_index(name="so_luong_thanh_tuu")
)

mean_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].mean()
var_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].var()
min_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].min()
max_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].max()
mode_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].mode()[0]  # pandas mode

plt.figure(figsize=(8, 5))
sns.histplot(so_luong_thanh_tuu["so_luong_thanh_tuu"], bins=15, kde=True, color="steelblue")


plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Trung bình = {mean_val:.2f}')


plt.text(
    x=max_val*0.5,
    y=plt.ylim()[1]*1.2,
    s=f"Min = {min_val}\nMax = {max_val}\nMode = {mode_val}\nVar = {var_val:.2f}",
    bbox=dict(facecolor='white', alpha=0.5),
    fontsize=10
)

plt.title("User Achievement Count Distribution (Aggregate)")
plt.xlabel("Number of achievements")
plt.ylabel("Number of users")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

bieu_do_1 = os.path.join(thu_muc_repo, "bieu_do_phan_phoi_thanh_tuu.png")
plt.savefig(bieu_do_1)
plt.close()
print(f" Đã lưu biểu đồ: {bieu_do_1}")

# ==============================================
# Biểu đồ 2: Tỷ lệ Post/Comment
# ==============================================
dem_post = post.groupby("username")["id"].count().reset_index(name="so_post")
dem_comment = comment.groupby("username")["id"].count().reset_index(name="so_comment")
hoat_dong_user = pd.merge(dem_post, dem_comment, on="username", how="outer").fillna(0)
hoat_dong_user["ti_le_post_comment"] = hoat_dong_user["so_post"] / (hoat_dong_user["so_comment"] + 1)

mean_ratio = hoat_dong_user["ti_le_post_comment"].mean()
var_ratio = hoat_dong_user["ti_le_post_comment"].var()
min_ratio = hoat_dong_user["ti_le_post_comment"].min()
max_ratio = hoat_dong_user["ti_le_post_comment"].max()
mode_ratio = hoat_dong_user["ti_le_post_comment"].mode()[0]  

plt.figure(figsize=(8, 5))
sns.histplot(hoat_dong_user["ti_le_post_comment"], bins=30, kde=True, color="orange")


plt.axvline(mean_ratio, color='red', linestyle='--', linewidth=2, label=f'Trung bình = {mean_ratio:.2f}')


plt.text(
    x=max_ratio*0.5,
    y=plt.ylim()[1]*1.2,
    s=f"Min = {min_ratio:.2f}\nMax = {max_ratio:.2f}\nMode = {mode_ratio:.2f}\nVar = {var_ratio:.2f}",
    bbox=dict(facecolor='white', alpha=0.5),
    fontsize=10
)

plt.title("User Post/Comment Ratio Distribution (Aggregate)")
plt.xlabel("Post/Comment Ratio")
plt.ylabel("Number of users")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

bieu_do_2 = os.path.join(thu_muc_repo, "bieu_do_ti_le_post_comment.png")
plt.savefig(bieu_do_2)
plt.close()
print(f" Đã lưu biểu đồ: {bieu_do_2}")








# ==============================================
# COMMIT + PUSH GITHUB
# ==============================================
try:
    os.chdir(thu_muc_repo)
    
    
    git_cmd = shutil.which("git")
    if git_cmd is None:
        
        git_cmd = r"C:\Program Files\Git\bin\git.exe"
        if not os.path.exists(git_cmd):
            raise FileNotFoundError("Không tìm thấy git.exe — vui lòng kiểm tra lại cài đặt Git!")

    subprocess.run([git_cmd, "add", "."], check=True)
    thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Cập nhật 2 biểu đồ tổng hợp dữ liệu ({thoi_gian})"
    subprocess.run([git_cmd, "commit", "-m", commit_msg], check=True)
    subprocess.run([git_cmd, "push"], check=True)
    print("\n Đã commit và push thành công lên GitHub!")

except Exception as e:
    print(f" Lỗi khi commit/push: {e}")
=======
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess
from datetime import datetime
import shutil
import numpy as np


thu_muc_goc = r"C:\Code\github\exported_data"   
thu_muc_repo = r"C:\Code\github"                


all_r_user, all_achievement, all_user_achievement, all_post, all_comment = [], [], [], [], []

# ==============================================
# Đọc và gộp toàn bộ dataset
# ==============================================
for thu_muc_con in os.listdir(thu_muc_goc):
    duong_dan = os.path.join(thu_muc_goc, thu_muc_con)
    if not os.path.isdir(duong_dan):
        continue

    print(f" Đang gộp dữ liệu từ: {thu_muc_con}")

    try:
        r_user = pd.read_csv(os.path.join(duong_dan, "r_user.csv"))
        achievement = pd.read_csv(os.path.join(duong_dan, "achievement.csv"))
        user_achievement = pd.read_csv(os.path.join(duong_dan, "user_achievement.csv"))
        post = pd.read_csv(os.path.join(duong_dan, "post.csv"))
        comment = pd.read_csv(os.path.join(duong_dan, "comment.csv"))

        # Thêm cột tên dataset
        for df in [r_user, achievement, user_achievement, post, comment]:
            df["dataset_name"] = thu_muc_con

        all_r_user.append(r_user)
        all_achievement.append(achievement)
        all_user_achievement.append(user_achievement)
        all_post.append(post)
        all_comment.append(comment)

    except Exception as e:
        print(f" Lỗi khi đọc {thu_muc_con}: {e}")

# --- Gộp toàn bộ lại ---
r_user = pd.concat(all_r_user, ignore_index=True)
achievement = pd.concat(all_achievement, ignore_index=True)
user_achievement = pd.concat(all_user_achievement, ignore_index=True)
post = pd.concat(all_post, ignore_index=True)
comment = pd.concat(all_comment, ignore_index=True)

print("\n Đã gộp tất cả dữ liệu xong!")
print(f"r_user: {r_user.shape}")
print(f"achievement: {achievement.shape}")
print(f"user_achievement: {user_achievement.shape}")
print(f"post: {post.shape}")
print(f"comment: {comment.shape}")

# ==============================================
# Biểu đồ 1: Số lượng thành tựu của người dùng
# ==============================================
so_luong_thanh_tuu = (
    user_achievement.groupby("username")["achievement_name"]
    .count()
    .reset_index(name="so_luong_thanh_tuu")
)

mean_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].mean()
var_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].var()
min_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].min()
max_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].max()
mode_val = so_luong_thanh_tuu["so_luong_thanh_tuu"].mode()[0]  # pandas mode

plt.figure(figsize=(8, 5))
sns.histplot(so_luong_thanh_tuu["so_luong_thanh_tuu"], bins=15, kde=True, color="steelblue")


plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Trung bình = {mean_val:.2f}')


plt.text(
    x=max_val*0.5,
    y=plt.ylim()[1]*1.2,
    s=f"Min = {min_val}\nMax = {max_val}\nMode = {mode_val}\nVar = {var_val:.2f}",
    bbox=dict(facecolor='white', alpha=0.5),
    fontsize=10
)

plt.title("User Achievement Count Distribution (Aggregate)")
plt.xlabel("Number of achievements")
plt.ylabel("Number of users")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

bieu_do_1 = os.path.join(thu_muc_repo, "bieu_do_phan_phoi_thanh_tuu.png")
plt.savefig(bieu_do_1)
plt.close()
print(f" Đã lưu biểu đồ: {bieu_do_1}")

# ==============================================
# Biểu đồ 2: Tỷ lệ Post/Comment
# ==============================================
dem_post = post.groupby("username")["id"].count().reset_index(name="so_post")
dem_comment = comment.groupby("username")["id"].count().reset_index(name="so_comment")
hoat_dong_user = pd.merge(dem_post, dem_comment, on="username", how="outer").fillna(0)
hoat_dong_user["ti_le_post_comment"] = hoat_dong_user["so_post"] / (hoat_dong_user["so_comment"] + 1)

mean_ratio = hoat_dong_user["ti_le_post_comment"].mean()
var_ratio = hoat_dong_user["ti_le_post_comment"].var()
min_ratio = hoat_dong_user["ti_le_post_comment"].min()
max_ratio = hoat_dong_user["ti_le_post_comment"].max()
mode_ratio = hoat_dong_user["ti_le_post_comment"].mode()[0]  

plt.figure(figsize=(8, 5))
sns.histplot(hoat_dong_user["ti_le_post_comment"], bins=50, kde=True, color="orange")


plt.axvline(mean_ratio, color='red', linestyle='--', linewidth=2, label=f'Trung bình = {mean_ratio:.2f}')


plt.text(
    x=max_ratio*0.5,
    y=plt.ylim()[1]*1.2,
    s=f"Min = {min_ratio:.2f}\nMax = {max_ratio:.2f}\nMode = {mode_ratio:.2f}\nVar = {var_ratio:.2f}",
    bbox=dict(facecolor='white', alpha=0.5),
    fontsize=10
)

plt.title("User Post/Comment Ratio Distribution (Aggregate)")
plt.xlabel("Post/Comment Ratio")
plt.ylabel("Number of users")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

bieu_do_2 = os.path.join(thu_muc_repo, "bieu_do_ti_le_post_comment.png")
plt.savefig(bieu_do_2)
plt.close()
print(f" Đã lưu biểu đồ: {bieu_do_2}")








# ==============================================
# COMMIT + PUSH GITHUB
# ==============================================
# try:
#     os.chdir(thu_muc_repo)
    
    
#     git_cmd = shutil.which("git")
#     if git_cmd is None:
        
#         git_cmd = r"C:\Program Files\Git\bin\git.exe"
#         if not os.path.exists(git_cmd):
#             raise FileNotFoundError("Không tìm thấy git.exe — vui lòng kiểm tra lại cài đặt Git!")

#     subprocess.run([git_cmd, "add", "."], check=True)
#     thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     commit_msg = f"Cập nhật 2 biểu đồ tổng hợp dữ liệu ({thoi_gian})"
#     subprocess.run([git_cmd, "commit", "-m", commit_msg], check=True)
#     subprocess.run([git_cmd, "push"], check=True)
#     print("\n Đã commit và push thành công lên GitHub!")

# except Exception as e:
#     print(f" Lỗi khi commit/push: {e}")
>>>>>>> bb7c47859f3596ebb319ef2660cebfa2aef23061:data_prepare/Trung/Lab.py
