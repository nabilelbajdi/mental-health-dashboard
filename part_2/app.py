import streamlit as st
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Mental Health Dataset Analysis",
    layout="wide",
    page_icon="brain"
)

# Load Mental Health Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Mental Health Dataset.csv")
    df["Hour"] = pd.to_datetime(df["Timestamp"]).dt.hour
    df["Month"] = pd.to_datetime(df["Timestamp"]).dt.month
    df["Year"] = pd.to_datetime(df["Timestamp"]).dt.year
    df["Day"] = pd.to_datetime(df["Timestamp"]).dt.day_name()
    return df

df = load_data()

# Title and Description
st.title("Mental Health Dataset Analysis")
st.write("""
Welcome to our interactive dashboard analyzing mental health data. Explore demographics and mental health insight across various factors such as gender, occupation, and treatment status.
Use the tabs above to navigate through different sections.
""")

# Data Cleaning
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce") 
df["self_employed"] = df["self_employed"].fillna("Not specified")
df["care_options"] = df["care_options"].replace("Not sure", "Maybe")

#------------ Visualization ------------

tab1, tab2, tab3 = st.tabs(["Data Overview", "Demographics", "Mental Health Insight"])

#--------- Tab 1: Data Overview ---------
with tab1:
    st.header("Data Overview")

    # Data Preview
    with st.expander("Data Preview"):
        st.dataframe(
            df,
            column_config={
                "Year": st.column_config.NumberColumn(format="%d")
            },
        )

    # Participation By Year Over Time Line Chart
    response_by_year = df.groupby("Year").size().reset_index(name="Total_Responses")
    fig_time = px.line(response_by_year,
                    x="Year",
                    y="Total_Responses",
                    title="Participation Over Time")
    st.plotly_chart(fig_time, use_container_width=True)

