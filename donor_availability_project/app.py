from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model and encoders
model = joblib.load('donor_availability_model.pkl')
le_blood = joblib.load('le_blood.pkl')
le_disease = joblib.load('le_disease.pkl')
le_location = joblib.load('le_location.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    try:
        blood_enc = le_blood.transform([data['blood_group']])[0]
        disease_enc = le_disease.transform([data['has_disease']])[0]
        location_enc = le_location.transform([data['location']])[0]

        features = [
            data['age'],
            blood_enc,
            data['last_donation_days_ago'],
            disease_enc,
            location_enc
        ]

        features_arr = np.array(features).reshape(1, -1)
        pred = model.predict(features_arr)[0]

        return jsonify({'available': int(pred)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
