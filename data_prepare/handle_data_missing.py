import pandas as pd

data = pd.read_csv("data_prepare/data_training.csv")

data = data.fillna(0)

print(data)

data.to_csv("data_prepare/data_training.csv", index=False)