#--------- Tab 2: Demographics ---------
with tab2:
    st.header("Demographics")
    
    # Gender Distribution Pie Chart
    response_by_gender = df.groupby("Gender").size().reset_index(name="Total_Responses")
    fig_gender = px.pie(response_by_gender,
                 names="Gender",
                 values="Total_Responses",
                 title="Gender Distribution of Respondents")
    st.plotly_chart(fig_gender, use_container_width=True)

    # Country Distribution Choropleth Map
    response_by_country = df.groupby("Country").size().reset_index(name="Total_Responses")
    fig_map = px.choropleth(response_by_country,
                            locations="Country",
                            locationmode="country names",
                            color="Total_Responses",
                            hover_name="Country",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            title="Country Distribution of Respondents")
    st.plotly_chart(fig_map, use_container_width=True)

    # Occupation Distribution Bar Chart
    response_by_occupation = df.groupby("Occupation").size().reset_index(name="Total_Responses").sort_values(by="Total_Responses", ascending=False)
    fig_occupation = px.bar(response_by_occupation,
                            x="Occupation",
                            y="Total_Responses",
                            title="Occupation Distribution of Respondents",
                            labels={"Occupation": "Occupation", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_occupation, use_container_width=True)

    # Self-Employment Distribution Bar Chart
    df_filtered = df[df["self_employed"] != "Not specified"]
    response_by_self_employment = df_filtered.groupby("self_employed").size().reset_index(name="Total_Responses").sort_values(by="Total_Responses", ascending=False)
    fig_self_employed = px.bar(response_by_self_employment,
                               x="self_employed",
                               y="Total_Responses",
                               title="Self-Employment Distribution of Respondents",
                               labels={"self_employed": "Self-Employment Status", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_self_employed, use_container_width=True)

#--------- Tab 3: Mental Health Insight ---------
with tab3:
    st.header("Mental Health Insight")
    st.write("""
    family history... days indoors... growing stress... etc..
    """)

    # Family History vs Treatment
    response_by_family_history = df.groupby(["family_history", "treatment"]).size().reset_index(name="Total_Responses")
    fig_family_history = px.bar(response_by_family_history,
                                x="family_history",
                                y="Total_Responses",
                                color="treatment",
                                title="Family History of Mental Illness and Seeking Treatment Correlation",
                                labels={"family_history": "Family History of Mental Illness", 
                                        "treatment": "Seeking Treatment",
                                        "Total_Responses": "Number of Respondents"},
                                barmode="stack")
    st.plotly_chart(fig_family_history, use_container_width=True)

    # Days Indoors vs Coping Struggles 
    response_by_days_indoors = df.groupby(["Days_Indoors", "Coping_Struggles"]).size().reset_index(name="Total_Responses")
    fig_indoors_coping = px.density_heatmap(response_by_days_indoors,
                                            x="Days_Indoors",
                                            y="Coping_Struggles",
                                            z="Total_Responses",
                                            title="Relationship between Days Spent Indoors and Coping Struggles")
    st.plotly_chart(fig_indoors_coping, use_container_width=True)

    # Habit Changes vs Coping Struggles
    response_by_habit_changes = df.groupby(["Changes_Habits", "Coping_Struggles"]).size().reset_index(name="Total_Responses")
    fig_habit_changes = px.bar(response_by_habit_changes,
                                x="Changes_Habits",
                                y="Total_Responses",
                                color="Coping_Struggles",
                                title="Changes in Habits and Coping Struggles",
                                labels={"Changes_Habits": "Changes in Habits", "Total_Responses": "Number of Respondents"},
                                barmode="stack")
    st.plotly_chart(fig_habit_changes, use_container_width=True)

    # Mood swings vs gender (vi har gender som filter redan, men kanske ska ha med den ändå?)
    response_by_mood_swings = df.groupby(["Gender", "Mood_Swings"]).size().reset_index(name="Total_Responses")
    fig_mood_swings = px.bar(response_by_mood_swings,
                             x="Gender",
                             y="Total_Responses",
                             color="Mood_Swings",
                             title="Mood Swings Distribution Based on Gender",
                             labels={"Gender": "Gender", "Total_Responses": "Number of Respondents"},
                             barmode="group")
    st.plotly_chart(fig_mood_swings, use_container_width=True)

    # Mental health interview pie chart
    response_by_interview = df.groupby("mental_health_interview").size().reset_index(name="Total_Responses")
    fig_interview = px.pie(response_by_interview,
                        names="mental_health_interview",
                        values="Total_Responses",
                        title="Respondents Who Have Had Mental Health Interviews")
    st.plotly_chart(fig_interview, use_container_width=True)

    # Stress levels vs occupation
    response_by_occupation_struggles = df.groupby(["Occupation", "Growing_Stress"]).size().reset_index(name="Total_Responses")
    fig_occupation_struggles = px.bar(response_by_occupation_struggles,
                                        x="Occupation",
                                        y="Total_Responses",
                                        color="Growing_Stress",
                                        title="Occupations and Growing Stress Correlation",
                                        labels={"Occupation": "Occupation", "Total_Responses": "Number of Respondents"},
                                        barmode="group")
    st.plotly_chart(fig_occupation_struggles, use_container_width=True)

    # Family history vs mood swings
    response_by_family_mood_swings = df.groupby(["family_history", "Mood_Swings"]).size().reset_index(name="Total_Responses")
    fig_family_mood_swings = px.bar(response_by_family_mood_swings,
                                    x="family_history",
                                    y="Total_Responses",
                                    color="Mood_Swings",
                                    title="Family History and Mood Swings Correlation")
    st.plotly_chart(fig_family_mood_swings, use_container_width=True)

    # Seeking treatment vs gender (gender är redan filter)
    response_by_gender_treatment = df.groupby(["Gender", "treatment"]).size().reset_index(name="Total_Responses")
    fig_gender_treatment = px.bar(response_by_gender_treatment,
                                  x="Gender",
                                  y="Total_Responses",
                                  color="treatment",
                                  title="Gender Distribution of Mental Health Treatment",
                                  labels={"Gender": "Gender", "Total_Responses": "Number of Respondents"},
                                  barmode="stack")
    st.plotly_chart(fig_gender_treatment, use_container_width=True)

    # Regional Differences in Coping Struggles
    response_by_country_coping = df[df["Coping_Struggles"] == "Yes"].groupby("Country").size().reset_index(name="Total_Responses")
    top_10_countries = response_by_country_coping.sort_values(by="Total_Responses", ascending=False).head(10)
    fig_country_coping = px.choropleth(response_by_country_coping,
                                       locations="Country",
                                       locationmode="country names",
                                       color="Total_Responses",
                                       hover_name="Country",
                                       color_continuous_scale=px.colors.sequential.Viridis,
                                       title="Regional Differences in Coping Struggles")
    st.plotly_chart(fig_country_coping, use_container_width=True)

    # Complementary bar chart showing the top 10 countries struggling
    fig_top_5_countries = px.bar(top_10_countries,
                    x="Country", 
                    y="Total_Responses",  
                    title="Top 10 Countries with Highest Coping Struggles",
                    labels={"Country": "Country", "Total_Responses": "Number of Struggles"})
    st.plotly_chart(fig_top_5_countries, use_container_width=True)

    # Occupations with the Highest Stress Levels
    response_by_occupation_stress = df[df["Growing_Stress"] == "Yes"].groupby("Occupation").size().reset_index(name="Total_Responses")
    response_by_occupation_stress = response_by_occupation_stress.sort_values(by="Total_Responses", ascending=True)
    fig_occupation_stress = px.bar(response_by_occupation_stress,
                                    x="Total_Responses",
                                    y="Occupation",
                                    title="Occupations with the Highest Stress Levels",
                                    labels={"Total_Responses": "Number of Respondents", "Occupation": "Occupation"})
    st.plotly_chart(fig_occupation_stress, use_container_width=True)