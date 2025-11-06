import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Kết nối
conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=LAPTOP-SUM9877U;'
    'Database=RedditDB;'
    'Trusted_Connection=yes;'
)

# Lấy dữ liệu
query = "SELECT TOP 10000 username, link_karma, comment_karma FROM r_user"
df = pd.read_sql(query, conn)

# Giới hạn trục X
x_max = 1000

# ================ Histogram Link =================
plt.figure(figsize=(8,4))
sns.histplot(df['link_karma'], bins=100, binrange=(0, x_max))
plt.title("Histogram - Link Karma (đã loại bỏ outlier)")
plt.xlabel("Link Karma")
plt.ylabel("Số lượng user")
plt.xlim(0, x_max)
plt.show()

# ================ Histogram Comment ==============
plt.figure(figsize=(8,4))
sns.histplot(df['comment_karma'], bins=100, binrange=(0, x_max))
plt.title("Histogram - Comment Karma (đã loại bỏ outlier)")
plt.xlabel("Comment Karma")
plt.ylabel("Số lượng user")
plt.xlim(0, x_max)
plt.show()
