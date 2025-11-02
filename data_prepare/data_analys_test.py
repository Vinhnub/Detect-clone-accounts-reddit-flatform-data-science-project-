import pandas as pd
from database.database_fetcher import DatabaseFetcher
import matplotlib.pyplot as plt

pd.set_option('display.float_format', '{:.0f}'.format)
o_database = DatabaseFetcher()

user_table = o_database.get_r_user_table()
comment_table = o_database.get_comment_table()
post_table = o_database.get_post_table()

user_karma = user_table[["link_karma", "comment_karma"]]
comment_score = comment_table[["score"]]
post_score = post_table[["score"]]

print(user_karma.describe())
print(comment_score.describe())
print(post_score.describe())

user_karma.hist(bins=10, figsize=(8,4))
comment_score.hist(bins=10, figsize=(8,4))
post_score.hist(bins=10, figsize=(8,4))
plt.show()