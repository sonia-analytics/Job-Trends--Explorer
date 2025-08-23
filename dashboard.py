import streamlit as st
import pandas as pd
import ast
import os

st.title("Local Job Trends Explorer")
st.write("Analyze Data Analyst job trends in Philadelphia, PA.")

# --- Data Loading ---
try:
    df = pd.read_csv("clean_job_data.csv")  # Directly load the CSV file
except Exception as e:
    st.error(f"Failed to load clean_job_data.csv. Please ensure it's in the app folder. Error: {str(e)}")
    st.stop()

# --- Data Preview ---
st.subheader("Data Preview")
st.dataframe(df.head(6))

# --- Filters ---
st.subheader("Filter Jobs")

# Company filter
company_col = [col for col in df.columns if col.strip().lower() == 'company']
if company_col:
    company_col = company_col[0]
    companies = sorted(df[company_col].dropna().unique())
    selected_company = st.selectbox("Filter by company", ["All"] + companies)
    if selected_company != "All":
        df = df[df[company_col] == selected_company]

# Skill filter
skills_col = [col for col in df.columns if col.strip().lower() == 'skills']
if skills_col:
    skills_col = skills_col[0]
    # Flatten all skills for the filter
    all_skills = []
    for val in df[skills_col].dropna():
        if isinstance(val, str):
            if val.startswith('['):
                try:
                    all_skills.extend(ast.literal_eval(val))
                except:
                    continue
            else:
                all_skills.extend([s.strip() for s in val.split(',')])
    all_skills = sorted(set([s.lower() for s in all_skills]))
    selected_skill = st.selectbox("Filter by skill", ["All"] + all_skills)
    if selected_skill != "All":
        def has_skill(x):
            if isinstance(x, str):
                if x.startswith('['):
                    try:
                        return selected_skill in [s.lower() for s in ast.literal_eval(x)]
                    except:
                        return False
                else:
                    return selected_skill in [s.strip().lower() for s in x.split(',')]
            return False
        df = df[df[skills_col].apply(has_skill)]

# Keyword search
keyword = st.text_input("Search job title or summary (optional)").strip().lower()
if keyword:
    title_col = [col for col in df.columns if col.strip().lower() == 'title']
    summary_col = [col for col in df.columns if col.strip().lower() == 'summary']
    mask = pd.Series([False]*len(df))
    if title_col:
        mask = mask | df[title_col[0]].astype(str).str.lower().str.contains(keyword, na=False)
    if summary_col:
        mask = mask | df[summary_col[0]].astype(str).str.lower().str.contains(keyword, na=False)
    df = df[mask]

st.write(f"Showing {len(df)} jobs after filtering.")

# --- Job Previews ---
st.subheader("Sample Job Previews")
st.dataframe(df.head(5))

# --- Bar Charts (Filtered) ---
st.subheader("Top Companies Hiring (Filtered)")
if company_col and not df.empty:
    company_counts = df[company_col].value_counts().head(10)
    st.bar_chart(company_counts)
else:
    st.warning("No 'Company' column found or no data to display.")

st.subheader("Top Skills in Demand (Filtered)")
if skills_col and not df.empty:
    def parse_skills(x):
        if isinstance(x, str):
            if x.startswith('['):
                try:
                    return [s.strip().lower() for s in ast.literal_eval(x)]
                except:
                    return []
            else:
                return [s.strip().lower() for s in x.split(',')]
        return []
    skills_series = df[skills_col].dropna().apply(parse_skills)
    all_skills = [skill for sublist in skills_series for skill in sublist]
    if all_skills:
        skills_counts = pd.Series(all_skills).value_counts().head(10)
        st.bar_chart(skills_counts)
    else:
        st.warning("No skills data found.")
else:
    st.warning("No 'Skills' column found or no data to display.")

# --- Static Images ---
st.subheader("Bar Chart Images")
if os.path.exists("companies.png"):
    st.image("companies.png", caption="Top Companies (Image)", use_container_width=True)
else:
    st.warning("companies.png not found in app folder.")

if os.path.exists("skills.png"):
    st.image("skills.png", caption="Top Skills (Image)", use_container_width=True)
else:
    st.warning("skills.png not found in app folder.")

st.markdown("---")
st.write("Data source: LinkedIn job postings | Dashboard by Sonia Mannepuli")
