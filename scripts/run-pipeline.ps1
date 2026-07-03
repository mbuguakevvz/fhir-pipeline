# scripts/run-pipeline.ps1
param([int]$PatientCount = 1000)

Write-Host "🚀 Starting FHIR Pipeline..." -ForegroundColor Cyan

# Generate data
Write-Host "`n📊 Generating patient data..." -ForegroundColor Yellow
python src/generator/generate_patients.py $PatientCount data/raw/patients.csv

# Transform to FHIR
Write-Host "`n🔄 Transforming to FHIR..." -ForegroundColor Yellow
python src/transformer/csv_to_fhir.py data/raw/patients.csv data/transformed

# Show results
Write-Host "`n📊 Pipeline Complete!" -ForegroundColor Green
Write-Host "Patients: $(Get-Content data/transformed/patients.ndjson).Count" -ForegroundColor Green
Write-Host "Launch dashboard: streamlit run src/dashboard/app.py" -ForegroundColor Yellow
