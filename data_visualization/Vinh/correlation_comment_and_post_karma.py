import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database.database_fetcher import DatabaseFetcher

oFetcher = DatabaseFetcher()
query = "SELECT * FROM r_user"
r_user = oFetcher.execute(query)
#print(r_user)

plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=r_user,
    x='link_karma',
    y='comment_karma',
    hue='verified_email', 
    alpha=0.7
)
plt.title("Relationship between comment karma and post karma")
plt.xlabel("Link Karma (Post)")
plt.ylabel("Comment Karma (Comment)")
plt.xscale('log')
plt.yscale('log')
plt.show()
