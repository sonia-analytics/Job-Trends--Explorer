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

st.markdown("###Filter and Sample Job Preview")

try:
    df_clean = pd.read_csv("clean_job_data.csv")
except Exception as e:
    st.error(f"Failed to load clean_job_data.csv. Error: {str(e)}")
    st.stop()

# Auto-detect a usable column for filtering
text_columns = df_clean.select_dtypes(include="object").columns.tolist()
filter_column = text_columns[0] if text_columns else None

if filter_column:
    st.write(f"Filtering by: **{filter_column}**")
    options = ["All"] + sorted(df_clean[filter_column].dropna().unique().tolist())
    selected = st.selectbox(f"Select a {filter_column}", options)

    filtered_df = df_clean if selected == "All" else df_clean[df_clean[filter_column] == selected]

    st.markdown("### 📄 Sample Job Preview")
    if not filtered_df.empty:
        job = filtered_df.sample(1).iloc[0]
        with st.expander("Click to view a sample job"):
            for col in filtered_df.columns:
                st.write(f"**{col}:** {job[col]}")
    else:
        st.warning("No jobs found for the selected option.")
else:
    st.warning("No text columns available for filtering.")
