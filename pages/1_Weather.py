import streamlit as st
import pandas as pd
import altair as alt
import warnings
import warnings
import plotly.express as px
import pydeck as pdk

warnings.simplefilter(action='ignore', category=FutureWarning)
st.title("Weather Trends")

st.header("Exploring National Parks Weather")

merged_df = pd.read_csv("merged_weather_park_data.csv")

# st.write(merged_df)

# First find the 5 most popular parks
top_5_parks = merged_df.groupby('ParkName')['RecreationVisits'].sum().nlargest(5).index.tolist()

# st.write(top_5_parks)

df_top5 = merged_df[merged_df['ParkName'].isin(top_5_parks)]

# st.write(df_top5.head())

# Create a multiselect widget with default values selected as the top 5 parks
selected_parks = st.multiselect(
    "Select parks to explore weather",
    options=merged_df["ParkName"].unique(),
    default=top_5_parks
)

st.subheader("1. 🌡️ Average monthly temperature")
# Filter the df based on the selected parks, and use that for visualization
filtered_df = merged_df[merged_df['ParkName'].isin(selected_parks)]


month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

filtered_df['MonthName'] = filtered_df['Month'].map(lambda x: month_names[x-1])

# Chart of average monthly temperature for each park over the last 30 years
temp_chart = alt.Chart(filtered_df).mark_line().encode(
    x=alt.X('MonthName:N', sort=month_names, axis=alt.Axis(title="Month", labelAngle=0)),
    y=alt.Y('average(AvgTemp):Q', title="Average temperature over last 30 years (C)"),
    color='ParkName:N'
).properties(width=600)

st.altair_chart(temp_chart)

# Find the most popular destinations for every temperature
st.subheader("2. 🌡️ Temperature vs Visitation (Which parks are popular when the temperature is within some range?)")

min_temp = float(filtered_df['AvgTemp'].min()) if not filtered_df['AvgTemp'].isnull().all() else 0
max_temp = float(filtered_df['AvgTemp'].max()) if not filtered_df['AvgTemp'].isnull().all() else 100

# Create a slider to accept a temperature range
temp_range = st.slider(
    "Temperature Range (°C)", 
    min_temp, 
    max_temp, 
    (min_temp, max_temp),
    help="Select temperature range for visitation analysis"
)

# Filter DataFrame based on selected temperature range
qualifying = filtered_df[
    (filtered_df["AvgTemp"] >= temp_range[0]) & 
    (filtered_df["AvgTemp"] <= temp_range[1])
]

base = alt.Chart(qualifying).encode(
    x=alt.X(
        'AvgTemp:Q', 
        title="Average Temperature (°C)",
        scale=alt.Scale(domain=[temp_range[0], temp_range[1]])
    ),
    y=alt.Y('RecreationVisits:Q', title="Visit Count")
)

scatter = base.mark_circle(size=60).encode(
    color='ParkName:N',
    tooltip=[
        alt.Tooltip('ParkName:N'),
        alt.Tooltip('Month:N'),
        alt.Tooltip('AvgTemp:Q', format='.1f'),
        alt.Tooltip('RecreationVisits:Q', format=',')
    ]
)

st.altair_chart(scatter, use_container_width=True)