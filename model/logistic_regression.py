import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib

data = pd.read_csv("data_prepare/data_training.csv")

data = data.drop(columns=["username"])

y = data


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

joblib.dump(pipeline, 'reddit_spam_model_logistic_regression.pkl')
print("Model saved to reddit_spam_model_logistic_regression.pkl")

