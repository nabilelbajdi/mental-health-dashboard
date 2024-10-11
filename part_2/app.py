import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np 

# page config
st.set_page_config(
    page_title="Mental Health Dataset Analysis",
    layout="wide",
    page_icon="brain"
)

# load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Mental Health Dataset.csv")
    df["Hour"] = pd.to_datetime(df["Timestamp"]).dt.hour
    df["Month"] = pd.to_datetime(df["Timestamp"]).dt.month
    df["Year"] = pd.to_datetime(df["Timestamp"]).dt.year
    df["Day"] = pd.to_datetime(df["Timestamp"]).dt.day_name()
    return df

df = load_data()

# title
st.title("Mental Health Dataset Analysis")
st.write("""
Welcome to our interactive dashboard analyzing mental health data. Explore demographics and mental health indicators across various factors such as gender, occupation, and treatment status.
Use the tabs above to navigate through different sections.
""")

# convert from object to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce') 

# clean self_employed None value data
df['self_employed'] = df['self_employed'].fillna('Not specified')

# clean care_options standardize "Maybe"
df["care_options"] = df["care_options"].replace("Not sure", "Maybe")

#__________Visualization__________"

tab1, tab2, tab3 = st.tabs(["Data Overview", "Survey Demographics", "Mental Health Indicators"])

with tab1:
    st.header("Data Overview")
    st.write("""
    number of participants... countries represented... date range... data preview...
    """)

    # original data preview
    with st.expander("Original Data Preview"):
        st.dataframe(
            df,
            column_config={
                "Year": st.column_config.NumberColumn(format="%d")
            },
        )

    # cleaned data preview
    with st.expander("Cleaned Data Preview"):
        st.dataframe(
            df,
            column_config={
                "Year": st.column_config.NumberColumn(format="%d")
            },
        )

with tab2:
    st.header("Survey Demographics")
    st.write("""
    gender distribution... geographic distribution... etc.
    """)
    
    # Gender distribution pie chart of responses
    gender_counts = df['Gender'].value_counts()
    fig = px.pie(gender_counts, names=gender_counts.index, values=gender_counts.values, title='Gender Distribution')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Mental Health Indicators")
    st.write("""
    family history... days indoors... growing stress... etc..
    """)