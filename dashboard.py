import streamlit as st
import pandas as pd
import ast
import os

st.title("Local Job Trends Explorer")
st.write("Analyze Data Analyst job trends in Philadelphia, PA.")

try:
    df = pd.read_csv("raw_job_data.csv")  # Directly load the CSV file
except Exception as e:
    st.error(f"Failed to load raw_job_data.csv. Please ensure it's in the app folder. Error: {str(e)}")
    st.stop()
    
st.subheader("Data Preview")
st.dataframe(df.head(35))

st.subheader("Sample Job Previews")
df = pd.read_csv("clean_job_data.csv")  # Directly load the CSV file
st.dataframe(df.head(5))

st.subheader("Bar Chart Images")
if os.path.exists("companies.png"):
    st.image("companies.png", caption="Top Companies (Image)", use_container_width=True)
else:
    st.warning("companies.png not found in app folder.")

if os.path.exists("skills.png"):
    st.image("skills.png", caption="Top Skills (Image)", use_container_width=True)
else:
    st.warning("skills.png not found in app folder.")

st.markdown('--------')
st.write("Data source: LinkedIn job postings | Dashboard by Sonia Mannepuli")

# -------- Filter and Sample Job Preview --------
st.markdown("### 🔍 Filter Jobs by Company")

# Reload cleaned data for filtering
try:
    df_clean = pd.read_csv("clean_job_data.csv")
except Exception as e:
    st.error(f"Failed to load clean_job_data.csv. Error: {str(e)}")
    st.stop()

# Create filter dropdown
company_options = ["All"] + sorted(df_clean["company"].dropna().unique().tolist())
selected_company = st.selectbox("Select a Company", company_options)

# Apply filter
if selected_company != "All":
    filtered_df = df_clean[df_clean["company"] == selected_company]
else:
    filtered_df = df_clean

# -------- Filter and Sample Job Preview --------
st.markdown("##Filter Jobs by Company")

try:
    df_clean = pd.read_csv("clean_job_data.csv")
except Exception as e:
    st.error(f"Failed to load clean_job_data.csv. Error: {str(e)}")
    st.stop()

# Use actual column name from your file
actual_column = "company"  # Replace with exact name from st.write output

if actual_column in df_clean.columns:
    company_options = ["All"] + sorted(df_clean[actual_column].dropna().unique().tolist())
    selected_company = st.selectbox("Select a Company", company_options)

    if selected_company != "All":
        filtered_df = df_clean[df_clean[actual_column] == selected_company]
    else:
        filtered_df = df_clean

    st.markdown("### 📄 Sample Job Preview")
    if not filtered_df.empty:
        sample_job = filtered_df.sample(1).iloc[0]
        with st.expander("Click to view a sample job"):
            st.write(f"**Title:** {sample_job.get('Title', 'N/A')}")
            st.write(f"**Company:** {sample_job.get(actual_column, 'N/A')}")
            st.write(f"**Location:** {sample_job.get('Location', 'N/A')}")
            st.write(f"**Description:** {sample_job.get('Description', 'N/A')}")
    else:
        st.warning("No jobs found for the selected company.")
else:
    st.warning(f"Column '{actual_column}' not found in dataset.")
