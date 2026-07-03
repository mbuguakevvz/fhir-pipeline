# src/transformer/csv_to_fhir.py
import pandas as pd
import json
import uuid
import os
import sys

def create_fhir_patient(row):
    return {
        "resourceType": "Patient",
        "id": row['patient_id'],
        "identifier": [{
            "system": "http://hospital.org/patient-id",
            "value": row['patient_id']
        }],
        "name": [{
            "use": "official",
            "family": row['last_name'],
            "given": [row['first_name']]
        }],
        "gender": row['gender'].lower(),
        "birthDate": row['dob']
    }

def create_fhir_condition(row, condition_name):
    mapping = {
        "Hypertension": "38341003",
        "Type 2 Diabetes": "44054006",
        "Hyperlipidemia": "55822004",
        "Asthma": "195967001",
        "Coronary Artery Disease": "53741008",
        "Cancer": "363346000"
    }
    snomed = mapping.get(condition_name, "160245001")
    
    return {
        "resourceType": "Condition",
        "id": f"cond-{str(uuid.uuid4())[:8]}",
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": snomed,
                "display": condition_name
            }]
        },
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }]
        }
    }

def create_fhir_observation(row, code, display, value, unit):
    return {
        "resourceType": "Observation",
        "id": f"obs-{code}-{row['patient_id']}",
        "status": "final",
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": code,
                "display": display
            }]
        },
        "valueQuantity": {
            "value": float(value) if pd.notna(value) else 0,
            "unit": unit,
            "system": "http://unitsofmeasure.org",
            "code": unit
        }
    }

def transform_to_fhir(input_file="data/raw/patients.csv", output_dir="data/transformed"):
    print(f"🔄 Transforming CSV to FHIR Resources...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("📖 Reading patient data...")
    df = pd.read_csv(input_file)
    print(f"✅ Read {len(df)} patients")
    
    patients = []
    conditions = []
    observations = []
    
    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"🔄 Processing {idx+1}/{len(df)}")
        
        patients.append(create_fhir_patient(row))
        
        # Fix: Check if conditions is not NaN and not 'None'
        conditions_str = row['conditions']
        if pd.notna(conditions_str) and conditions_str != 'None':
            for cond in str(conditions_str).split('|'):
                if cond and cond.strip():  # Make sure it's not empty
                    conditions.append(create_fhir_condition(row, cond.strip()))
        
        # Add observations with NaN check
        observations.append(create_fhir_observation(row, "2339-0", "Glucose", row['glucose_mgdl'], "mg/dL"))
        observations.append(create_fhir_observation(row, "8480-6", "Systolic BP", row['systolic_bp'], "mmHg"))
        observations.append(create_fhir_observation(row, "39156-5", "BMI", row['bmi'], "kg/m2"))
    
    print("💾 Saving FHIR resources...")
    
    with open(f"{output_dir}/patients.ndjson", 'w') as f:
        for p in patients:
            f.write(json.dumps(p) + '\n')
    
    with open(f"{output_dir}/conditions.ndjson", 'w') as f:
        for c in conditions:
            f.write(json.dumps(c) + '\n')
    
    with open(f"{output_dir}/observations.ndjson", 'w') as f:
        for o in observations:
            f.write(json.dumps(o) + '\n')
    
    print(f"✅ Complete! {len(patients)} patients, {len(conditions)} conditions, {len(observations)} observations")
    return patients, conditions, observations

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/raw/patients.csv"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/transformed"
    transform_to_fhir(input_file, output_dir)
