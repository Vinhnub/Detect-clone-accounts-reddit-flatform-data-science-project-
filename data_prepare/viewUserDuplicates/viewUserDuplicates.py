import os
import sqlite3
import pandas as pd

folder_path = r"D:\FecthDataToSQL\dataReddit"
tables_order = ["r_user", "achievement", "user_achievement", "post", "comment"]
merged_data = {t: [] for t in tables_order}

# Đọc dữ liệu từ SQLite
for file in os.listdir(folder_path):
    if file.endswith(".db"):
        db_path = os.path.join(folder_path, file)
        conn = sqlite3.connect(db_path)
        for table in tables_order:
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                df["source_file"] = file
                merged_data[table].append(df)
            except:
                continue
        conn.close()

# Phân tích user trùng
if merged_data["r_user"]:
    all_users = pd.concat(merged_data["r_user"], ignore_index=True)
    total_users = len(all_users)
    unique_users = all_users["username"].nunique()
    duplicate_count = total_users - unique_users
    duplicate_percent = round(duplicate_count / total_users * 100, 2)

    print(f"Tổng user: {total_users}, duy nhất: {unique_users}, trùng: {duplicate_count} ({duplicate_percent}%)")
    dup_users = all_users["username"].value_counts()
    dup_users = dup_users[dup_users > 1]
    if not dup_users.empty:
        print("\nMột vài user trùng:")
        print(dup_users.head(100))
