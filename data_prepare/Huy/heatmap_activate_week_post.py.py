import pandas as pd
import pyodbc
import matplotlib
matplotlib.use('Agg')

sql_server = r"LAPTOP-SUM9877U"
database_name = "RedditDB"

conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={sql_server};"
    f"DATABASE={database_name};"
    f"Trusted_Connection=yes;"
)

with pyodbc.connect(conn_str) as conn:
    df = pd.read_sql("SELECT created FROM comment", conn)

    count_df = pd.read_sql("SELECT COUNT(*) AS total_comments FROM comment", conn)
    total = int(count_df["total_comments"][0])
    print("Tổng số comment:", total)

    df['created'] = pd.to_datetime(df['created'], errors='coerce', utc=True)
    df['created'] = df['created'].dt.tz_convert('Asia/Ho_Chi_Minh')
    df['day_of_week'] = df['created'].dt.dayofweek
    df['hour'] = df['created'].dt.hour



import matplotlib.pyplot as plt
import seaborn as sns

# Đếm số lượng comment theo ngày + giờ
activity = df.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)

# Vẽ heatmap
plt.figure(figsize=(12, 5))
sns.heatmap(activity, cmap="YlOrRd")

plt.title("Hoạt động theo thời gian trong tuần (Comment)", fontsize=14)
plt.xlabel("Giờ trong ngày")
plt.ylabel("Thứ trong tuần")
plt.yticks(
    ticks=[0, 1, 2, 3, 4, 5, 6],
    labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    rotation=0
)
#plt.show()
plt.savefig("heat_map_activate.png", dpi=300)
plt.close()