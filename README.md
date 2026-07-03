# FHIR Clinical Data Pipeline

A complete end-to-end pipeline for generating synthetic patient data and transforming it to FHIR R4 resources.

## Features
- ✅ Synthetic patient data generation (1,000+ patients)
- ✅ FHIR R4 transformation (Patient, Condition, Observation)
- ✅ Interactive Streamlit dashboard
- ✅ PowerShell automation
- ✅ HIPAA-compliant de-identification

## Quick Start
\\\powershell
.\scripts\run-pipeline.ps1 -PatientCount 1000
streamlit run src/dashboard/app.py
\\\

## Tech Stack
- Python 3.10+, Pandas, Faker
- FHIR R4 (HL7)
- Streamlit, Plotly
- PowerShell

## Author
Kevin Mbugua
