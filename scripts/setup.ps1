# scripts/setup.ps1
Write-Host "🔧 Setting up FHIR Pipeline..." -ForegroundColor Cyan

# Create virtual environment
python -m venv venv

# Activate and install packages
.\venv\Scripts\Activate.ps1
pip install pandas faker streamlit flask requests numpy plotly

Write-Host "✅ Setup complete!" -ForegroundColor Green
