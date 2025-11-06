import matplotlib.pyplot as plt
import pandas as pd

df_duplicate = pd.read_csv("data_prepare/Vinh/duplicate_score.csv")

plt.figure(figsize=(8,6))
plt.hist(df_duplicate['post'], bins=1000, alpha=0.6, label='Post')
plt.xlabel('Tỉ lệ trùng lặp')
plt.ylabel('Số lượng user')
plt.title('Phân phối tỉ lệ trùng lặp của user')
plt.ylim(0, 150)
plt.legend()
plt.show