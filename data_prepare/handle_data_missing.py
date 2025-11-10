import pandas as pd

data = pd.read_csv("data_prepare/data_training.csv")

data = data[(data["total_posts"] > 0) & (data["total_comments"] > 0)]

data = data.fillna(0)

print(data)

data.to_csv("data_prepare/data_training.csv", index=False)

