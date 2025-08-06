import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib

# Load dataset
df = pd.read_csv("thalassemia_risk_data.csv")

# Drop patient_id
df = df.drop(columns=['patient_id'])

# Encode categorical columns
le_gender = LabelEncoder()
df['gender_enc'] = le_gender.fit_transform(df['gender'])

le_family = LabelEncoder()
df['family_history_enc'] = le_family.fit_transform(df['family_history'])

le_fatigue = LabelEncoder()
df['fatigue_level_enc'] = le_fatigue.fit_transform(df['fatigue_level'])

le_anemia = LabelEncoder()
df['anemia_level_enc'] = le_anemia.fit_transform(df['anemia_level'])

le_symptoms = LabelEncoder()
df['symptoms_enc'] = le_symptoms.fit_transform(df['symptoms'])

le_risk = LabelEncoder()
df['risk_level_enc'] = le_risk.fit_transform(df['risk_level'])  # target

# Features and target
X = df[['age', 'gender_enc', 'family_history_enc', 'fatigue_level_enc',
        'anemia_level_enc', 'hemoglobin_level', 'symptoms_enc']]
y = df['risk_level_enc']

# Handle imbalance using SMOTE
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res,
                                                    test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=200, max_depth=10,
                               class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = model.predict(X_test)

print("Classification Report:\n", classification_report(y_test, y_pred))
print(f"Model Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save model and encoders
joblib.dump(model, "thalassemia_model.pkl")
joblib.dump(le_gender, "le_gender.pkl")
joblib.dump(le_family, "le_family.pkl")
joblib.dump(le_fatigue, "le_fatigue.pkl")
joblib.dump(le_anemia, "le_anemia.pkl")
joblib.dump(le_symptoms, "le_symptoms.pkl")
joblib.dump(le_risk, "le_risk.pkl")

print("✅ Model and encoders saved")
