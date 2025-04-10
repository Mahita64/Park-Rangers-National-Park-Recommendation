import streamlit as st
import warnings
import kagglehub
import pandas as pd
import os 
import plotly.express as px
import pydeck as pdk

warnings.simplefilter(action='ignore', category=FutureWarning)
st.title("Top Parks")
st.markdown("Contains interactive dashboard that recommends the top parks to visit based on user preferences. For now, we have startd with a partial implementation of the idea")



path_species = kagglehub.dataset_download("nationalparkservice/park-biodiversity")
files_species = os.listdir(path_species)
csv_file_species = [f for f in files_species if f.endswith(".csv")][0]
parks_geo_df = pd.read_csv(os.path.join(path_species, csv_file_species))

csv_url = "https://raw.githubusercontent.com/melaniewalsh/responsible-datasets-in-context/main/datasets/national-parks/US-National-Parks_Use_1979-2023_By-Month.csv"
parks_visit_df = pd.read_csv(csv_url)

merged_df = pd.merge(parks_visit_df, parks_geo_df, how='left', left_on='UnitCode', right_on='Park Code')


# st.write(merged_df.head())

# st.write(merged_df.columns)



st.markdown("### 🎛️ Filter Parks by Your Preferences")


filtered_df = merged_df.dropna(subset=["ParkName", "ParkType", "Region", "State_x", "Acres", "Latitude", "Longitude"])


states = sorted(filtered_df["State_x"].dropna().unique())
park_types = sorted(filtered_df["ParkType"].dropna().unique())
regions = sorted(filtered_df["Region"].dropna().unique())
years = sorted(filtered_df["Year"].dropna().unique())
months = sorted(filtered_df["Month"].dropna().unique())

selected_states = st.multiselect("Select State(s)", states, default=states[:3])


col1, col2 = st.columns(2)
with col1:
    selected_years = st.select_slider("Select Year Range", options=years, value=(2015, 2023))
with col2:
    selected_months = st.multiselect("Select Month(s)", months, default=months)

st.markdown("#### ⛺ Activity Preferences")
camp_col1, camp_col2, camp_col3 = st.columns(3)
with camp_col1:
    tent_camping = st.checkbox("Tent Camping")
with camp_col2:
    rv_camping = st.checkbox("RV Camping")
with camp_col3:
    backcountry = st.checkbox("Backcountry Camping")

filtered_df = filtered_df[
    (filtered_df["State_x"].isin(selected_states)) &
    (filtered_df["Year"] >= selected_years[0]) &
    (filtered_df["Year"] <= selected_years[1]) &
    (filtered_df["Month"].isin(selected_months))
]

if tent_camping:
    filtered_df = filtered_df[filtered_df["TentCampers"] > 0]
if rv_camping:
    filtered_df = filtered_df[filtered_df["RVCampers"] > 0]
if backcountry:
    filtered_df = filtered_df[filtered_df["Backcountry"] > 0]

filtered_df["Latitude"] = pd.to_numeric(filtered_df["Latitude"], errors="coerce")
filtered_df["Longitude"] = pd.to_numeric(filtered_df["Longitude"], errors="coerce")

map_df = filtered_df.dropna(subset=["Latitude", "Longitude"])
map_df = map_df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})
if not map_df.empty:
    st.markdown("### 🗺️ Parks Map View with Hover Info")

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=pdk.ViewState(
            latitude=map_df["latitude"].mean(),
            longitude=map_df["longitude"].mean(),
            zoom=4,
            pitch=30,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_df,
                get_position='[longitude, latitude]',
                get_radius=40000,
                get_fill_color='[0, 128, 255, 160]',
                pickable=True,
            )
        ],
        tooltip={
            "html": "<b>{ParkName}</b><br/>Region: {Region}<br/>State: {State_x}<br/>Acres: {Acres}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }
    ))
else:
    st.warning("No parks with valid coordinates to show on the map.")



st.markdown("### 🌟 Top Parks by Recreation Visits")
top_parks = (
    filtered_df.groupby("ParkName")["RecreationVisits"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
if not top_parks.empty:
    fig = px.bar(
        top_parks, 
        x="RecreationVisits",
        y="ParkName",
        orientation="h",
        title="Top 10 Parks by Recreation Visits",
        labels={"RecreationVisits": "Visits", "ParkName": "Park"},
        color="ParkName",  
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data to display after filtering.")


st.markdown("### 📊 Recreation Visits Trend for a Selected Park")
unique_parks = filtered_df["ParkName"].dropna().unique()
selected_park = st.selectbox("Choose a Park", sorted(unique_parks))
park_monthly_visits = (
    filtered_df[filtered_df["ParkName"] == selected_park]
    .groupby("Month")["RecreationVisits"]
    .mean()
    .reset_index()
)
fig = px.line(
    park_monthly_visits,
    x="Month",
    y="RecreationVisits",
    markers=True,
    title=f"Average Monthly Recreation Visits - {selected_park}",
    labels={"RecreationVisits": "Avg Visits", "Month": "Month"}
)
st.plotly_chart(fig, use_container_width=True)



st.markdown("### 🏆 Best Month to Visit Each Park")
best_month_df = (
    filtered_df.groupby(["ParkName", "Month"])["RecreationVisits"]
    .mean()
    .reset_index()
)
best_month_per_park = best_month_df.loc[
    best_month_df.groupby("ParkName")["RecreationVisits"].idxmax()
]
best_month_per_park["Month"] = best_month_per_park["Month"].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
best_month_per_park_reset = best_month_per_park.reset_index(drop=True)
best_month_per_park_reset = best_month_per_park_reset.rename(columns={"Month": "Best Month", "RecreationVisits": "Avg Visits"})
best_month_per_park_reset_sorted = best_month_per_park_reset.sort_index(ascending=True)
st.dataframe(best_month_per_park_reset_sorted, use_container_width=True)



st.markdown("### 🔥 Heatmap of Monthly Visits by State")
state_month = (
    filtered_df.groupby(["State_x", "Month"])["RecreationVisits"]
    .sum()
    .reset_index()
)
state_month = state_month.rename(columns={"State_x": "State"})
state_month["Month"] = state_month["Month"].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
heatmap_fig = px.density_heatmap(
    state_month,
    x="Month",
    y="State",
    z="RecreationVisits",
    color_continuous_scale="Viridis",
    title="Recreation Visits by State and Month",
    labels={"RecreationVisits": "Visits"}
)
st.plotly_chart(heatmap_fig, use_container_width=True)



# st.markdown("### 🏕️ Based on Preferred Activity")
# top_parks_activity = (
#     filtered_df.groupby("ParkName")["RecreationVisits"]
#     .sum()
#     .sort_values(ascending=False)
#     .head(10)
#     .reset_index()
# )
# fig = px.bar(
#     top_parks_activity,
#     x="RecreationVisits",
#     y="ParkName",
#     orientation="h",
#     title="Top 10 Parks by Recreation Visits (Filtered by Activity)",
#     labels={"RecreationVisits": "Visits", "ParkName": "Park"},
#     color="ParkName",  
#     color_discrete_sequence=px.colors.qualitative.Set3
# )
# fig.update_layout(showlegend=False)
# st.plotly_chart(fig, use_container_width=True)


