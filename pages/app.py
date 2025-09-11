import streamlit as st
import geopandas as gpd
import pydeck as pdk
import pandas as pd
import folium
from branca.colormap import linear
from streamlit_folium import st_folium

def load_data(filename: str):
    return gpd.read_file(filename)

gdf = load_data("../data/processed/elderly_data.geojson")
colour_by = "Elderly Distribution"

gdf[colour_by] = pd.to_numeric(gdf[colour_by], errors = "coerce") # casts retrieved strings to numbers. improper conversion -> NaN
gdf = gdf.dropna(subset = [colour_by])

min_val = gdf[colour_by].min()
max_val = gdf[colour_by].max()

colour_map = linear.YlOrRd_09.scale(min_val, max_val)
colour_map.caption = "Heat Risk Index"

city_map = folium.Map(location = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean(),], zoom_start = 11)

folium.GeoJson(
    gdf, 
    style_function = lambda feature: {
        "fillColor": colour_map(feature["properties"][colour_by]),
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.7,
    },
    tooltip = folium.GeoJsonTooltip(fields = [colour_by], aliases = ["Heat Risk: "])
).add_to(city_map)

colour_map.add_to(city_map)

st.title("Urban Heat Risk Explorer")
st_data = st_folium(city_map, width = 800, height = 600)

# # Add the legend
# colormap.add_to(m)

# # Display in Streamlit
# st.title("Urban Heat Risk Explorer")
# st_data = st_folium(m, width=800, height=600)
