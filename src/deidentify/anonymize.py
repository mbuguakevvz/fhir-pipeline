# src/deidentify/anonymize.py
import json
import hashlib
import random
from datetime import datetime, timedelta
import os
import sys

def anonymize_patient(patient_data):
    """Apply HIPAA-compliant de-identification"""
    
    # Hash patient ID (irreversible)
    patient_id = patient_data['id']
    hashed_id = hashlib.sha256(patient_id.encode()).hexdigest()[:10]
    patient_data['id'] = f"ANON-{hashed_id}"
    
    # Update references
    if 'identifier' in patient_data:
        for ident in patient_data['identifier']:
            ident['value'] = f"ANON-{hashed_id}"
    
    # Shift birth date by random days (1-365)
    if 'birthDate' in patient_data:
        original_date = datetime.strptime(patient_data['birthDate'], '%Y-%m-%d')
        shift_days = random.randint(-365, 365)
        new_date = original_date + timedelta(days=shift_days)
        patient_data['birthDate'] = new_date.strftime('%Y-%m-%d')
    
    # Remove specific name details (keep first initial only)
    if 'name' in patient_data:
        for name in patient_data['name']:
            if 'given' in name and name['given']:
                name['given'] = [name['given'][0][0] + '.']
            if 'family' in name:
                name['family'] = name['family'][0] + '***'
    
    return patient_data

def anonymize_condition(condition_data, id_mapping):
    """Update condition references"""
    if 'subject' in condition_data and 'reference' in condition_data['subject']:
        old_id = condition_data['subject']['reference'].replace('Patient/', '')
        if old_id in id_mapping:
            condition_data['subject']['reference'] = f"Patient/{id_mapping[old_id]}"
    return condition_data

def anonymize_observation(observation_data, id_mapping):
    """Update observation references"""
    if 'subject' in observation_data and 'reference' in observation_data['subject']:
        old_id = observation_data['subject']['reference'].replace('Patient/', '')
        if old_id in id_mapping:
            observation_data['subject']['reference'] = f"Patient/{id_mapping[old_id]}"
    
    # Anonymize observation ID
    if 'id' in observation_data:
        old_id = observation_data['id']
        hashed = hashlib.sha256(old_id.encode()).hexdigest()[:8]
        observation_data['id'] = f"obs-{hashed}"
    
    return observation_data

def anonymize_dataset(input_dir="data/transformed", output_dir="data/anonymized"):
    """Anonymize all FHIR resources"""
    
    print("🔒 Applying de-identification...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load patients
    with open(f"{input_dir}/patients.ndjson", 'r') as f:
        patients = [json.loads(line) for line in f]
    
    # Create ID mapping
    id_mapping = {}
    anonymized_patients = []
    
    for patient in patients:
        old_id = patient['id']
        anonymized = anonymize_patient(patient)
        new_id = anonymized['id']
        id_mapping[old_id] = new_id
        anonymized_patients.append(anonymized)
    
    # Anonymize conditions
    with open(f"{input_dir}/conditions.ndjson", 'r') as f:
        conditions = [json.loads(line) for line in f]
    
    anonymized_conditions = []
    for condition in conditions:
        anonymized_conditions.append(anonymize_condition(condition, id_mapping))
    
    # Anonymize observations
    with open(f"{input_dir}/observations.ndjson", 'r') as f:
        observations = [json.loads(line) for line in f]
    
    anonymized_observations = []
    for observation in observations:
        anonymized_observations.append(anonymize_observation(observation, id_mapping))
    
    # Save anonymized data
    with open(f"{output_dir}/patients.ndjson", 'w') as f:
        for p in anonymized_patients:
            f.write(json.dumps(p) + '\n')
    
    with open(f"{output_dir}/conditions.ndjson", 'w') as f:
        for c in anonymized_conditions:
            f.write(json.dumps(c) + '\n')
    
    with open(f"{output_dir}/observations.ndjson", 'w') as f:
        for o in anonymized_observations:
            f.write(json.dumps(o) + '\n')
    
    print(f"✅ De-identification complete!")
    print(f"📁 Output: {output_dir}")
    print(f"📊 {len(anonymized_patients)} patients anonymized")

if __name__ == "__main__":
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "data/transformed"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/anonymized"
    anonymize_dataset(input_dir, output_dir)
