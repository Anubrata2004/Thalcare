import pandas as pd
import random
import uuid

genders = ['male', 'female']
family_history = ['yes', 'no']
fatigue_levels = ['low', 'moderate', 'high']
anemia_levels = ['none', 'mild', 'severe']
symptoms_list = ['none', 'jaundice', 'pale_skin', 'bone_deformities', 'delayed_growth']
risk_levels = ['low', 'moderate', 'high']

def generate_row():
    age = random.randint(1, 40)
    gender = random.choice(genders)
    family = random.choice(family_history)
    fatigue = random.choices(fatigue_levels, weights=[3, 4, 3])[0]
    anemia = random.choices(anemia_levels, weights=[2, 4, 4])[0]
    hb_level = round(random.uniform(6.0, 15.0), 1)
    symptoms = random.choice(symptoms_list)
    
    if family == 'yes' and anemia == 'severe' and hb_level < 9.0:
        risk = 'high'
    elif fatigue == 'high' or anemia == 'mild':
        risk = 'moderate'
    else:
        risk = random.choices(risk_levels, weights=[6, 3, 1])[0]
    
    return {
        "patient_id": str(uuid.uuid4())[:8],
        "age": age,
        "gender": gender,
        "family_history": family,
        "fatigue_level": fatigue,
        "anemia_level": anemia,
        "hemoglobin_level": hb_level,
        "symptoms": symptoms,
        "risk_level": risk
    }

data = [generate_row() for _ in range(1000)]
df = pd.DataFrame(data)
df.to_csv("thalassemia_risk_data.csv", index=False)
print("✅ Dataset saved as 'thalassemia_risk_data.csv'")