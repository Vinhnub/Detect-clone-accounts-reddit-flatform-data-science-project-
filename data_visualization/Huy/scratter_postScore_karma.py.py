import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

sql_server = r"LAPTOP-SUM9877U"
database_name = "RedditDB"

conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={sql_server};"
    f"DATABASE={database_name};"
    f"Trusted_Connection=yes;"
)

with pyodbc.connect(conn_str) as conn:
    query = """
    SELECT 
        p.score,
        u.link_karma
    FROM post AS p
    JOIN r_user AS u
        ON p.username = u.username
    WHERE p.score IS NOT NULL AND u.link_karma IS NOT NULL
    """
    df = pd.read_sql(query, conn)

df = df.dropna(subset=['score', 'link_karma'])

df = df[(df['score'] < df['score'].quantile(0.99)) & 
        (df['link_karma'] < df['link_karma'].quantile(0.99))]

df_sample = df.sample(min(1_700_000, len(df)), random_state=42)

df_sample['log_link_karma'] = np.log1p(df_sample['link_karma'])

x_jitter = df_sample['log_link_karma'] + np.random.uniform(-0.01, 0.01, size=len(df_sample))

plt.figure(figsize=(12,6))
plt.scatter(x_jitter, df_sample['score'], alpha=0.3, s=10)
plt.title("Score của Post rải theo Link Karma người đăng (log scale)", fontsize=14)
plt.xlabel("Link Karma (log scale)")
plt.ylabel("Score của Post")
plt.grid(True)

# --- Chọn tick dễ nhìn ---
friendly_ticks = [0, 10, 50, 100, 500, 1000, 5000]
plt.xticks(np.log1p(friendly_ticks), labels=friendly_ticks)

plt.tight_layout()
plt.savefig("scatter_post_link_karma.png", dpi=300)
plt.close()
