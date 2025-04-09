import streamlit as st
import warnings
import kagglehub
import pandas as pd
import os 
import plotly.express as px
import pydeck as pdk

warnings.simplefilter(action='ignore', category=FutureWarning)
st.title("Maps")
st.markdown("Contains interactive maps to support exploration of the National Parks in the United States.")

path_species = kagglehub.dataset_download("nationalparkservice/park-biodiversity")
files_species = os.listdir(path_species)
csv_file_species = [f for f in files_species if f.endswith(".csv")][0]
parks_geo_df = pd.read_csv(os.path.join(path_species, csv_file_species))

csv_url = "https://raw.githubusercontent.com/melaniewalsh/responsible-datasets-in-context/main/datasets/national-parks/US-National-Parks_Use_1979-2023_By-Month.csv"
parks_visit_df = pd.read_csv(csv_url)

merged_df = pd.merge(parks_visit_df, parks_geo_df, how='left', left_on='UnitCode', right_on='Park Code')

# region_df = merged_df[['ParkName', 'UnitCode', 'Region', 'State_x', 'Latitude', 'Longitude']].drop_duplicates()

# st.write(merged_df.head())

col1, col2, col3 = st.columns(3)

with col1:
    filter_by_region = st.multiselect("Filter by the region of United States:", merged_df['Region'].unique())
    if not filter_by_region:
        filter_by_region = merged_df['Region'].unique()
    filtered_region_df = merged_df[merged_df['Region'].isin(filter_by_region)]

with col3:
    filter_by_year =  st.slider("Filter by year: ", filtered_region_df["Year"].min(), filtered_region_df["Year"].max(), (filtered_region_df["Year"].min(), filtered_region_df["Year"].max()))
    min_year, max_year = filter_by_year
    filtered_by_year = filtered_region_df[(filtered_region_df['Year']>=min_year) & (filtered_region_df['Year']<=max_year)]
    

total_visitors_per_park = (
    filtered_by_year
    .groupby(['ParkName', 'UnitCode', 'Latitude', 'Longitude'], as_index=False)['RecreationVisits']
    .sum()
    .rename(columns={'RecreationVisits': 'TotalVisitors'})
)
total_visitors_per_park['TotalVisitors'] = total_visitors_per_park['TotalVisitors'] / 1_000_000


min_visits = total_visitors_per_park['TotalVisitors'].min()
max_visits = total_visitors_per_park['TotalVisitors'].max()
total_visitors_per_park['point_size'] = (
    (total_visitors_per_park['TotalVisitors'] - min_visits) / (max_visits - min_visits + 1e-9)
) * 100000

layer = pdk.Layer(
    "ScatterplotLayer",
    total_visitors_per_park,
    get_position=["Longitude", "Latitude"],
    get_fill_color=[255, 0, 0, 140],  # Red color for the points
    get_radius='point_size',  # Adjust the radius of the points
    pickable=True,  # Make the points pickable for interaction
    auto_highlight=True  # Highlight the points when hovered
)

deck = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=39.8283,  # Latitude for the middle of the US
        longitude=-98.5795,  # Longitude for the middle of the US
        zoom=3,  # Zoom level
        pitch=0,
        transition_duration=500  # Smooth transition (in ms)
    ),
    layers=[layer],
    tooltip={
       "html": "<b>{ParkName}</b><br>Visitors: {TotalVisitors} million",
        "style": {"color": "white"}
    },
    map_style="mapbox://styles/mapbox/streets-v11"  # Set the default map style (e.g., streets)
)

st.pydeck_chart(deck)