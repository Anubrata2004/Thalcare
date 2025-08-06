import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import joblib

# Load dataset
df = pd.read_csv("patient_data.csv")

# Encode categorical columns
le = LabelEncoder()
for col in ['blood_group', 'condition', 'severity']:
    df[col] = le.fit_transform(df[col])

# Features and target
X = df[['age', 'blood_group', 'condition', 'severity']]
y = df['transfusion_needed'].map({'yes': 1, 'no': 0})

# Handle imbalance
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# XGBoost model
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    objective='binary:logistic',
    eval_metric='logloss',
    use_label_encoder=False,
    random_state=42
)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("✅ Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save model
joblib.dump(model, "transfusion_model_xgb.pkl")
print("\n✅ XGBoost model saved as 'transfusion_model_xgb.pkl'")



