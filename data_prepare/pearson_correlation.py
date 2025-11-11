import pandas as pd

data = pd.read_csv("data_prepare/data_training.csv")

numeric_cols = data.select_dtypes(include=['float64', 'int64'])

# tính ma trận tương quan
corr = numeric_cols.corr(method='pearson')

print(corr)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.imshow(corr)
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Pearson Correlation Heatmap")
plt.show()
