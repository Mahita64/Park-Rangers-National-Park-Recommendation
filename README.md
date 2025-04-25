[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/z4O17nG5)
# IDS Final Project: National Park Visitation Analysis & Recommender System

* **Team members**:
  * Contact person: aditisai@andrew.cmu.edu
  * aangadi@andrew.cmu.edu
  * mkandala@andrew.cmu.edu
  * rupsad@andrew.cmu.edu

## Work distribution

1. Exploratory Data Analysis & Map Visualizations: Aditi Saini
2. Interactive Visualizations & Recommendation UI: Rupsa Dhar
3. Weather Data Integration and Visualizations: Ananya Prabhu Angadi
4. Clustering & Recommendation System: Mahita Kandala

## Instructions to run locally

```bash
python3 -m venv venv  
source venv/bin/activate  
pip install --upgrade pip  
pip install -r requirements.txt  
streamlit run ./Park_Rangers.py  
```

## Abstract

US National Parks are rich areas of biodiversity conservation and tourism. However, some parks are more well-known, and receive greater visitation on average. Hence, there is a need to bridge the gap, and boost the visitation numbers of less-frequented parks. To address this, we have built an interactive Streamlit dashboard combining visitation analysis with a questionnaire-guided recommendation system. Our goals are to provide a unified portal to explore everything US National Parks-related. We facilitate park comparisons based on several metrics, enable users to easily locate nearby airports, offer weather trends and biodiversity information to aid in decision making. We also highlight overall trends to support policymakers. Lastly, we have incorporated a questionnaire-driven clustering algorithm, to help users find parks that align with their preferences.

To do this, we have integrated data from several sources - national park visitation numbers, historical weather data, geospatial and airports-related information, as well as biodiversity data. We then used Altair and Plotly to present this data in an interactive and user-friendly format. We also built a simple K-Means clustering algorithm to help users find parks they will enjoy visiting. Future work includes social media sentiment analysis, dynamic clustering based on real-time weather, and incorporating socio-economic accessibility factors.

## Project Process

This project taught us the value of collaboration, communication, and team bonding. We effectively resolved conflicts by listening and aligning on shared goals. Working together on data integration, visualization, and recommendations strengthened our teamwork. The experience not only enhanced our technical skills but also our ability to work cohesively as a unit.

## Links

### [Proposal](Proposal.md)
### [Final Report](Report.md)
### [Video](https://drive.google.com/file/d/1JbkVSzpqqGHfC3Mc_M_1BUze4MjxiZL_/view?usp=sharing)
