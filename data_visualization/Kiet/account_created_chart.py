import matplotlib.pyplot as plt
import pandas as pd
from database.database_fetcher import DatabaseFetcher
def plot_user_creation_trend():
    db = DatabaseFetcher()
    users = db.get_r_user_table()
    if 'created' not in users.columns:
        print("❌ Không tìm thấy cột 'created' trong bảng r_user.")
        return
    users['created'] = pd.to_datetime(users['created'], errors='coerce')
    users = users.dropna(subset=['created'])
    users['month_year'] = users['created'].dt.to_period('M')
    user_counts = users.groupby('month_year').size().reset_index(name='count')
    user_counts['month_year'] = user_counts['month_year'].dt.to_timestamp()
    plt.figure(figsize=(10, 5))
    plt.plot(user_counts['month_year'], user_counts['count'], marker='o', linestyle='-', color='steelblue')
    plt.title("Số lượng tài khoản tạo theo thời gian", fontsize=14, fontweight='bold')
    plt.xlabel("Thời gian (Tháng/Năm)")
    plt.ylabel("Số lượng tài khoản được tạo")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    plot_user_creation_trend()
