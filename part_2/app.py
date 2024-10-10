import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np 

# Load the data
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
st.title("Mental Health Dataset")

# convert from object to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce') 

# clean self_employed None value data
df['self_employed'] = df['self_employed'].fillna('Not specified')

# clean care_options standardize "Maybe"
df["care_options"] = df["care_options"].replace("Not sure", "Maybe")

# Gender distribution pie chart of responses
gender_counts = df['Gender'].value_counts()
fig = px.pie(gender_counts, names=gender_counts.index, values=gender_counts.values, title='Gender Distribution')
st.plotly_chart(fig, use_container_width=True)