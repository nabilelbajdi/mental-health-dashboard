# Mental Health Dashboard

An interactive data visualization tool built with Streamlit and Plotly that analyzes mental health survey data to uncover demographic patterns and insights.

## Project Overview

This dashboard analyzes a comprehensive mental health dataset to identify trends and patterns in mental health experiences across different demographics, regions, and occupations. The interactive dashboard allows users to filter data by various parameters and explore visualizations that reveal insights about:

- Global and demographic distribution of mental health concerns
- Correlations between lifestyle factors and mental health outcomes
- Impact of work environments and occupations on mental health
- Treatment access and efficacy patterns

## Features

- **Interactive Filtering**: Filter data by gender, country, occupation, and time period
- **Multi-tab Organization**: Explore different aspects of mental health data through organized tabs
- **Diverse Visualizations**: Analyze data through maps, charts, and interactive graphs
- **Real-time Calculations**: See statistics updated in real-time based on your filtering choices

## Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Interactive web application framework
- **Plotly**: Advanced interactive visualizations
- **Data Analysis**: Statistical analysis and data insights

## Getting Started

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/nabilelbajdi/mental-health-dashboard.git
   cd mental-health-dashboard
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```
   streamlit run app.py
   ```

## Data Source

The analysis is based on an anonymized mental health survey dataset from Kaggle: [Mental Health Dataset](https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset). The dataset contains responses about mental health experiences, work environments, and treatment access, including demographic information that allows for segmentation and comparative analysis.

## Project Structure

```
mental-health-dashboard/
├── app.py                      # Main Streamlit dashboard application
├── mental_health_dataset.csv   # Dataset used for analysis
├── favicon.png                 # Dashboard icon
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Future Improvements

- Add machine learning models to predict mental health risks based on demographics and behaviors
- Expand dataset with more recent survey data
- Add sentiment analysis of open-ended responses
- Develop additional visualizations focused on treatment efficacy

## License

This project is open source and available for personal and educational use.
