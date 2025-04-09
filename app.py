import streamlit as st
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Mental Health Dashboard",
    layout="wide",
    page_icon="favicon.png"
)

# Load Mental Health Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mental_health_dataset.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce") 
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

st.sidebar.title("Occupation Filter")
occupation = st.sidebar.multiselect(
    "Select Occupation",
    options=df["Occupation"].unique(),
)

st.sidebar.title("Time Range Filter")
min_date = df["Timestamp"].min().date()
max_date = df["Timestamp"].max().date()

start_date = st.sidebar.date_input(
    "Start Date", min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "End Date", max_date, min_value=min_date, max_value=max_date
)

if start_date > end_date:
    st.sidebar.error("Start date can't be after end date")
    st.stop()

# Default Filters
if not gender:
    gender = df["Gender"].unique()
if not country:
    country = df["Country"].unique()
if not occupation:
    occupation = df["Occupation"].unique()

df_selection = df[
    df["Gender"].isin(gender) &
    df["Country"].isin(country) & 
    df["Occupation"].isin(occupation) &
    (df["Timestamp"].dt.date >= start_date) &
    (df["Timestamp"].dt.date <= end_date)
    ]

# Title and Description
st.title("Mental Health Dashboard")
st.write("""
Welcome to this interactive dashboard analyzing mental health data. Explore demographics and mental health insights across various factors such as gender, country and occupation.
Use the tabs below to navigate through different sections.
""")

# Data Cleaning
df["self_employed"] = df["self_employed"].fillna("Not specified")
df["care_options"] = df["care_options"].replace("Not sure", "Maybe")

#------------ Visualization ------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([":bar_chart: Overview", ":earth_africa: Demographics", ":brain: Mental Health Insights", ":briefcase: Work-Related Insights", ":pill: Treatment and Care"])

#--------- Tab 1: Overview ---------
with tab1:
    st.header("Overview")

    # Overall Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Responses", df_selection.shape[0])

    with col2:
        st.metric("Countries Represented", df_selection["Country"].nunique())

    with col3:
        st.metric("Occupations", df_selection[df_selection["Occupation"] != "Others"]["Occupation"].nunique())

    with col4:
        st.metric("Years Covered", f"{df_selection['Year'].min()} - {df_selection['Year'].max()}")

    st.divider()

    # Participation By Year Over Time (Line Chart)
    response_by_year = df.groupby("Year").size().reset_index(name="Total_Responses")

    fig_time = px.line(response_by_year,
                       x="Year", y="Total_Responses",
                       title="Participation Over Time",
                       labels={"Year": "Year", "Total_Responses": "Number of Respondents"},
                       markers=True)
    st.plotly_chart(fig_time, use_container_width=True)
    st.caption("This line chart shows how survey participation has changed over the years. You can see which years had the highest engagement and how participation trends evolved.")

