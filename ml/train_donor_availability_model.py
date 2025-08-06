import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib

# Load dataset
df = pd.read_csv("donor_availability_data.csv")

# Encode categorical columns
le = LabelEncoder()
for col in ['blood_group', 'has_disease', 'location']:
    df[col] = le.fit_transform(df[col])

# Target encoding
df['available'] = df['available'].map({'yes': 1, 'no': 0})

# Features and target
X = df[['age', 'blood_group', 'last_donation_days_ago', 'has_disease', 'location']]
y = df['available']

# Apply SMOTE to handle imbalance
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=200, max_depth=10, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save the model
joblib.dump(model, "donor_availability_model.pkl")
print("✅ Model saved as 'donor_availability_model.pkl'")

