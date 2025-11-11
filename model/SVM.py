import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib

data = pd.read_csv("data_prepare/data_training.csv")

# Remove unneeded columns
data = data.drop(columns=["username"])

Y = data

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    data, y, test_size=0.2, random_state=42, stratify=y
)

smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)


pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', SVC(kernel='rbf', probability=True, class_weight='balanced', gamma="scale"))
])

pipeline.fit(X_train, y_train)

# Prediction & Evaluation
y_proba = pipeline.predict_proba(X_test)[:, 1]

threshold = 0.6     # You can tune threshold later
y_pred = (y_proba > threshold).astype(int)

print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))

# Save model
joblib.dump(pipeline, "reddit_spam_model_svm.pkl")
print("✅ Model saved as reddit_spam_model_svm.pkl")

