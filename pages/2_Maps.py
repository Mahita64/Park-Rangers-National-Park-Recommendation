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

airports_df = pd.read_csv('parks_and_airports.csv')

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
    
airports_df = airports_df[airports_df['Park Code'].isin(filtered_region_df['UnitCode'].unique())]
total_visitors_per_park = (
    filtered_by_year
    .groupby(['ParkName', 'UnitCode', 'Latitude', 'Longitude'], as_index=False)['RecreationVisits']
    .sum()
    .rename(columns={'RecreationVisits': 'TotalVisitors'})
)
total_visitors_per_park['TotalVisitors'] = total_visitors_per_park['TotalVisitors'] / 1_000_000
total_visitors_per_park = total_visitors_per_park.merge(
    airports_df, how='left', left_on='UnitCode', right_on='Park Code'
)

min_visits = total_visitors_per_park['TotalVisitors'].min()
max_visits = total_visitors_per_park['TotalVisitors'].max()
total_visitors_per_park['point_size'] = (
    (total_visitors_per_park['TotalVisitors'] - min_visits) / (max_visits - min_visits + 1e-9)
) * 100000

total_visitors_per_park["tooltip_text"] = (
    total_visitors_per_park["ParkName"] +
    "<br><b>Visitors:</b> " + total_visitors_per_park["TotalVisitors"].round(2).astype(str) + " million" + 
    "<br><b>Nearest Airport:</b> " + total_visitors_per_park["nearest_airport_name"].fillna("N/A")
)

airports_df["tooltip_text"] = (
    "<b>Airport:</b> " + airports_df["nearest_airport_name"].fillna("N/A")
)
airports_df["icon_data"] = airports_df.apply(
    lambda row: {
        "url": "https://img.icons8.com/?size=100&id=43122&format=png&color=000000",
        "width": 128,
        "height": 128,
        "anchorY": 128  # Aligns the bottom of the icon to the coordinate point
    },
    axis=1
)

layer = pdk.Layer(
    "ScatterplotLayer",
    total_visitors_per_park,
    get_position=["Longitude_x", "Latitude_x"],
    get_fill_color=[255, 0, 0, 140],  # Red color for the points
    get_radius='point_size',  # Adjust the radius of the points
    pickable=True,  # Make the points pickable for interaction
    auto_highlight=True,  # Highlight the points when hovered
)

airport_layer = pdk.Layer(
    type="IconLayer",
    data=airports_df,
    get_icon="icon_data",
    get_size=3,
    size_scale=5,
    get_position=["airport_lon", "airport_lat"],
    pickable=True,
    auto_highlight=True
)

total_visitors_per_park["path"] = total_visitors_per_park.apply(
    lambda row: [[row["Longitude_x"], row["Latitude_x"]], [row["airport_lon"], row["airport_lat"]]],
    axis=1
)

line_layer = pdk.Layer(
    type="PathLayer",
    data=total_visitors_per_park,
    pickable=True,
    get_color=[138, 43, 226, 200],  # Purple lines
    width_scale=20,
    width_min_pixels=2,
    get_path="path",
    get_width=20,
)

deck = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=39.8283,  # Latitude for the middle of the US
        longitude=-98.5795,  # Longitude for the middle of the US
        zoom=3,  # Zoom level
        pitch=0,
        transition_duration=500  # Smooth transition (in ms)
    ),
    layers=[layer, airport_layer, line_layer],
    tooltip={
        "html": "{tooltip_text}",
        "style": {"color": "white"}
    },
    map_style="mapbox://styles/mapbox/streets-v11"  # Set the default map style (e.g., streets)
)

st.pydeck_chart(deck)