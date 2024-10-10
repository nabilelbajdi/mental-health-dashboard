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
st.write(df["self_employed"].value_counts())
st.write(df['self_employed'].isna().sum())

# checks that all missing values are gone
st.write(df.isna().sum())

st.write(df)

# Gender distribution pie chart of responses
gender_counts = df['Gender'].value_counts()
fig = px.pie(gender_counts, names=gender_counts.index, values=gender_counts.values, title='Gender Distribution')
st.plotly_chart(fig, use_container_width=True)

st.write(df['Timestamp'].unique())
st.write(df['Gender'].unique())
st.write(df['Country'].unique())
st.write(df['Occupation'].unique())
st.write(df['self_employed'].unique())
st.write(df['family_history'].unique())
st.write(df['treatment'].unique())
st.write(df['Days_Indoors'].unique())
st.write(df['Growing_Stress'].unique())
st.write(df['Changes_Habits'].unique())
st.write(df['Mental_Health_History'].unique())
st.write(df['Mood_Swings'].unique())
st.write(df['Coping_Struggles'].unique())
st.write(df['Work_Interest'].unique())
st.write(df['Social_Weakness'].unique())
st.write(df['mental_health_interview'].unique())
st.write(df['care_options'].unique())
st.write(df['Hour'].unique())
st.write(df['Day'].unique())
st.write(df['Month'].unique())
st.write(df['Year'].unique())




