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
st.dataframe(df.head(36))

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
