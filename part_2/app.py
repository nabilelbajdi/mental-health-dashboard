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
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce") 

# clean self_employed None value data
df["self_employed"] = df["self_employed"].fillna("Not specified")

# clean care_options standardize "Maybe"
df["care_options"] = df["care_options"].replace("Not sure", "Maybe")

#__________Visualization__________"

tab1, tab2, tab3 = st.tabs(["Data Overview", "Survey Demographics", "Mental Health Indicators"])

with tab1:
    st.header("Data Overview")
    st.write("""
    number of participants... countries represented... date range... data preview...
    """)

    # data preview
    with st.expander("Data Preview"):
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
    response_by_gender = df.groupby("Gender").size().reset_index(name="Total_Responses")
    fig_gender = px.pie(response_by_gender,
                 names="Gender",
                 values="Total_Responses",
                 title="Gender Distribution of Respondents")
    st.plotly_chart(fig_gender, use_container_width=True)

    # Country distribution choropleth map of responses
    response_by_country = df.groupby("Country").size().reset_index(name="Total_Responses")
    fig_map = px.choropleth(response_by_country,
                            locations="Country",
                            locationmode="country names",
                            color="Total_Responses",
                            hover_name="Country",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            title="Country Distribution of Respondents")
    st.plotly_chart(fig_map, use_container_width=True)

    # Occupation distribution bar chart of responses
    response_by_occupation = df.groupby("Occupation").size().reset_index(name="Total_Responses").sort_values(by="Total_Responses", ascending=False)
    fig_occupation = px.bar(response_by_occupation,
                            x="Occupation",
                            y="Total_Responses",
                            title="Occupation Distribution of Respondents",
                            labels={"Occupation": "Occupation", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_occupation, use_container_width=True)

with tab3:
    st.header("Mental Health Indicators")
    st.write("""
    family history... days indoors... growing stress... etc..
    """)