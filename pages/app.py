import streamlit as st
import geopandas as gpd
import pydeck as pdk
import pandas as pd

st.set_page_config(layout="wide")
st.title("🗺️ Toronto Urban Heat Risk Explorer")
st.markdown("This interactive map shows the distribution of elderly residents across Toronto neighborhoods — a key vulnerability factor for heat risk.")

# Load data
@st.cache_data
def load_data():
    return gpd.read_file("../data/elderly_data.geojson")

gdf = load_data()

# Check geometry
if gdf.empty or gdf.geometry.isnull().all():
    st.error("GeoDataFrame is empty or missing geometry.")
    st.stop()

# Convert to WGS84 if needed
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")

# Create pydeck layer
layer = pdk.Layer(
    "GeoJsonLayer",
    data = gdf,
    get_fill_color = '[255, 100, 100, 140]',
    pickable = True,
    auto_highlight = True
)

initial_view = pdk.ViewState(
    latitude = 56.0,
    longitude = -96.0,
    zoom = 3.5,
    pitch = 0
)

view_state = pdk.ViewState(
    latitude = gdf.geometry.centroid.y.mean(),
    longitude = gdf.geometry.centroid.x.mean(),
    zoom = 10,
    pitch = 0
)

# Display
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{Neighbourhood}\nElderly %: {Elderly Distribution}"}))
