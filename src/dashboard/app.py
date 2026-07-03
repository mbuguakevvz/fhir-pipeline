# src/dashboard/app.py
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="FHIR Clinical Data Pipeline",
    page_icon="🏥",
    layout="wide"
)

# Title
st.title("🏥 FHIR Clinical Data Pipeline Dashboard")
st.markdown("*Real-time visualization of synthetic patient data*")
st.markdown("---")

# Load data
@st.cache_data
def load_patients():
    with open('data/transformed/patients.ndjson', 'r') as f:
        patients = [json.loads(line) for line in f]
    return pd.DataFrame([{
        'Patient ID': p['id'],
        'First Name': p['name'][0]['given'][0],
        'Last Name': p['name'][0]['family'],
        'Gender': p['gender'].capitalize(),
        'Birth Date': p['birthDate'],
        'Age': datetime.now().year - int(p['birthDate'][:4])
    } for p in patients])

@st.cache_data
def load_conditions():
    with open('data/transformed/conditions.ndjson', 'r') as f:
        conditions = [json.loads(line) for line in f]
    return pd.DataFrame([{
        'Patient ID': c['subject']['reference'].replace('Patient/', ''),
        'Condition': c['code']['coding'][0]['display']
    } for c in conditions])

@st.cache_data
def load_observations():
    with open('data/transformed/observations.ndjson', 'r') as f:
        obs = [json.loads(line) for line in f]
    return pd.DataFrame([{
        'Patient ID': o['subject']['reference'].replace('Patient/', ''),
        'Type': o['code']['coding'][0]['display'],
        'Value': o['valueQuantity']['value'],
        'Unit': o['valueQuantity']['unit']
    } for o in obs])

# Load all data
patients_df = load_patients()
conditions_df = load_conditions()
observations_df = load_observations()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Gender filter
gender_filter = st.sidebar.multiselect(
    "Gender",
    options=patients_df['Gender'].unique(),
    default=patients_df['Gender'].unique()
)

# Age range filter
age_min = int(patients_df['Age'].min())
age_max = int(patients_df['Age'].max())
age_range = st.sidebar.slider(
    "Age Range",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max)
)

# Condition filter
all_conditions = sorted(conditions_df['Condition'].unique())
condition_filter = st.sidebar.multiselect(
    "Condition",
    options=all_conditions,
    default=all_conditions[:5] if len(all_conditions) > 5 else all_conditions
)

# Filter data
filtered_patients = patients_df[
    (patients_df['Gender'].isin(gender_filter)) &
    (patients_df['Age'] >= age_range[0]) &
    (patients_df['Age'] <= age_range[1])
]

filtered_conditions = conditions_df[
    conditions_df['Patient ID'].isin(filtered_patients['Patient ID']) &
    (conditions_df['Condition'].isin(condition_filter))
]

filtered_observations = observations_df[
    observations_df['Patient ID'].isin(filtered_patients['Patient ID'])
]

# Main Dashboard
# Row 1: Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Patients",
        f"{len(filtered_patients):,}",
        delta=f"{len(filtered_patients) - len(patients_df)} from total" if len(filtered_patients) != len(patients_df) else None
    )

with col2:
    st.metric(
        "Total Conditions",
        f"{len(filtered_conditions):,}"
    )

with col3:
    st.metric(
        "Total Observations",
        f"{len(filtered_observations):,}"
    )

with col4:
    avg_obs = len(filtered_observations) / len(filtered_patients) if len(filtered_patients) > 0 else 0
    st.metric(
        "Avg Observations/Patient",
        f"{avg_obs:.1f}"
    )

st.markdown("---")

# Row 2: Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Patient Demographics")
    
    # Gender distribution
    gender_counts = filtered_patients['Gender'].value_counts()
    fig = px.pie(
        values=gender_counts.values,
        names=gender_counts.index,
        title="Gender Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Age distribution
    st.subheader("📊 Age Distribution")
    fig = px.histogram(
        filtered_patients,
        x='Age',
        nbins=20,
        title="Age Distribution",
        color_discrete_sequence=['#1f77b4']
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏥 Top Conditions")
    condition_counts = filtered_conditions['Condition'].value_counts().head(10)
    fig = px.bar(
        x=condition_counts.values,
        y=condition_counts.index,
        orientation='h',
        title="Most Common Conditions",
        color=condition_counts.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(xaxis_title="Count", yaxis_title="Condition")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔬 Observation Distribution")
    obs_counts = filtered_observations['Type'].value_counts()
    fig = px.bar(
        x=obs_counts.values,
        y=obs_counts.index,
        orientation='h',
        title="Observations by Type",
        color=obs_counts.values,
        color_continuous_scale='Greens'
    )
    fig.update_layout(xaxis_title="Count", yaxis_title="Observation Type")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 3: Detailed Tables
st.subheader("📋 Patient List")
st.dataframe(
    filtered_patients,
    use_container_width=True,
    hide_index=True
)

# Row 4: Patient Detail View
st.subheader("🔍 Patient Detail Explorer")
selected_patient = st.selectbox(
    "Select a Patient ID to view details",
    filtered_patients['Patient ID'].tolist()
)

if selected_patient:
    col1, col2 = st.columns(2)
    
    with col1:
        patient_info = filtered_patients[filtered_patients['Patient ID'] == selected_patient].iloc[0]
        st.markdown("**Patient Demographics:**")
        st.write(f"👤 **Name:** {patient_info['First Name']} {patient_info['Last Name']}")
        st.write(f"⚧️ **Gender:** {patient_info['Gender']}")
        st.write(f"📅 **Age:** {patient_info['Age']}")
        st.write(f"🎂 **Birth Date:** {patient_info['Birth Date']}")
    
    with col2:
        st.markdown("**Conditions:**")
        patient_conditions = filtered_conditions[filtered_conditions['Patient ID'] == selected_patient]
        if len(patient_conditions) > 0:
            for cond in patient_conditions['Condition']:
                st.write(f"• {cond}")
        else:
            st.write("No conditions recorded")
    
    st.markdown("**Observations:**")
    patient_obs = filtered_observations[filtered_observations['Patient ID'] == selected_patient]
    if len(patient_obs) > 0:
        st.dataframe(patient_obs[['Type', 'Value', 'Unit']], use_container_width=True, hide_index=True)
    else:
        st.write("No observations recorded")

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Data source: Synthetic patient data generated via FHIR Pipeline")
