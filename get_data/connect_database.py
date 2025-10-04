import pandas as pd
import pyodbc

# Kết nối
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"       # hoặc "TENMAYCHU\SQLEXPRESS"
    "DATABASE=TenDatabase;"
    "UID=sa;"
    "PWD=vinh1255;"
)

# Đọc dữ liệu
query = "SELECT TOP 10 * FROM TenBang"
df = pd.read_sql(query, conn)

print(df.head())

conn.close()
