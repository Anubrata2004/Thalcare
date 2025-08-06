import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import joblib

# Add these metric imports
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
# Load data (make sure your CSV file is named like this and in the same folder)
df = pd.read_csv("donor_availability_data.csv")

# Drop donor_id (not useful)
df = df.drop(columns=['donor_id'])

# Encode categorical columns
le_blood = LabelEncoder()
df['blood_group_enc'] = le_blood.fit_transform(df['blood_group'])

le_disease = LabelEncoder()
df['has_disease_enc'] = le_disease.fit_transform(df['has_disease'])

le_location = LabelEncoder()
df['location_enc'] = le_location.fit_transform(df['location'])

# Encode target
df['available_enc'] = df['available'].map({'yes':1, 'no':0})

# Features and target
X = df[['age', 'blood_group_enc', 'last_donation_days_ago', 'has_disease_enc', 'location_enc']]
y = df['available_enc']

# Handle imbalance with SMOTE
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, max_depth=10, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "donor_availability_model.pkl")
joblib.dump(le_blood, "le_blood.pkl")
joblib.dump(le_disease, "le_disease.pkl")
joblib.dump(le_location, "le_location.pkl")

print("✅ Model and encoders saved")
y_pred = model.predict(X_test)

# Print classification report
print("Classification Report:\n", classification_report(y_test, y_pred))

# Print accuracy
acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy on test set: {acc * 100:.2f}%")

# Print confusion matrix
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))