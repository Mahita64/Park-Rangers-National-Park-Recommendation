import streamlit as st
import warnings
import kagglehub
import pandas as pd
import os 
import plotly.express as px
import pydeck as pdk
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)
st.title("Top Parks")
st.markdown("Contains interactive dashboard that recommends the top parks to visit based on user preferences.")

# Load and prepare data
path_species = kagglehub.dataset_download("nationalparkservice/park-biodiversity")
files_species = os.listdir(path_species)
csv_file_species = [f for f in files_species if f.endswith(".csv")][0]

parks_visit_df = pd.read_csv("/Users/mahitakandala/Desktop/IDS/final-project-s25-parkrangers/merged_weather_park_data.csv")
airport_df = pd.read_csv('/Users/mahitakandala/Desktop/IDS/final-project-s25-parkrangers/parks_and_airports.csv')

# Merge datasets
merged_df = pd.merge(
    parks_visit_df,
    airport_df[['Park Code', 'nearest_airport_name', 'airport_lat', 'airport_lon', 'airport_state', 'distance_km']],
    on='Park Code',
    how='left'
)

columns_to_keep = [
    'UnitCode', 'ParkType', 'Region', 'Year', 'Month', 
    'RecreationVisits', 'NonRecreationVisits', 'TentCampers', 'RVCampers', 'Backcountry',
    'Park Code', 'Park Name', 'State', 'Acres', 'Latitude', 'Longitude',
    'AvgTemp', 'MinTemp', 'MaxTemp', 'Precipitation', 'Snowfall', 'WindSpeed', 'Pressure', 'Sunshine',
    'nearest_airport_name', 'airport_lat', 'airport_lon', 'airport_state', 'distance_km'
]

df = merged_df[columns_to_keep]

month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

st.title("🏞️ Find Your Ideal National Park Adventure")

# User input section
st.subheader("Your Travel Preferences")

