import pandas as pd
import random
import uuid

blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
conditions = ['thalassemia major', 'thalassemia minor']
severities = ['low', 'moderate', 'high']
needs = ['yes', 'no']

def generate_row():
    age = random.randint(5, 40)
    blood = random.choice(blood_groups)
    condition = random.choices(conditions, weights=[3, 2])[0]
    severity = random.choices(severities, weights=[3, 5, 2])[0]
    
    if condition == 'thalassemia major' and severity in ['moderate', 'high']:
        transfuse = 'yes'
    else:
        transfuse = random.choices(needs, weights=[3, 7])[0]

    return {
        "patient_id": str(uuid.uuid4())[:8],
        "age": age,
        "blood_group": blood,
        "condition": condition,
        "severity": severity,
        "transfusion_needed": transfuse
    }

data = [generate_row() for _ in range(1000)]
df = pd.DataFrame(data)
df.to_csv("patient_data.csv", index=False)
print("✅ Dataset saved as 'patient_data.csv'")
