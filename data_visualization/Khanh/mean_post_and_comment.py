import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =================== Cấu hình SQL Server ===================
sql_server = r"LAPTOP-SUM9877U"
database_name = "RedditDB"

conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={sql_server};"
    f"DATABASE={database_name};"
    f"Trusted_Connection=yes;"
)

# =================== Hàm truy vấn ===================
def fetch_user_activity():
    """
    Truy vấn số lượng bài post, comment, link_karma và comment_karma cho mỗi người dùng.
    Loại bỏ người dùng bị xóa ([deleted]).
    """
    query = """
    WITH PostCounts AS (
        SELECT username, COUNT(id) AS num_posts
        FROM post
        GROUP BY username
    ),
    CommentCounts AS (
        SELECT username, COUNT(id) AS num_comments
        FROM comment
        GROUP BY username
    )
    SELECT 
        u.username,
        ISNULL(p.num_posts, 0) AS num_posts,
        ISNULL(c.num_comments, 0) AS num_comments,
        u.link_karma,
        u.comment_karma
    FROM r_user AS u
    LEFT JOIN PostCounts AS p ON u.username = p.username
    LEFT JOIN CommentCounts AS c ON u.username = c.username
    WHERE u.username != '[deleted]';
    """
    try:
        with pyodbc.connect(conn_str) as conn:
            df = pd.read_sql_query(query, conn)
        return df
    except pyodbc.Error as e:
        print(f"Lỗi khi kết nối hoặc truy vấn cơ sở dữ liệu: {e}")
        return None


# =================== Biểu đồ trung bình ===================
def plot_average_activity(df):
    """
    Vẽ biểu đồ cột thể hiện trung bình số lượng post và comment của tất cả người dùng.
    """
    if df is None or df.empty:
        print("Không có dữ liệu để trực quan hóa.")
        return

    # Tính trung bình
    avg_posts = df['num_posts'].mean()
    avg_comments = df['num_comments'].mean()

    avg_data = pd.DataFrame({
        'Hoạt động': ['Bài đăng (Posts)', 'Bình luận (Comments)'],
        'Trung bình': [avg_posts, avg_comments]
    })

    # Vẽ biểu đồ
    plt.figure(figsize=(6, 5))
    sns.barplot(x='Hoạt động', y='Trung bình', data=avg_data, palette=['skyblue', 'lightcoral'])

    # Hiển thị giá trị trung bình trên cột
    for index, value in enumerate(avg_data['Trung bình']):
        plt.text(index, value + 0.1, f"{value:.2f}", ha='center', fontsize=12, fontweight='bold')

    plt.title("Trung bình số lượng Post và Comment của người dùng", fontsize=14)
    plt.ylabel("Số lượng trung bình", fontsize=12)
    plt.xlabel("")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.show()


# =================== Main ===================
if __name__ == "__main__":
    df_activity = fetch_user_activity()
    plot_average_activity(df_activity)
