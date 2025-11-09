import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.database_fetcher import DatabaseFetcher
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import numpy as np
import re


custom_stop_words = list(ENGLISH_STOP_WORDS.union({
    'http', 'https', 'www', 'com', 'amp',
    'u', 'r', 'imgur', 'jpg', 'png', 'gif',
    'click', 'buy', 'join', 'discord', 'telegram', 'follow',
    'free', 'giveaway', 'offer', 'limited', 'subscribe'
}))

duplicate_ratio = {} # format username : {"post", "comment"}


def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()

oFetcher = DatabaseFetcher()
query = "SELECT RU.username, content FROM r_user RU INNER JOIN post P ON RU.username = P.username"
user_post_data = oFetcher.execute(query)
query = "SELECT RU.username, body FROM r_user RU INNER JOIN comment C ON RU.username = C.username"
user_comment_data = oFetcher.execute(query)

# check duplicate for post content
list_user = user_post_data['username'].tolist()
list_user = list(set(list_user))

count = 1
for user in list_user:
    if user not in duplicate_ratio: duplicate_ratio[user] = {}
    duplicate_ratio[user]["post"] = np.nan
    texts = user_post_data[user_post_data['username'] == user]['content'].tolist()
    texts = [clean_text(t) for t in texts if isinstance(t, str) and t.strip()]

    if not texts:
        print(f"User {user} has no valid posts.")
        dup_score = np.nan  
    else:
        try:
            vectorizer = TfidfVectorizer(stop_words=custom_stop_words, lowercase=True)
            tfidf_matrix = vectorizer.fit_transform(texts)

            if tfidf_matrix.shape[0] == 1:
                dup_score = 0
            else:
                sim = cosine_similarity(tfidf_matrix)
                np.fill_diagonal(sim, 0)  
                dup_score = sim.mean()
        except:
            dup_score = np.nan
    
    print(f"Number: {count} Duplicate content score for {user}: {dup_score}")
    duplicate_ratio[user]["post"] = dup_score 
    count += 1


# check duplicate for comment content
list_user = user_comment_data['username'].tolist()
list_user = list(set(list_user))

count = 1
for user in list_user:
    if user not in duplicate_ratio: duplicate_ratio[user] = {}
    duplicate_ratio[user]["comment"] = np.nan
    texts = user_comment_data[user_comment_data['username'] == user]['body'].tolist()
    texts = [clean_text(t) for t in texts if isinstance(t, str) and t.strip()]

    if not texts:
        print(f"User {user} has no valid comments.")
        dup_score = np.nan  
    else:
        try:
            vectorizer = TfidfVectorizer(stop_words=custom_stop_words, lowercase=True)
            tfidf_matrix = vectorizer.fit_transform(texts)

            if tfidf_matrix.shape[0] == 1:
                dup_score = 0
            else:
                sim = cosine_similarity(tfidf_matrix)
                np.fill_diagonal(sim, 0)  
                dup_score = sim.mean()
        except:
            dup_score = np.nan
    
    print(f"Number: {count} Duplicate content score for {user}: {dup_score}")
    duplicate_ratio[user]["comment"] = dup_score 
    count += 1

df_duplicate = pd.DataFrame(columns=['username', 'post', 'comment'])
df_duplicate = pd.DataFrame.from_dict(duplicate_ratio, orient='index').reset_index()
df_duplicate = df_duplicate.rename(columns={'index': 'username'})    
print(df_duplicate)
df_duplicate.to_csv("data_prepare/Vinh/duplicate_ratio.csv", index=False)
