import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
from theme import inject_starry_bg

st.set_page_config(page_title="Toronto Heat Risk Explorer", layout="wide")
inject_starry_bg()

gdf = gpd.read_file("data/processed/final_heat_risk_index.geojson")

# Ensure proper CRS
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=4326)
elif gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs(epsg=4326)

rename_map = {
    "HRI": "Heat Risk Index",
    "LST": "Land Surface Temperature",
    "NDVI": "Normalized Difference Vegetation Index",
    "Elderly": "Elderly Population (%)",
    "LowIncome": "Low-Income Households (%)",
    "LivingAlone": "Living Alone (%)",
}
gdf = gdf.rename(columns={k: v for k, v in rename_map.items() if k in gdf.columns})

name_col = "Neighbourhood" if "Neighbourhood" in gdf.columns else "neighborhood"
gdf[name_col] = gdf[name_col].str.strip()

# Ensure numerics are numeric
for c in rename_map.values():
    if c in gdf.columns:
        gdf[c] = pd.to_numeric(gdf[c], errors="coerce")

st.markdown("""
<div style="
    max-width: 950px; margin: 1rem auto; text-align: center;
    background: rgba(255,255,255,0.06);
    color: #fff; padding: 1.5rem; border-radius: 14px;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 0 25px rgba(255, 150, 0, 0.3);
">
  <h1 style="margin: 0;">🔥 Toronto Heat Risk Explorer</h1>
  <p style="margin: 0.5rem 0 0; color: #ccc;">
    Explore neighbourhood-level <b>heat vulnerability</b> across Toronto using multiple metrics.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    div[data-testid="stRadio"] {
        display: flex;
        justify-content: center;
        margin-top: 0.5rem;
    }
    div[data-testid="stRadio"] label p {
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown(
        """
        <div style="
            max-width: 950px; margin: 0.5rem auto 1rem auto; text-align: center;
            background: rgba(255,255,255,0.06);
            color: #fff; padding: 1rem; border-radius: 14px;
            backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 0 25px rgba(255, 150, 0, 0.3); /* same glow as title */
        ">
            <h4 style="margin: 0; font-size: 1.1rem; text-align: center;">
                🎨 Colour the Map By
            </h4>
        """,
        unsafe_allow_html=True
    )

    metric = st.radio(
        "Choose a metric to color the map by",
        ["Heat Risk Index", "Land Surface Temperature", "Normalized Difference Vegetation Index"],
        horizontal=True,
        label_visibility="collapsed",
        key="metric_selector"
    )

    st.markdown("</div>", unsafe_allow_html=True)



# Heat risk colour palette (green = low; red = high)
vals = gdf[metric].dropna().to_numpy()
vmin, vmax = float(np.nanmin(vals)), float(np.nanmax(vals))
if metric == "Normalized Difference Vegetation Index":
    # special case NDVI: green = good, brown = bad
    cmap = LinearColormap(
        colors = ["#a50026", "#f46d43", "#fee08b", "#1a9850"], 
        vmin = vmin, vmax = vmax
    )
else:
    cmap = LinearColormap(
        colors = ["#1a9850", "#fee08b", "#f46d43", "#d73027"],  
        vmin = vmin, vmax = vmax
    )

def color_for(v):
    if pd.isna(v):
        return "#cccccc"
    return cmap(v)

def build_map(gdf, metric, name_col, color_for, zoom_to=None):
    center = [43.7, -79.4] # Toronto bounds
    zoom = 11
    if zoom_to is not None: # zoom to selected neighbourhood
        bounds = gdf[gdf[name_col] == zoom_to].total_bounds
        center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
        zoom = 14 
 
    m = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB Positron")

    gdf["metric_display"] = gdf[metric].round(2)

    gj = GeoJson(
        data=gdf.__geo_interface__,
        style_function=lambda f: {
            "fillColor": color_for(f["properties"].get(metric)),
            "color": "#333",
            "weight": 0.6,
            "fillOpacity": 0.9,
        },
        highlight_function=lambda f: {"weight": 2, "color": "#000", "fillOpacity": 0.95},
        tooltip=GeoJsonTooltip(fields=[name_col, "metric_display"], aliases=["Neighbourhood:", metric]),
    ).add_to(m)

    if zoom_to:
        bounds = gdf[gdf[name_col] == zoom_to].total_bounds  # [minx, miny, maxx, maxy]
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]], max_zoom=14)

    return m

vals = gdf[metric].dropna().to_numpy()
vmin, vmax = float(np.nanmin(vals)), float(np.nanmax(vals))

if metric == "Normalized Difference Vegetation Index":
    cmap = LinearColormap(colors=["#a50026", "#f46d43", "#fee08b", "#1a9850"], vmin=vmin, vmax=vmax)
else:
    cmap = LinearColormap(colors=["#1a9850", "#fee08b", "#f46d43", "#d73027"], vmin=vmin, vmax=vmax)

def color_for(v):
    return "#ccc" if pd.isna(v) else cmap(v)

neighbourhoods = sorted(gdf[name_col].dropna().unique())
selected_neigh = st.session_state.get("selected_neigh", "-- Select --")

zoom_target = selected_neigh if selected_neigh != "-- Select --" else None
m = build_map(gdf, metric, name_col, color_for, zoom_to=zoom_target)

st_folium(m, height=720, use_container_width=True, key="mainmap")

new_selection = st.selectbox(
    "Neighbourhood",
    ["-- Select --"] + list(neighbourhoods),
    index=(["-- Select --"] + list(neighbourhoods)).index(selected_neigh)
    if selected_neigh in neighbourhoods else 0,
    label_visibility="collapsed"
)

if new_selection != selected_neigh:
    st.session_state.selected_neigh = new_selection
    st.rerun()  # map rerender with zoom

if selected_neigh and selected_neigh != "-- Select --":
    props = gdf[gdf[name_col] == selected_neigh].iloc[0].to_dict()

    st.markdown("---")
    st.markdown(f"### 📍 {props.get(name_col)}")

    cols = st.columns(3)
    fmt = lambda x: "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.2f}"

    with cols[0]:
        st.metric("Normalized Heat Risk Index", fmt(props.get("Heat Risk Index")))
        st.metric("Normalized NDVI (mean)", fmt(props.get("Normalized Difference Vegetation Index")))

    with cols[1]:
        st.metric("LST (°C)", fmt(props.get("Land Surface Temperature")))
        st.metric("Elderly (%)", fmt(props.get("Elderly Population (%)")))

    with cols[2]:
        st.metric("Low Income (%)", fmt(props.get("Low-Income Households (%)")))
        st.metric("Living Alone (%)", fmt(props.get("Living Alone (%)")))
else:
    st.caption("Select a neighbourhood to view its metrics.")


st.markdown("---")
st.markdown("### 📊 Neighbourhood Rankings")

if metric in gdf.columns:
    df_sorted = gdf[[name_col, metric]].dropna()

    if metric == "Normalized Difference Vegetation Index":
        # Sort ascending for bottom 5 (least vegetated first)
        df_sorted = df_sorted.sort_values(by=metric, ascending=True)
    else:
        df_sorted = df_sorted.sort_values(by=metric, ascending=False)

    col_high, col_low = st.columns(2)

if metric in gdf.columns:
    df_sorted = gdf[[name_col, metric]].dropna()

    if metric == "Normalized Difference Vegetation Index":
        # For NDVI, high = good
        df_sorted = df_sorted.sort_values(by=metric, ascending=True)

        col_high, col_low = st.columns(2)

        with col_high:
            st.markdown(f"**Top 5 – Best Vegetation (High NDVI)** 🌳")
            top5 = df_sorted.tail(5).sort_values(by=metric, ascending=False).reset_index(drop=True)
            st.dataframe(
                top5.style.format({metric: "{:.2f}"}).background_gradient(
                    subset=[metric], cmap="Greens"
                ),
                use_container_width=True,
                hide_index=True,
            )

        with col_low:
            st.markdown(f"**Bottom 5 – Sparse Vegetation (Low NDVI)** 🌵")
            bottom5 = df_sorted.head(5).reset_index(drop=True)
            st.dataframe(
                bottom5.style.format({metric: "{:.2f}"}).background_gradient(
                    subset=[metric], cmap="Reds_r"  # reversed so lowest = darkest red
                ),
                use_container_width=True,
                hide_index=True,
            )

    else:
        df_sorted = df_sorted.sort_values(by=metric, ascending=False)

        col_high, col_low = st.columns(2)

        with col_high:
            st.markdown(f"**Top 5 – Highest {metric}** 🔥")
            top5 = df_sorted.head(5).reset_index(drop=True)
            st.dataframe(
                top5.style.format({metric: "{:.2f}"}).background_gradient(
                    subset=[metric], cmap="Reds"
                ),
                use_container_width=True,
                hide_index=True,
            )

        with col_low:
            st.markdown(f"**Top 5 – Lowest {metric}** 🌱")
            bottom5 = df_sorted.tail(5).sort_values(by=metric, ascending=True).reset_index(drop=True)
            st.dataframe(
                bottom5.style.format({metric: "{:.2f}"}).background_gradient(
                    subset = [metric], cmap = "Greens_r"  # reversed so lowest = darkest green
                ),
                use_container_width=True,
                hide_index=True,
            )
else:
    st.warning(f"No data available for {metric}")
