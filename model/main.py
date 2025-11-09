# ===============================
# reddit_spam_train.py
# ===============================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib
from datetime import datetime

# -------------------------------
# 1. Chuẩn bị dữ liệu giả lập
# -------------------------------
# Giả lập dữ liệu user + post + comment
data = {
    "username": ["user1", "user2", "user3", "user4", "user5"],
    "link_karma": [5, 150, 20, 0, 200],
    "comment_karma": [2, 300, 15, 1, 100],
    "created": ["2025-11-01", "2020-01-01", "2025-10-28", "2025-11-03", "2019-05-05"],
    "premium": [0,1,0,0,1],
    "verified_email": [0,1,1,0,1],
    "total_posts": [15, 30, 5, 20, 50],
    "total_comments": [10, 50, 8, 15, 60],
    "total_achievements": [0, 10, 1, 0, 15],
    "avg_post_score": [0, 50, 1, 0, 60],
    "avg_comment_score": [0, 40, 0, 0, 30]
}

df = pd.DataFrame(data)

# Tạo feature account_age_days
df["created"] = pd.to_datetime(df["created"])
df["account_age_days"] = (pd.Timestamp("2025-11-06") - df["created"]).dt.days

# Drop username/created để dùng làm feature
X = df.drop(columns=["username","created"])

# -------------------------------
# 2. Gắn nhãn rule-based
# -------------------------------
def label_user(row):
    if (row['link_karma'] + row['comment_karma'] < 20 and
        row['account_age_days'] < 7 and
        row['total_posts'] + row['total_comments'] > 10):
        return 1  # spam
    else:
        return 0  # not spam

y = X.apply(label_user, axis=1)

# -------------------------------
# 3. Chia dữ liệu train/test
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# -------------------------------
# 4. Tạo pipeline Logistic Regression
# -------------------------------
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(solver='lbfgs', max_iter=1000, class_weight='balanced'))
])

pipeline.fit(X_train, y_train)

# -------------------------------
# 5. Đánh giá model
# -------------------------------
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:,1]

print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))

# -------------------------------
# 6. Lưu model
# -------------------------------
joblib.dump(pipeline, 'reddit_spam_model.pkl')
print("Model saved to reddit_spam_model.pkl")

# -------------------------------
# 7. Dự đoán với user mới (ví dụ)
# -------------------------------
# Giả lập user mới
X_new = pd.DataFrame([{
    "link_karma": 3,
    "comment_karma": 1,
    "premium": 0,
    "verified_email": 0,
    "total_posts": 12,
    "total_comments": 8,
    "total_achievements": 0,
    "avg_post_score": 0,
    "avg_comment_score": 0,
    "account_age_days": 5
}])

spam_prob = pipeline.predict_proba(X_new)[:,1]
spam_label = pipeline.predict(X_new)

print("Spam probability:", spam_prob)
print("Spam label:", spam_label)
