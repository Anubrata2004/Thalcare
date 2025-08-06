from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model and encoders
model = joblib.load('thalassemia_model.pkl')
le_gender = joblib.load('le_gender.pkl')
le_family = joblib.load('le_family.pkl')
le_fatigue = joblib.load('le_fatigue.pkl')
le_anemia = joblib.load('le_anemia.pkl')
le_symptoms = joblib.load('le_symptoms.pkl')
le_risk = joblib.load('le_risk.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        gender_enc = le_gender.transform([data['gender']])[0]
        family_enc = le_family.transform([data['family_history']])[0]
        fatigue_enc = le_fatigue.transform([data['fatigue_level']])[0]
        anemia_enc = le_anemia.transform([data['anemia_level']])[0]
        symptoms_enc = le_symptoms.transform([data['symptoms']])[0]

        features = [
            data['age'],
            gender_enc,
            family_enc,
            fatigue_enc,
            anemia_enc,
            data['hemoglobin_level'],
            symptoms_enc
        ]

        features_arr = np.array(features).reshape(1, -1)
        pred_enc = model.predict(features_arr)[0]
        pred_label = le_risk.inverse_transform([pred_enc])[0]

        return jsonify({'risk_level': pred_label})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
