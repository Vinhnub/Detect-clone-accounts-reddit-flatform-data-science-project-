import matplotlib.pyplot as plt
import pandas as pd
from database.database_fetcher import DatabaseFetcher

def plot_verified_premium_ratio(save_fig=True):
    db = DatabaseFetcher()
    users = db.get_r_user_table()
    required_cols = ['verified_email', 'premium']
    for col in required_cols:
        if col not in users.columns:
            print(f"❌ Không tìm thấy cột '{col}' trong bảng r_user.")
            return
    users['verified_email'] = users['verified_email'].astype(int)
    users['premium'] = users['premium'].astype(int)
    verified_counts = users['verified_email'].value_counts().reindex([1, 0], fill_value=0)
    verified_labels = ['Đã xác thực email', 'Chưa xác thực email']
    verified_perc = verified_counts / verified_counts.sum() * 100
    premium_counts = users['premium'].value_counts().reindex([1, 0], fill_value=0)
    premium_labels = ['Có Premium', 'Không có Premium']
    premium_perc = premium_counts / premium_counts.sum() * 100
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].pie(
        verified_counts,
        labels=[f"{l} ({p:.1f}%)" for l, p in zip(verified_labels, verified_perc)],
        autopct=None,
        colors=['#4CAF50', '#FF7043'],
        startangle=90
    )
    axes[0].set_title("Tỷ lệ tài khoản xác thực email", fontsize=12, fontweight='bold')
    axes[1].pie(
        premium_counts,
        labels=[f"{l} ({p:.1f}%)" for l, p in zip(premium_labels, premium_perc)],
        autopct=None,
        colors=['#2196F3', '#9E9E9E'],
        startangle=90
    )
    axes[1].set_title("Tỷ lệ tài khoản Premium", fontsize=12, fontweight='bold')

    plt.tight_layout()
    # if save_fig:
    #     plt.savefig("verified_premium_ratio.png", dpi=300)
    #     print("💾 Đã lưu biểu đồ thành file: verified_premium_ratio.png")
    plt.show()
if __name__ == "__main__":
    plot_verified_premium_ratio()
