# format: link_karma, comment_karma, verified_email, totol_posts, totol_comments, avg_post_score, avg_comment_score
# total_achievements, tf_idf_post_content, tf_idf_comment, subreddit_count

from database.database_fetcher import DatabaseFetcher
import pandas as pd
import numpy as np

oDatabase = DatabaseFetcher()

users = oDatabase.get_r_user