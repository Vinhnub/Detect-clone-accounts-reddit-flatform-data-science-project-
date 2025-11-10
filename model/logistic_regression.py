import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib

data = pd.read_csv("data_prepare/data_training.csv")

data = data.drop(columns=["username"])

def label_user(row):
    if (
        row["total_posts"] > 10 and
        row["comment_per_post"] < 0.3 and
        row["karma_ratio"] > 5 and
        row["subreddit_count"] > 10
    ):
        return 1  # Spam user

    # if (
    #     row["total_posts"] > 20 and
    #     row["avg_post_score"] < 3 and
    #     row["link_karma"] < 20 and
    #     row["tf_idf_post_content"] > 0.2
    # ):
    #     return 1
    #
    # if (
    #     row["total_comments"] > 30 and
    #     row["avg_comment_score"] < 3 and
    #     row["comment_karma"] < 20 and
    #     row["tf_idf_comment"] > 0.1
    # ):
    #     return 1

    if row["tf_idf_comment"] > 0.2 or row["tf_idf_post_content"] > 0.3:
        return 1  # Spam user

    soft_score = 0
    soft_score += 1 if row["link_karma"] < 10 else 0
    soft_score += 1 if row["comment_karma"] < 10 else 0
    soft_score += 1 if row["verified_email"] == 0 else 0

    if soft_score >= 2:
        return 1  # Spam user

    return 0


y = data.apply(label_user, axis=1)


X_train, X_test, y_train, y_test = train_test_split(
    data, y, test_size=0.2, random_state=42, stratify=y
)

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)


pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(solver='lbfgs', max_iter=1000, class_weight='balanced'))
])

pipeline.fit(X_train, y_train)


y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:,1]

threshold = 0.6
y_pred = (y_proba > threshold).astype(int)

print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))

joblib.dump(pipeline, 'reddit_spam_model.pkl')
print("Model saved to reddit_spam_model.pkl")

# Giả lập user mới
# X_new = pd.DataFrame([{
#             "link_karma": 23168,
#             "comment_karma": 216,
#             "verified_email": 0,
#             "total_posts" : 10618,
#             "total_comments" : 11159,
#             "avg_post_score" : 1.0456771520060275,
#             "avg_comment_score" : 1.0000896137646742,
#             "total_achievements" : 0,
#             "tf_idf_post_content" : 0.9999058203051424,
#             "tf_idf_comment" : 0.9999058203051424,
#             "subreddit_count" : 1,
#             "comment_per_post" : 1.0509512149180638,
#             "karma_ratio" : 107.25925925925924
#         }])
#
# spam_prob = pipeline.predict_proba(X_new)[:,1]
# spam_label = pipeline.predict(X_new)
#
# print("Spam probability:", spam_prob)
# print("Spam label:", spam_label)
