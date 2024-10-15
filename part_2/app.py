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

# Sidebar Filters
st.sidebar.title("Gender Filter")
gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
)

st.sidebar.title("Country Filter")
country = st.sidebar.multiselect(
    "Select Country",
    options=df["Country"].unique(),
)

# Default Filters
if not gender:
    gender = df["Gender"].unique()
if not country:
    country = df["Country"].unique()

df_selection = df[df["Gender"].isin(gender) & df["Country"].isin(country)]

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

tab1, tab2, tab3, tab4 = st.tabs(["Data Overview", "Demographics", "Mental Health Insight", "Treatment & Care"])

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

    # Participation By Year Over Time (Line Chart)
    response_by_year = df.groupby("Year").size().reset_index(name="Total_Responses")
    fig_time = px.line(response_by_year,
                    x="Year", y="Total_Responses",
                    title="Participation Over Time")
    st.plotly_chart(fig_time, use_container_width=True)

#--------- Tab 2: Demographics ---------
with tab2:
    st.header("Demographics")
    
    # Gender Distribution (Pie Chart)
    response_by_gender = df_selection.groupby("Gender").size().reset_index(name="Total_Responses")
    fig_gender = px.pie(response_by_gender,
                 names="Gender",
                 values="Total_Responses",
                 title="Gender Distribution")
    st.plotly_chart(fig_gender, use_container_width=True)

    # Country Distribution (Choropleth Map)
    response_by_country = df_selection.groupby("Country").size().reset_index(name="Total_Responses")
    fig_map = px.choropleth(response_by_country,
                            locations="Country",
                            locationmode="country names",
                            color="Total_Responses",
                            hover_name="Country",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            title="Country Distribution")
    st.plotly_chart(fig_map, use_container_width=True)

    # Occupation Distribution (Bar Chart)
    response_by_occupation = df_selection.groupby("Occupation").size().reset_index(name="Total_Responses").sort_values(by="Total_Responses", ascending=False)
    fig_occupation = px.bar(response_by_occupation,
                            x="Occupation", y="Total_Responses",
                            title="Occupation Distribution",
                            labels={"Occupation": "Occupation", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_occupation, use_container_width=True)

    # Self-Employment Distribution (Bar Chart)
    df_filtered = df_selection[df_selection["self_employed"] != "Not specified"]
    response_by_self_employment = df_filtered.groupby("self_employed").size().reset_index(name="Total_Responses").sort_values(by="Total_Responses", ascending=False)
    fig_self_employed = px.bar(response_by_self_employment,
                               x="self_employed", y="Total_Responses",
                               title="Self-Employment Distribution",
                               labels={"self_employed": "Self-Employment Status", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_self_employed, use_container_width=True)

    # Family History Distribution (Bar Chart)
    response_by_family_history = df_selection.groupby("family_history").size().reset_index(name="Total_Responses")
    fig_family_history = px.bar(response_by_family_history,
                                x="family_history", y="Total_Responses",
                                title="Family History of Mental Illness Distribution",
                                labels={"family_history": "Family History", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_family_history, use_container_width=True)

    # Mental Health Interview Distribution (Pie Chart)
    response_by_interview = df_selection.groupby("mental_health_interview").size().reset_index(name="Total_Responses")
    fig_interview = px.pie(response_by_interview,
                        names="mental_health_interview",
                        values="Total_Responses",
                        title="Mental Health Interview Distribution")
    st.plotly_chart(fig_interview, use_container_width=True)

    # Growing Stress Distribution (Bar chart)
    response_by_stress_levels = df_selection.groupby("Growing_Stress").size().reset_index(name="Total_Responses")
    fig_stress_levels = px.bar(response_by_stress_levels,
                            x="Growing_Stress", y="Total_Responses",
                            title="Growing Stress Distribution",
                            labels={"Growing_Stress": "Stress Level", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_stress_levels, use_container_width=True)

    # Coping Struggles Distribution (Bar chart)
    response_by_coping_struggles = df_selection.groupby("Coping_Struggles").size().reset_index(name="Total_Responses")
    fig_coping_struggles = px.bar(response_by_coping_struggles,
                                x="Coping_Struggles", y="Total_Responses",
                                title="Coping Struggles Distribution",
                                labels={"Coping_Struggles": "Coping Struggles", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_coping_struggles, use_container_width=True)

    # Treatment Distribution (Bar chart)
    response_by_treatment = df_selection.groupby("treatment").size().reset_index(name="Total_Responses")
    fig_treatment = px.bar(response_by_treatment,
                        x="treatment", y="Total_Responses",
                        title="Treatment STatus Distribution",
                        labels={"treatment": "Treatment Status", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_treatment, use_container_width=True)

    # Days Indoors Distribution (Bar chart)
    response_by_days_indoors = df_selection.groupby("Days_Indoors").size().reset_index(name="Total_Responses")
    fig_days_indoors = px.bar(response_by_days_indoors,
                            x="Days_Indoors", y="Total_Responses",
                            title="Days Indoors Distribution",
                            labels={"Days_Indoors": "Days Indoors", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_days_indoors, use_container_width=True)

    # Habit Changes Distribution (Bar chart)
    response_by_changes_habits = df_selection.groupby("Changes_Habits").size().reset_index(name="Total_Responses")
    fig_changes_habits = px.bar(response_by_changes_habits,
                                x="Changes_Habits", y="Total_Responses",
                                title="Habit Changes Distribution",
                                labels={"Changes_Habits": "Changes in Habits", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_changes_habits, use_container_width=True)

    # History of Mental Health Distribution (Bar chart)
    response_by_mental_health_history = df_selection.groupby("Mental_Health_History").size().reset_index(name="Total_Responses")
    fig_mental_health_history = px.bar(response_by_mental_health_history,
                                    x="Mental_Health_History", y="Total_Responses",
                                    title="Mental Health History Distribution",
                                    labels={"Mental_Health_History": "History of Mental Health", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_mental_health_history, use_container_width=True)

    # Mood Swings Distribution (Bar chart)
    response_by_mood_swings = df_selection.groupby("Mood_Swings").size().reset_index(name="Total_Responses")
    fig_mood_swings = px.bar(response_by_mood_swings,
                            x="Mood_Swings", y="Total_Responses",
                            title="Mood Swings Distribution",
                            labels={"Mood_Swings": "Mood Swings", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_mood_swings, use_container_width=True)

    # Work Interest Distribution (Bar chart)
    response_by_work_interest = df_selection.groupby("Work_Interest").size().reset_index(name="Total_Responses")
    fig_work_interest = px.bar(response_by_work_interest,
                            x="Work_Interest", y="Total_Responses",
                            title="Work Interest Distribution",
                            labels={"Work_Interest": "Work Interest", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_work_interest, use_container_width=True)

    # Social Weakness Distribution (Bar chart)
    response_by_social_weakness = df_selection.groupby("Social_Weakness").size().reset_index(name="Total_Responses")
    fig_social_weakness = px.bar(response_by_social_weakness,
                                x="Social_Weakness", y="Total_Responses",
                                title="Social Weakness Distribution",
                                labels={"Social_Weakness": "Social Weakness", "Total_Responses": "Number of Respondents"})
    st.plotly_chart(fig_social_weakness, use_container_width=True)

#--------- Tab 3: Mental Health Insight ---------
with tab3:
    st.header("Mental Health Insight")

    # Days Indoors vs Coping Struggles 
    response_by_days_indoors = df_selection.groupby(["Days_Indoors", "Coping_Struggles"]).size().reset_index(name="Total_Responses")
    fig_indoors_coping = px.density_heatmap(response_by_days_indoors,
                                            x="Days_Indoors",
                                            y="Coping_Struggles",
                                            z="Total_Responses",
                                            title="Relationship between Days Spent Indoors and Coping Struggles")
    st.plotly_chart(fig_indoors_coping, use_container_width=True)

    # Habit Changes vs Coping Struggles
    response_by_habit_changes = df_selection.groupby(["Changes_Habits", "Coping_Struggles"]).size().reset_index(name="Total_Responses")
    fig_habit_changes = px.bar(response_by_habit_changes,
                                x="Changes_Habits",
                                y="Total_Responses",
                                color="Coping_Struggles",
                                title="Changes in Habits and Coping Struggles",
                                labels={"Changes_Habits": "Changes in Habits", "Total_Responses": "Number of Respondents"},
                                barmode="stack")
    st.plotly_chart(fig_habit_changes, use_container_width=True)

    # Mood swings vs gender
    response_by_mood_swings = df_selection.groupby(["Gender", "Mood_Swings"]).size().reset_index(name="Total_Responses")
    fig_mood_swings = px.bar(response_by_mood_swings,
                             x="Gender",
                             y="Total_Responses",
                             color="Mood_Swings",
                             title="Mood Swings Distribution Based on Gender",
                             labels={"Gender": "Gender", "Total_Responses": "Number of Respondents"},
                             barmode="group")
    st.plotly_chart(fig_mood_swings, use_container_width=True)

    # Stress levels vs occupation
    response_by_occupation_struggles = df_selection.groupby(["Occupation", "Growing_Stress"]).size().reset_index(name="Total_Responses")
    fig_occupation_struggles = px.bar(response_by_occupation_struggles,
                                        x="Occupation",
                                        y="Total_Responses",
                                        color="Growing_Stress",
                                        title="Occupations and Growing Stress Correlation",
                                        labels={"Occupation": "Occupation", "Total_Responses": "Number of Respondents"},
                                        barmode="group")
    st.plotly_chart(fig_occupation_struggles, use_container_width=True)

    # Family history vs mood swings
    response_by_family_mood_swings = df_selection.groupby(["family_history", "Mood_Swings"]).size().reset_index(name="Total_Responses")
    fig_family_mood_swings = px.bar(response_by_family_mood_swings,
                                    x="family_history",
                                    y="Total_Responses",
                                    color="Mood_Swings",
                                    title="Family History and Mood Swings Correlation")
    st.plotly_chart(fig_family_mood_swings, use_container_width=True)

    # Regional Differences in Coping Struggles
    response_by_country_coping = df_selection[df_selection["Coping_Struggles"] == "Yes"].groupby("Country").size().reset_index(name="Total_Responses")
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
    response_by_occupation_stress = df_selection[df_selection["Growing_Stress"] == "Yes"].groupby("Occupation").size().reset_index(name="Total_Responses")
    response_by_occupation_stress = response_by_occupation_stress.sort_values(by="Total_Responses", ascending=True)
    fig_occupation_stress = px.bar(response_by_occupation_stress,
                                    x="Total_Responses",
                                    y="Occupation",
                                    title="Occupations with the Highest Stress Levels",
                                    labels={"Total_Responses": "Number of Respondents", "Occupation": "Occupation"})
    st.plotly_chart(fig_occupation_stress, use_container_width=True)

#--------- Tab 4: Treatment & Care ---------
with tab4:
    st.header("Treatment & Care")

    # Family History vs Treatment
    response_by_family_history = df_selection.groupby(["family_history", "treatment"]).size().reset_index(name="Total_Responses")
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

    # Seeking treatment vs gender
    response_by_gender_treatment = df_selection.groupby(["Gender", "treatment"]).size().reset_index(name="Total_Responses")
    fig_gender_treatment = px.bar(response_by_gender_treatment,
                                  x="Gender",
                                  y="Total_Responses",
                                  color="treatment",
                                  title="Gender Distribution of Mental Health Treatment",
                                  labels={"Gender": "Gender", "Total_Responses": "Number of Respondents"},
                                  barmode="stack")
    st.plotly_chart(fig_gender_treatment, use_container_width=True)