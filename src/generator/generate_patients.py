# src/generator/generate_patients.py
import pandas as pd
from faker import Faker
import random
from datetime import datetime
import os

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_patient(patient_id):
    gender = random.choice(['Male', 'Female'])
    first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    
    conditions = []
    if random.random() < 0.3:
        conditions.append('Hypertension')
    if random.random() < 0.25:
        conditions.append('Type 2 Diabetes')
    if random.random() < 0.15:
        conditions.append('Hyperlipidemia')
    if random.random() < 0.10:
        conditions.append('Asthma')
    if random.random() < 0.05:
        conditions.append('Coronary Artery Disease')
    if random.random() < 0.02:
        conditions.append('Cancer')
    if not conditions:
        conditions = ['None']
    
    return {
        'patient_id': f"P{patient_id:07d}",
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'dob': dob.strftime('%Y-%m-%d'),
        'age': (datetime.now().date() - dob).days // 365,
        'race': random.choice(['White', 'Black', 'Asian', 'Hispanic', 'Other']),
        'conditions': '|'.join(conditions),
        'num_encounters': random.randint(1, 5),
        'glucose_mgdl': random.randint(70, 180),
        'systolic_bp': random.randint(100, 160),
        'diastolic_bp': random.randint(60, 100),
        'cholesterol_mgdl': random.randint(130, 280),
        'bmi': round(random.uniform(18.5, 40.0), 1),
        'is_smoker': random.random() < 0.2,
        'has_hypertension': 'Hypertension' in conditions,
        'has_diabetes': 'Type 2 Diabetes' in conditions,
    }

def generate_data(count=1000, output_file="data/raw/patients.csv"):
    print(f"👤 Generating {count} synthetic patients...")
    patients = [generate_patient(i) for i in range(1, count + 1)]
    df = pd.DataFrame(patients)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Generated {len(df)} patients to {output_file}")
    return df

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    output = sys.argv[2] if len(sys.argv) > 2 else "data/raw/patients.csv"
    generate_data(count, output)