region = st.selectbox("📍 Select Region", ['Northeast', 'Pacific West', 'Southeast', 'Intermountain', 'Midwest', 'Alaska'])
month = st.selectbox("🗓️ When do you want to go?", ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
activities = st.multiselect(
    "⛺ Select Camping Activities You Enjoy",
    ['TentCampers', 'RVCampers', 'Backcountry']
)

st.subheader("🌍 Environment Preferences")

temp_preference = st.selectbox(
    "🌡️ Select your preferred temperature range:",
    ["Doesn't matter", "❄️ Very Cold", "🧥 Cold", "🌤️ Mild", "☀️ Warm", "🔥 Hot"]
)

precip_preference = st.selectbox(
    "💧 Select your preferred precipitation level:",
    ["Doesn't matter", "🌵 Dry", "🌿 Moderate", "🌧️ Wet"]
)

distance_preference = st.selectbox(
    "✈️ Select your preferred distance to airport:",
    ["Doesn't matter", "🏙️ Close to airport", "🚗 Can travel a bit", "🏞️ Okay with remote travel"]
)

# Define category mappings
temp_preference_map = {
    "Doesn't matter": None,  
    "❄️ Very Cold": -5,
    "🧥 Cold": 5,
    "🌤️ Mild": 15,
    "☀️ Warm": 25,
    "🔥 Hot": 35
}

precip_preference_map = {
    "Doesn't matter": None,  
    "🌵 Dry": 10,
    "🌿 Moderate": 40,
    "🌧️ Wet": 80
}

distance_preference_map = {
    "Doesn't matter": None,  
    "🏙️ Close to airport": 30,
    "🚗 Can travel a bit": 100,
    "🏞️ Okay with remote travel": 200
}

# Data preparation
df = df[df['Year'] >= 2010].copy()

numeric_cols = [
    'RecreationVisits', 'TentCampers', 'RVCampers', 'Backcountry',
    'AvgTemp', 'Precipitation', 'Snowfall', 'WindSpeed', 'distance_km'
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Aggregate data by park
agg_df = df.groupby('Park Name').agg({
    'RecreationVisits': 'mean',
    'TentCampers': 'mean',
    'RVCampers': 'mean',
    'Backcountry': 'mean',
    'AvgTemp': 'mean',
    'Precipitation': 'mean',
    'Snowfall': 'mean',
    'WindSpeed': 'mean',
    'distance_km': 'mean',
    'Region': 'first',
    'Latitude': 'first',
    'Longitude': 'first',
    'State': 'first'
}).reset_index()

# Create monthly visitation profiles
monthly = df.groupby(['Park Name', 'Month'])['RecreationVisits'].mean().reset_index()
monthly_pivot = monthly.pivot(index='Park Name', columns='Month', values='RecreationVisits').fillna(0)

month_map = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
monthly_pivot.columns = [month_map[m] for m in monthly_pivot.columns]

# Normalize to get percentage of annual visits per month
monthly_pivot = monthly_pivot.div(monthly_pivot.sum(axis=1), axis=0).fillna(0)

# Merge all features
features_df = agg_df.merge(monthly_pivot, left_on='Park Name', right_index=True)

# Create camping flags
features_df['TentCampers_flag'] = (features_df['TentCampers'] > 1000).astype(int)
features_df['RVCampers_flag'] = (features_df['RVCampers'] > 1000).astype(int)
features_df['Backcountry_flag'] = (features_df['Backcountry'] > 1000).astype(int)

# Prepare features for clustering - IMPORTANT: exclude string columns like 'Region'
X = features_df.drop(columns=['Park Name', 'RecreationVisits', 'TentCampers', 'RVCampers',
                             'Backcountry', 'Snowfall', 'WindSpeed', 'Latitude', 'Longitude', 'State', 'Region']).copy()

# Functions for categorization
def categorize_temp(temp):
    if pd.isna(temp):
        return "Unknown"
    if temp <= 0:
        return "❄️ Very Cold"
    elif temp <= 10:
        return "🧥 Cold"
    elif temp <= 20:
        return "🌤️ Mild"
    elif temp <= 30:
        return "☀️ Warm"
    else:
        return "🔥 Hot"

def categorize_precip(p):
    if pd.isna(p):
        return "Unknown"
    if p <= 20:
        return "🌵 Dry"
    elif p <= 60:
        return "🌿 Moderate"
    else:
        return "🌧️ Wet"

def categorize_distance(d):
    if pd.isna(d):
        return "Unknown"
    if d <= 50:
        return "🏙️ Close to airport"
    elif d <= 150:
        return "🚗 Can travel a bit"
    else:
        return "🏞️ Okay with remote travel"

# Function to find nearest parks
def find_nearest_parks(user_features, park_features, all_parks_df, n=5):
    """Find the n nearest parks to user preferences based on Euclidean distance"""
    distances = []
    
    # Calculate Euclidean distance between user preferences and each park
    for i, park_feature in enumerate(park_features[:-1]):  # Exclude the user
        distance = np.linalg.norm(park_feature - user_features)
        distances.append((i, distance))
    
    # Sort by distance
    distances.sort(key=lambda x: x[1])
    
    # Return the nearest parks dataframe
    nearest_indices = [idx for idx, _ in distances[:n]]
    return all_parks_df.iloc[nearest_indices].copy()

# Create user preference data with only the numerical/flag columns (no Region)
user_data = {
    'Jan': 1 if month == 'Jan' else 0,
    'Feb': 1 if month == 'Feb' else 0,
    'Mar': 1 if month == 'Mar' else 0,
    'Apr': 1 if month == 'Apr' else 0,
    'May': 1 if month == 'May' else 0,
    'Jun': 1 if month == 'Jun' else 0,
    'Jul': 1 if month == 'Jul' else 0,
    'Aug': 1 if month == 'Aug' else 0,
    'Sep': 1 if month == 'Sep' else 0,
    'Oct': 1 if month == 'Oct' else 0,
    'Nov': 1 if month == 'Nov' else 0,
    'Dec': 1 if month == 'Dec' else 0,
    'AvgTemp': temp_preference_map[temp_preference],
    'Precipitation': precip_preference_map[precip_preference],
    'distance_km': distance_preference_map[distance_preference],
    'TentCampers_flag': 1 if 'TentCampers' in activities else 0,
    'RVCampers_flag': 1 if 'RVCampers' in activities else 0,
    'Backcountry_flag': 1 if 'Backcountry' in activities else 0
}

# Handle "Doesn't matter" preferences
if user_data['AvgTemp'] is None:
    user_data['AvgTemp'] = X['AvgTemp'].median()
    
if user_data['Precipitation'] is None:
    user_data['Precipitation'] = X['Precipitation'].median()
    
if user_data['distance_km'] is None:
    user_data['distance_km'] = X['distance_km'].median()

# Create user DataFrame
user_df = pd.DataFrame([user_data])

# Ensure we're using the same columns for user data as for park data
user_clustering_features = pd.DataFrame()
for col in X.columns:
    if col in user_df.columns:
        user_clustering_features[col] = user_df[col]
    else:
        user_clustering_features[col] = X[col].median()

# Combine for scaling
combined_features = pd.concat([X, user_clustering_features], ignore_index=True)

# Fill missing values
numeric_cols = combined_features.select_dtypes(include=['float64', 'int64']).columns
combined_features[numeric_cols] = combined_features[numeric_cols].fillna(combined_features[numeric_cols].median())

# Scale data for clustering
scaler = StandardScaler()
features_scaled = scaler.fit_transform(combined_features)

# Apply clustering
k = 10  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
labels = kmeans.fit_predict(features_scaled)

# Assign clusters
features_df['Cluster'] = labels[:-1]  # All except the last one (user)
user_cluster = labels[-1]

# Find nearest parks based on Euclidean distance
user_features = features_scaled[-1]  # Get the user feature vector
nearest_parks = find_nearest_parks(user_features, features_scaled, features_df, n=5)




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


# =============================================================================================================
# Create a visualization of clusters with PCA
# st.subheader("🔍 Visualizing Your Position in Park Clusters")
# st.write("This visualization shows how your preferences relate to different park groups:")

# # Use PCA to reduce dimensions for visualization
# pca = PCA(n_components=2)
# features_scaled_2d = pca.fit_transform(features_scaled)

# # Create a DataFrame for plotting
# plot_df = pd.DataFrame({
#     'PCA1': features_scaled_2d[:, 0],
#     'PCA2': features_scaled_2d[:, 1],
#     'Cluster': labels,
#     'Type': ['Park'] * (len(features_scaled_2d) - 1) + ['Your Preferences']
# })

# # Create a custom color map for clusters with enough colors for all clusters
# cluster_colors = {}
# color_palette = px.colors.qualitative.Bold
# for i in range(k):
#     cluster_colors[i] = color_palette[i % len(color_palette)]

# # Create a scatter plot with Plotly
# fig = px.scatter(
#     plot_df[plot_df['Type'] == 'Park'],  # Just the parks first
#     x='PCA1',
#     y='PCA2',
#     color='Cluster',
#     color_discrete_map=cluster_colors,
#     title='Park Clusters and Your Preferences',
#     labels={'PCA1': 'Component 1', 'PCA2': 'Component 2'},
#     opacity=0.7
# )

# # Add user point separately with a distinct style
# user_point = plot_df[plot_df['Type'] == 'Your Preferences']
# fig.add_trace(
#     px.scatter(
#         user_point, 
#         x='PCA1', 
#         y='PCA2',
#     ).update_traces(
#         marker=dict(
#             color='black',
#             size=20,
#             symbol='star',
#             line=dict(width=2, color='black')
#         )
#     ).data[0]
# )

# # Highlight parks in the user's cluster with a distinct border
# parks_in_user_cluster = plot_df[(plot_df['Type'] == 'Park') & (plot_df['Cluster'] == user_cluster)]
# fig.add_trace(
#     px.scatter(
#         parks_in_user_cluster,
#         x='PCA1',
#         y='PCA2',
#     ).update_traces(
#         marker=dict(
#             size=12,
#             symbol='circle',
#             line=dict(width=2, color='black'),
#             color=cluster_colors[user_cluster]
#         )
#     ).data[0]
# )

# # Add annotations
# fig.add_annotation(
#     x=user_point['PCA1'].values[0],
#     y=user_point['PCA2'].values[0],
#     text="Your Preferences",
#     showarrow=True,
#     arrowhead=2,
#     arrowsize=1,
#     arrowwidth=2,
#     ax=40,
#     ay=-40,
#     font=dict(size=14, color='black')
# )

# # Update layout for white background and better styling
# fig.update_layout(
#     plot_bgcolor='white',
#     paper_bgcolor='white',
#     legend_title_text='Cluster',
#     height=600,
#     margin=dict(l=20, r=20, t=40, b=20),
#     font=dict(family="Arial", size=12, color="black"),
#     xaxis=dict(
#         showgrid=True,
#         gridcolor='lightgray',
#         zeroline=True,
#         zerolinecolor='lightgray'
#     ),
#     xaxis_title=dict(
#         font=dict(family="Arial", size=14, color="black")
#     ),
#     yaxis=dict(
#         showgrid=True,
#         gridcolor='lightgray',
#         zeroline=True,
#         zerolinecolor='lightgray'
#     ),
#     yaxis_title=dict(
#         font=dict(family="Arial", size=14, color="black")
#     ),
#     title=dict(
#         font=dict(family="Arial", size=18, color="black")
#     )
# )

# # Show the plot
# st.plotly_chart(fig, use_container_width=True)

# # Add explanation text
# st.markdown(f"""
# This chart shows how your preferences relate to different park clusters:
# - Each dot represents a park, colored by its cluster
# - The **black star** shows where your preferences fall
# - Parks in your cluster (Cluster {user_cluster}) have a black outline
# - Parks that are closer to your preferences are more similar to what you're looking for
# """)

# =============================================================================================================


# Display the nearest parks on a map
st.subheader("🗺️ Map of Your Best Matching Parks")

# Check if we have geographic coordinates
if not nearest_parks.empty and not nearest_parks['Latitude'].isna().any():
    park_locations = nearest_parks[['Park Name', 'Latitude', 'Longitude', 'State']].copy()
    park_locations['size'] = 75000  # Consistent marker size
    
    view_state = pdk.ViewState(
        latitude=park_locations["Latitude"].mean(),
        longitude=park_locations["Longitude"].mean(),
        zoom=3,
        pitch=0
    )
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=park_locations,
        get_position=['Longitude', 'Latitude'],
        get_radius='size',
        get_fill_color=[255, 105, 180],
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True
    )
    
    tooltip = {
        "html": "<b>{Park Name}</b><br>State: {State}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    ))
else:
    st.warning("Location data not available for the recommended parks.")

# Show detailed information about each recommended park
st.subheader("📋 Detailed Park Information")

# For each of the nearest parks, show more details
for i, (idx, park) in enumerate(nearest_parks.iterrows()):
    with st.expander(f"{i+1}. {park['Park Name']} ({park['State']})"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Region:** {park['Region']}")
            
            # Show temperature info
            temp_category = categorize_temp(park['AvgTemp'])
            st.markdown(f"**Temperature:** {temp_category} ({park['AvgTemp']:.1f}°C)")
            
            # Show precipitation info
            precip_category = categorize_precip(park['Precipitation'])
            st.markdown(f"**Precipitation:** {precip_category} ({park['Precipitation']:.1f} mm)")
        
        
        with col2:
            # Show best months
            month_values = [park[m] for m in month_map.values()]
            best_month_idx = np.argmax(month_values)
            best_month = list(month_map.values())[best_month_idx]
            
            st.markdown(f"**Best month to visit:** {best_month}")
            
            # Show camping options
            camping_options = []
            if park['TentCampers_flag'] == 1:
                camping_options.append("⛺ Tent Camping")
            if park['RVCampers_flag'] == 1:
                camping_options.append("🚐 RV Camping")
            if park['Backcountry_flag'] == 1:
                camping_options.append("🥾 Backcountry")
                
            st.markdown(f"**Available activities:** {', '.join(camping_options) if camping_options else 'Limited camping options'}")
            
            # Show recreation visits
            st.markdown(f"**Average annual visits:** {park['RecreationVisits']:,.0f}")
                    # Show distance info
            distance_category = categorize_distance(park['distance_km'])
        st.markdown(f"**Distance from airport:** {distance_category} ({park['distance_km']:.1f} km)")