#--------- Tab 2: Demographics ---------
with tab2:
    st.header("Demographics")

    # Country Distribution (Choropleth Map)
    response_by_country = df_selection.groupby("Country").size().reset_index(name="Total_Responses")
    fig_map = px.choropleth(response_by_country,
                            locations="Country",
                            locationmode="country names",
                            color="Total_Responses",
                            hover_name="Country",
                            title="Country Distribution",
                            color_continuous_scale=px.colors.sequential.Blues,
                            labels={"Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("This map shows the global distribution of survey respondents. Darker colors indicate countries with more participants. The visualization helps identify which regions are most represented, and it suggests areas where mental health awareness or survey access may be higher.")
    st.divider()

    # Gender Distribution (Pie Chart)
    response_by_gender = df_selection.groupby("Gender").size().reset_index(name="Total_Responses")

    fig_gender = px.pie(response_by_gender,
                        names="Gender",
                        values="Total_Responses",
                        title="Gender Distribution")
    
    st.plotly_chart(fig_gender, use_container_width=True)
    st.caption("This pie chart shows the gender breakdown of respondents. The chart highlights whether the survey had a balanced gender representation, revealing potential disparities that could influence the interpretation of mental health trends.")

#--------- Tab 3: Mental Health Insights ---------
with tab3:
    st.header("Mental Health Insights")

    # History of Mental Health Distribution (Bar chart)
    response_by_mental_health_history = df_selection.groupby("Mental_Health_History").size().reset_index(name="Total_Responses")
    fig_mental_health_history = px.bar(response_by_mental_health_history,
                                       x="Mental_Health_History", y="Total_Responses", 
                                       title="Mental Health History Distribution",
                                       labels={"Mental_Health_History": "History of Mental Health", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_mental_health_history, use_container_width=True)
    st.caption("This bar chart shows the distribution of respondents who have a history of mental health issues. It helps illustrate how common mental health challenges are within this survey group.")
    st.divider()

    # Family History Distribution (Bar Chart)
    response_by_family_history = df_selection.groupby("family_history").size().reset_index(name="Total_Responses")
    fig_family_history = px.bar(response_by_family_history,
                                x="family_history", y="Total_Responses",
                                title="Family History of Mental Illness Distribution",
                                labels={"family_history": "Family History", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_family_history, use_container_width=True)
    st.caption("This chart shows how many respondents have a family history of mental illness. It offers insights into the potential hereditary factors of mental health struggles.")
    st.divider()

    # Mental Health Interview Distribution (Pie Chart)
    response_by_interview = df_selection.groupby("mental_health_interview").size().reset_index(name="Total_Responses")
    fig_interview = px.pie(response_by_interview,
                           names="mental_health_interview",
                           values="Total_Responses",
                           title="Mental Health Interview Distribution",
                           labels={"mental_health_interview": "Mental Health Interview", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_interview, use_container_width=True)
    st.caption("This pie chart shows the proportion of respondents who have had a mental health interview. It gives insight into how often respondents have sought professional help.")
    st.divider()

    # Growing Stress Distribution (Bar chart)
    response_by_stress_levels = df_selection.groupby("Growing_Stress").size().reset_index(name="Total_Responses")
    fig_stress_levels = px.bar(response_by_stress_levels,
                               x="Growing_Stress", y="Total_Responses",
                               title="Growing Stress Distribution",
                               labels={"Growing_Stress": "Growing Stress", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_stress_levels, use_container_width=True)
    st.caption("This bar chart shows the number of respondents reporting growing levels of stress. It highlights the prevalence of stress within the survey group.")
    st.divider()

    # Mood Swings Distribution (Bar chart)
    response_by_mood_swings = df_selection.groupby("Mood_Swings").size().reset_index(name="Total_Responses")
    fig_mood_swings = px.bar(response_by_mood_swings,
                            x="Mood_Swings", y="Total_Responses",
                            title="Mood Swings Distribution",
                            labels={"Mood_Swings": "Mood Swings", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_mood_swings, use_container_width=True)
    st.caption("This bar chart shows the distribution of respondents who experience mood swings. It offers insights into how common mood swings are in this survey group.")
    st.divider()

    # Social Weakness Distribution (Bar chart)
    response_by_social_weakness = df_selection.groupby("Social_Weakness").size().reset_index(name="Total_Responses")
    fig_social_weakness = px.bar(response_by_social_weakness,
                                 x="Social_Weakness", y="Total_Responses",
                                 title="Social Weakness Distribution",
                                 labels={"Social_Weakness": "Social Weakness", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_social_weakness, use_container_width=True)
    st.caption("This bar chart shows how many respondents report experiencing social weakness. It helps to identify the prevalence of social difficulties among the participants.")
    st.divider()

    # Days Indoors Distribution (Bar chart)
    response_by_days_indoors = df_selection.groupby("Days_Indoors").size().reset_index(name="Total_Responses")
    fig_days_indoors = px.bar(response_by_days_indoors,
                              x="Days_Indoors", y="Total_Responses",
                              title="Days Indoors Distribution",
                              labels={"Days_Indoors": "Days Indoors", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_days_indoors, use_container_width=True)
    st.caption("This bar chart shows the number of days respondents spend indoors. It helps analyze how indoor activity may affect mental health.")
    st.divider()

    # Coping Struggles Distribution (Bar chart)
    response_by_coping_struggles = df_selection.groupby("Coping_Struggles").size().reset_index(name="Total_Responses")
    fig_coping_struggles = px.bar(response_by_coping_struggles,
                                  x="Coping_Struggles", y="Total_Responses",
                                  title="Coping Struggles Distribution",
                                  labels={"Coping_Struggles": "Coping Struggles", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_coping_struggles, use_container_width=True)
    st.caption("This bar chart shows how many respondents are struggling with coping. It highlights the extent of coping difficulties in this group.")

    st.divider()

    # Days Indoors vs Coping Struggles (Heatmap)
    response_by_days_indoors = df_selection.groupby(["Days_Indoors", "Coping_Struggles"]).size().reset_index(name="Total_Responses")
    fig_indoors_coping = px.density_heatmap(response_by_days_indoors,
                                            x="Days_Indoors", y="Coping_Struggles",
                                            z="Total_Responses",
                                            title="Correlation Between Days Spent Indoors and Coping Struggles",
                                            labels={"Days_Indoors": "Days Indoors", "Coping_Struggles": "Coping Struggles", "Total_Responses": "respondents"},
                                            color_continuous_scale=px.colors.sequential.Blues)

    st.plotly_chart(fig_indoors_coping, use_container_width=True)
    st.caption("This heatmap shows the correlation between the number of days spent indoors and coping struggles. It helps identify how indoor activity might be related to mental health difficulties.")
    st.divider()

    # Regional Differences in Coping Struggles (Choropleth)
    response_by_country_coping = df_selection[df_selection["Coping_Struggles"] == "Yes"].groupby("Country").size().reset_index(name="Total_Responses")
    top_10_countries = response_by_country_coping.sort_values(by="Total_Responses", ascending=False).head(10)
    fig_country_coping = px.choropleth(response_by_country_coping,
                                       locations="Country",
                                       locationmode="country names",
                                       color="Total_Responses",
                                       hover_name="Country",
                                       title="Regional Differences in Coping Struggles",
                                       color_continuous_scale=px.colors.sequential.Blues,
                                       labels={"Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_country_coping, use_container_width=True)
    st.caption("This map highlights the regional differences in coping struggles, showing which countries report the highest levels of difficulty.")
    st.divider()

    # Complementary Bar Chart Showing The Top 10 Countries Struggling (Bar Chart) - Kan vi lägga denna side to side till den ovan
    fig_top_10_countries = px.bar(top_10_countries, 
                                  x="Country", y="Total_Responses",
                                  title="Top 10 Countries with Highest Coping Struggles", 
                                  labels={"Country": "Country", "Total_Responses": "Number of Struggles"})

    st.plotly_chart(fig_top_10_countries, use_container_width=True)
    st.caption("This bar chart complements the chart above, showing the top 10 countries where respondents report the most coping struggles. It provides insight into regional mental health challenges.")
    st.divider()

    # Habit Changes Distribution (Bar chart)
    response_by_changes_habits = df_selection.groupby("Changes_Habits").size().reset_index(name="Total_Responses")
    fig_changes_habits = px.bar(response_by_changes_habits,
                                x="Changes_Habits", y="Total_Responses",
                                title="Habit Changes Distribution",
                                labels={"Changes_Habits": "Changes in Habits", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_changes_habits, use_container_width=True)
    st.caption("This bar chart shows the distribution of respondents who have experienced changes in habits. It helps to identify how common these changes are in the group.")
    st.divider()

    # Habit Changes vs Coping Struggles (Stacked Bar Chart)
    response_by_habit_changes = df_selection.groupby(["Changes_Habits", "Coping_Struggles"]).size().reset_index(name="Total_Responses")
    fig_habit_changes = px.bar(response_by_habit_changes,
                               x="Changes_Habits", y="Total_Responses",
                               color="Coping_Struggles",
                               title="Correlation Between Habit Changes and Coping Struggles",
                               labels={"Changes_Habits": "Changes in Habits", "Total_Responses": "Number of Respondents"},
                               barmode="stack")

    st.plotly_chart(fig_habit_changes, use_container_width=True)
    st.caption("This stacked bar chart shows the relationship between habit changes and coping struggles. It highlights how changes in behavior may relate to mental health difficulties.")
    st.divider()

    # Mood Swings vs Gender (Grouped Bar Chart)
    response_by_mood_swings = df_selection.groupby(["Gender", "Mood_Swings"]).size().reset_index(name="Total_Responses")
    fig_mood_swings = px.bar(response_by_mood_swings,
                             x="Gender", y="Total_Responses",
                             color="Mood_Swings",
                             title="Correlation Between Gender and Mood Swings",
                             labels={"Gender": "Gender", "Total_Responses": "Number of Respondents"},
                             barmode="group")

    st.plotly_chart(fig_mood_swings, use_container_width=True)
    st.caption("This grouped bar chart shows the relationship between gender and mood swings. It offers insight into whether certain genders report more mood swings.")
    st.divider()

    # Family History vs Mood Swings (Bar Chart)
    response_by_family_mood_swings = df_selection.groupby(["family_history", "Mood_Swings"]).size().reset_index(name="Total_Responses")
    fig_family_mood_swings = px.bar(response_by_family_mood_swings,
                                    x="family_history", y="Total_Responses",
                                    color="Mood_Swings",
                                    title="Correlation Between Family History and Mood Swings",
                                    labels={"family_history": "Family History", "Mood_Swings": "Mood Swings", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_family_mood_swings, use_container_width=True)
    st.caption("This stacked bar chart shows the relationship between family history of mental illness and mood swings. It highlights potential hereditary factors influencing mood swings.")

#--------- Tab 4: Work-Related Insights ---------
with tab4:
    st.header("Work-Related Insights")    
    
    # Occupation Distribution (Bar Chart)
    response_by_occupation = df_selection.groupby("Occupation").size().reset_index(name="Total_Responses").sort_values(by="Total_Responses", ascending=False)
    fig_occupation = px.bar(response_by_occupation,
                            x="Occupation", y="Total_Responses",
                            title="Occupation Distribution",
                            labels={"Occupation": "Occupation", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_occupation, use_container_width=True)
    st.caption("This chart breaks down respondents by occupation. It highlights which professions are most represented in the survey and helps provide context for analyzing mental health trends by job role.")
    st.divider()

    # Self-Employment Distribution (Bar Chart)
    df_filtered = df_selection[df_selection["self_employed"] != "Not specified"]
    response_by_self_employment = df_filtered.groupby("self_employed").size().reset_index(name="Total_Responses").sort_values(by="Total_Responses", ascending=False)
    fig_self_employed = px.bar(response_by_self_employment,
                               x="self_employed", y="Total_Responses",
                               title="Self-Employment Distribution",
                               labels={"self_employed": "Self-Employment Status", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_self_employed, use_container_width=True)
    st.caption("This chart shows the distribution of self-employed respondents. It highlights the prevalence of self-employment in the survey group and its potential link to mental health.")
    st.divider()

    # Work Interest Distribution (Bar chart)
    response_by_work_interest = df_selection.groupby("Work_Interest").size().reset_index(name="Total_Responses")
    fig_work_interest = px.bar(response_by_work_interest,
                            x="Work_Interest", y="Total_Responses",
                            title="Work Interest Distribution",
                            labels={"Work_Interest": "Work Interest", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_work_interest, use_container_width=True)
    st.caption("This chart shows the distribution of respondents interest in their work. It helps provide insight into how work engagement may influence mental health.")
    st.divider()

    # Occupations with the Highest Stress Levels (Horizontal Bar Chart)
    response_by_occupation_stress = df_selection[df_selection["Growing_Stress"] == "Yes"].groupby("Occupation").size().reset_index(name="Total_Responses")
    response_by_occupation_stress = response_by_occupation_stress.sort_values(by="Total_Responses", ascending=True)
    fig_occupation_stress = px.bar(response_by_occupation_stress,
                                   x="Total_Responses", y="Occupation",
                                   title="Occupations with the Highest Stress Levels",
                                   labels={"Total_Responses": "Number of Respondents", "Occupation": "Occupation"})

    st.plotly_chart(fig_occupation_stress, use_container_width=True)
    st.caption("This bar chart highlights which occupations report the highest levels of stress. It helps identify which job roles may be more prone to mental health struggles due to work-related stress.")

#--------- Tab 5: Treatment and Care ---------
with tab5:
    st.header("Treatment and Care")

    # Treatment Status Distribution (Bar chart)
    response_by_treatment = df_selection.groupby("treatment").size().reset_index(name="Total_Responses")
    fig_treatment = px.bar(response_by_treatment,
                           x="treatment", y="Total_Responses",
                           title="Treatment Status Distribution",
                           labels={"treatment": "Treatment Status", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_treatment, use_container_width=True)
    st.caption("This bar chart shows how many respondents have received mental health treatment. It helps understand the level of engagement with mental health care among survey participants.")
    st.divider()

    # Care Options Distribution (Pie Chart)
    response_by_interview = df_selection.groupby("care_options").size().reset_index(name="Total_Responses")
    fig_interview = px.pie(response_by_interview,
                        names="care_options",
                        values="Total_Responses",
                        title="Care Options Distribution",
                        labels={"care_options": "Care Options", "Total_Responses": "Number of Respondents"})

    st.plotly_chart(fig_interview, use_container_width=True)
    st.caption("This pie chart shows the distribution of mental health care options available to respondents. It highlights the availability of care resources.")
    st.divider()

    # Care Options Distribution by country (Choropleth map)
    response_by_care_options = df_selection.groupby(["Country", "care_options"]).size().reset_index(name="Total_Responses")
    fig_care_options = px.choropleth(response_by_care_options,
                                    locations="Country", 
                                    locationmode="country names",
                                    color="care_options", 
                                    hover_name="Country",
                                    hover_data={"Total_Responses": True},  # Adding total responses to hover
                                    title="Access to Mental Health Care Options by Country",
                                    color_continuous_scale=px.colors.sequential.Blues,
                                    labels={"care_options": "Care Options", "Total_Responses": "Number of Respondents"})
    
    st.plotly_chart(fig_care_options, use_container_width=True)
    st.caption("This map highlights access to mental health care options by country. It helps identify regions with better access to care and areas where care might be lacking. It's important to note that some countries may have mixed responses, so this reflects the dominant opinion, not all opinions.")
    st.divider()

    # Gender vs Treatment (Stacked Bar Chart)
    response_by_gender_treatment = df_selection.groupby(["Gender", "treatment"]).size().reset_index(name="Total_Responses")
    fig_gender_treatment = px.bar(response_by_gender_treatment, 
                                  x="Gender", y="Total_Responses",
                                  color="treatment",
                                  title="Correlation Between Gender and Mental Health Treatment",
                                  labels={"Gender": "Gender", "Total_Responses": "Number of Respondents"},
                                  barmode="stack")

    st.plotly_chart(fig_gender_treatment, use_container_width=True)
    st.caption("This chart shows the relationship between gender and engagement with mental health treatment. It provides insights into whether certain genders are more likely to seek help and receive treatment.")
    st.divider()

    # Treatment vs Mood Swings (Stacked Bar chart)
    response_by_treatment_mood_swings = df_selection.groupby(["treatment", "Mood_Swings"]).size().reset_index(name="Total_Responses")
    fig_treatment_mood_swings = px.bar(response_by_treatment_mood_swings,
                                       x="treatment", y="Total_Responses", 
                                       color="Mood_Swings",
                                       title="Correlation Between Mental Health Treatment and Mood Swings",
                                       labels={"treatment": "Treatment", "Mood_Swings": "Mood Swings", "Total_Responses": "Number of Respondents"},
                                       barmode="stack")

    st.plotly_chart(fig_treatment_mood_swings, use_container_width=True)
    st.caption("This chart shows how receiving mental health treatment relates to mood swings. It helps to assess whether treatment has an impact on emotional stability.")
    st.divider()

    # Treatment vs Family History of Mental Illness (Stacked Bar Chart)
    response_by_family_history = df_selection.groupby(["treatment", "family_history"]).size().reset_index(name="Total_Responses")
    fig_family_history = px.bar(response_by_family_history,
                                x="treatment", y="Total_Responses",
                                color="family_history",
                                title="Correlation Between Family History of Mental Illness and Treatment",
                                labels={"family_history": "Family History of Mental Illness", "treatment": "Treatment", "Total_Responses": "Number of Respondents"},
                                barmode="stack")

    st.plotly_chart(fig_family_history, use_container_width=True)
    st.caption("This chart explores the relationship between a family history of mental illness and receiving treatment. It offers insight into how genetic factors may influence the decision to seek help.")