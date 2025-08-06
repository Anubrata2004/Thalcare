from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load('transfusion_model_xgb.pkl')

# Prepare LabelEncoders for categorical variables
blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
conditions = ['thalassemia minor', 'thalassemia major']
severities = ['low', 'moderate', 'high']

le_blood = LabelEncoder()
le_blood.fit(blood_groups)

le_condition = LabelEncoder()
le_condition.fit(conditions)

le_severity = LabelEncoder()
le_severity.fit(severities)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        blood_enc = le_blood.transform([data['blood_group']])[0]
        condition_enc = le_condition.transform([data['condition']])[0]
        severity_enc = le_severity.transform([data['severity']])[0]

        features = [
            data['age'],
            blood_enc,
            condition_enc,
            severity_enc
        ]

        features_arr = np.array(features).reshape(1, -1)
        pred = model.predict(features_arr)[0]
        pred_label = 'yes' if pred == 1 else 'no'

        return jsonify({'transfusion_needed': pred_label})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
