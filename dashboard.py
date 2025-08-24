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

st.markdown("### Filter and Sample Job Preview")
df_clean = pd.read_csv("clean_job_data.csv")
filter_col = df_clean.select_dtypes(include="object").columns[0]
options = ["All"] + sorted(df_clean[filter_col].dropna().unique())
choice = st.selectbox(f"Select {filter_col}", options)

filtered = df_clean if choice == "All" else df_clean[df_clean[filter_col] == choice]

if not filtered.empty:
    job = filtered.sample(1).iloc[0]
    with st.expander("#Sample Job"):
        for col in filtered.columns:
            st.write(f"**{col}:** {job[col]}")
else:
    st.warning("No jobs found.")

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
