import pandas as pd
import random
import uuid

blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
diseases = ['none', 'diabetes', 'hypertension', 'asthma', 'none']
locations = ['Kolkata', 'Delhi', 'Mumbai', 'Chennai', 'Bangalore']
availability = ['yes', 'no']

def generate_row():
    age = random.randint(18, 60)
    blood = random.choice(blood_groups)
    disease = random.choices(diseases, weights=[6, 1.5, 1.5, 1, 6])[0]
    last_donation = random.randint(1, 365)
    loc = random.choice(locations)
    
    if disease == 'none' and last_donation > 90:
        avail = 'yes'
    elif disease != 'none' and last_donation < 60:
        avail = 'no'
    else:
        avail = random.choice(availability)
    
    return {
        "donor_id": str(uuid.uuid4())[:8],
        "age": age,
        "blood_group": blood,
        "last_donation_days_ago": last_donation,
        "has_disease": disease,
        "location": loc,
        "available": avail
    }

data = [generate_row() for _ in range(1000)]
df = pd.DataFrame(data)
df.to_csv("donor_availability_data.csv", index=False)
print("✅ Dataset saved as 'donor_availability_data.csv'")
