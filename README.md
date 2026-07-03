# 🏥 FHIR Clinical Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FHIR](https://img.shields.io/badge/FHIR-R4-green.svg)](https://hl7.org/fhir)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue.svg)](https://microsoft.com/powershell)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/mbuguakevvz/fhir-pipeline)](https://github.com/mbuguakevvz/fhir-pipeline/stargazers)

## 📊 Project Overview

An **end-to-end clinical data interoperability pipeline** that generates synthetic patient data, transforms it into FHIR-compliant resources, and provides interactive visualization. Built with Python, PowerShell, and Streamlit.

## 🎯 Key Features

- ✅ **Data Generation**: Creates realistic synthetic patient data with demographics, conditions, and lab results
- ✅ **FHIR Transformation**: Converts CSV data to FHIR R4 resources (Patient, Condition, Observation)
- ✅ **Interactive Dashboard**: Real-time visualization with filtering and search (Streamlit + Plotly)
- ✅ **De-identification**: HIPAA-compliant anonymization of patient data
- ✅ **PowerShell Automation**: One-command pipeline execution

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PowerShell 5.1+
- Git

### Installation

\\\powershell
# Clone the repository
git clone https://github.com/mbuguakevvz/fhir-pipeline.git
cd fhir-pipeline

# Run setup (installs all dependencies)
.\scripts\setup.ps1

# Activate virtual environment
.\venv\Scripts\Activate.ps1
\\\

### Run the Pipeline

\\\powershell
# Generate 1000 patients and transform to FHIR
.\scripts\run-pipeline.ps1 -PatientCount 1000

# Launch the dashboard
streamlit run src/dashboard/app.py

# Apply de-identification (HIPAA compliance)
python src/deidentify/anonymize.py
\\\

## 📁 Project Structure

\\\
fhir-pipeline/
├── data/
│   ├── raw/          # Generated patient CSVs
│   └── transformed/  # FHIR NDJSON resources
├── src/
│   ├── generator/    # Synthetic data generation
│   ├── transformer/  # CSV → FHIR conversion
│   ├── deidentify/   # HIPAA anonymization
│   └── dashboard/    # Streamlit visualization
├── scripts/          # PowerShell automation
│   ├── setup.ps1
│   └── run-pipeline.ps1
└── requirements.txt  # Python dependencies
\\\

## 📊 Dashboard Preview

The interactive dashboard provides:

- **Key Metrics**: Total patients, conditions, observations
- **Demographics**: Gender distribution, age histogram
- **Clinical Insights**: Top conditions, observation distribution
- **Patient Search**: Filter and view individual patient details

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Data Generation | Python, Faker, Pandas |
| FHIR Transformation | Python, Pandas |
| De-identification | Python, Hashlib |
| Dashboard | Streamlit, Plotly |
| Orchestration | PowerShell |
| Version Control | Git, GitHub |

## 📈 Generated Data Statistics

With default settings (1000 patients):

| Resource Type | Count |
|--------------|-------|
| Patients | 1,000 |
| Conditions | 600+ |
| Observations | 3,000 |
| Avg Observations/Patient | 3.0 |

## 🔒 Privacy & Compliance

- **Synthetic Data**: No real patient data used
- **De-identification**: HIPAA-compliant anonymization
- **Data Security**: Local processing only

## 🚀 Future Enhancements

- [ ] Add more FHIR resources (Encounter, Medication, Allergy)
- [ ] REST API with Flask/FastAPI
- [ ] Cloud deployment (Azure/AWS)
- [ ] CI/CD with GitHub Actions
- [ ] Real EHR system integration

## 📝 License

MIT License - Feel free to use, modify, and distribute!

## 🙏 Acknowledgments

- HL7 FHIR Standard
- Faker Library for data generation
- Streamlit for dashboard framework

---

**Built with ❤️ by Kevin Mbugua**

🔗 **Repository**: [https://github.com/mbuguakevvz/fhir-pipeline](https://github.com/mbuguakevvz/fhir-pipeline)
🐙 **GitHub**: [@mbuguakevvz](https://github.com/mbuguakevvz)
