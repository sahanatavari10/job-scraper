import streamlit as st
import pandas as pd

df = pd.read_csv("python_jobs.csv")

st.set_page_config(page_title="Python Job Listings", layout="wide")
st.title("🐍 Python Job Listings Dashboard")

with st.sidebar:
    st.header("Filters")

    locations = st.multiselect(
        "Select Locations", 
        df['location'].dropna().unique(), 
        default=df['location'].dropna().unique()
    )

    title_keyword = st.text_input("Search Job Titles", value="")

    sort_option = st.selectbox("Sort by", ["Date Posted (Newest)", "Job Title (A-Z)"])

filtered_df = df[df['location'].isin(locations)]

if title_keyword:
    filtered_df = filtered_df[filtered_df['title'].str.contains(title_keyword, case=False, na=False)]

if sort_option == "Date Posted (Newest)":
    if "date_posted" in df.columns:
        filtered_df['date_posted'] = pd.to_datetime(filtered_df['date_posted'], errors='coerce')
        filtered_df = filtered_df.sort_values(by='date_posted', ascending=False)
elif sort_option == "Job Title (A-Z)":
    filtered_df = filtered_df.sort_values(by='title')

st.subheader(f"Showing {len(filtered_df)} job listings")
st.dataframe(filtered_df)

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_df)

st.download_button(
    label="⬇️ Download CSV",
    data=csv_data,
    file_name="filtered_python_jobs.csv",
    mime="text/csv"
)

st.subheader("📍 Jobs per Location")
location_counts = filtered_df['location'].value_counts()
st.bar_chart(location_counts)