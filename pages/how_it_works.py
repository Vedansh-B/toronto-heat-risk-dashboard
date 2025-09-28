import streamlit as st
from theme import inject_starry_bg, footer_message, disable_sidebar_flash
import geopandas as gpd

st.set_page_config(page_title = "How It Works", layout = "wide", page_icon = "📚", initial_sidebar_state = "collapsed", menu_items = None)

disable_sidebar_flash(hide_toolbar = True)
inject_starry_bg()

# ---------- Page title ----------
st.markdown("""
<div style="
    max-width: 950px; margin: 2rem auto; text-align: center;
    background: rgba(255,255,255,0.06);
    color: #fff; padding: 1.5rem; border-radius: 14px;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 0 25px rgba(255, 150, 0, 0.3);
">
  <h1 style="margin: 0;">🧠 How This Project Works</h1>
  <p style="margin: 0.5rem 0 0; color: #ccc;">
    Peek behind the curtain of the <b>Toronto Heat Risk Explorer</b> and see how we calculate neighbourhood vulnerability.
  </p>
</div>
""", unsafe_allow_html = True)

# ---------- Methodology ----------
st.markdown("""
<div style="text-align: center; margin: 1.5rem auto; max-width: 850px;">
  <h3>📊 Methodology</h3>
  <p style="color: #ccc; font-size: 1rem; margin-bottom: 1rem;">
    This project combines <b>environmental</b> and <b>socio-demographic</b> factors into a single,
    composite <b>Heat Risk Index (HRI)</b>. All factors were normalized to a 0–1 scale and then combined
    using a weighted sum. Higher HRI values indicate <b>greater vulnerability</b>.
  </p>
</div>
""", unsafe_allow_html = True)

# --- Simple Flow Diagram ---
st.markdown("""
<div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 1rem; margin: 1rem 0 2rem;">
  
  <div style="background: rgba(255,255,255,0.08); width: 90px; height: 90px; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); text-align: center;">
    🌡<br>LST
  </div>
  
  ➕
  
  <div style="background: rgba(255,255,255,0.08); width: 90px; height: 90px; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); text-align: center;">
    🌱<br>NDVI
  </div>
  
  ➕
  
  <div style="background: rgba(255,255,255,0.08); width: 90px; height: 90px; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); text-align: center;">
    👵<br>Elderly
  </div>
  
  ➕
  
  <div style="background: rgba(255,255,255,0.08); width: 90px; height: 90px; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); text-align: center;">
    🏠<br>Living Alone
  </div>
  
  ➕
  
  <div style="background: rgba(255,255,255,0.08); width: 90px; height: 90px; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); text-align: center;">
    💸<br>Low-Income
  </div>
  
  ➡️
  
  <div style="background: rgba(255,150,0,0.2); padding: 1rem 2rem; border-radius: 10px; border: 1px solid rgba(255,150,0,0.6);">
    <b>🔥 Heat Risk Index</b>
  </div>

</div>
""", unsafe_allow_html = True)


# --- Centered Weights Table ---
st.markdown("""
<div style="text-align: center; margin-top: 1rem;">
  <h4>🎯 Applied Weights</h4>
  <table style="
    margin-left: auto;
    margin-right: auto;
    border-collapse: collapse;
    font-size: 1rem;
  ">
    <tr>
      <th style="padding: 6px 12px; border-bottom: 1px solid rgba(255,255,255,0.3);">Factor</th>
      <th style="padding: 6px 12px; border-bottom: 1px solid rgba(255,255,255,0.3);">Weight</th>
    </tr>
    <tr>
      <td style="padding: 6px 12px;">🌡 Land Surface Temperature (LST)</td>
      <td style="padding: 6px 12px;"><b>30%</b></td>
    </tr>
    <tr>
      <td style="padding: 6px 12px;">🌱 NDVI (Greenness, Inverted)</td>
      <td style="padding: 6px 12px;"><b>25%</b></td>
    </tr>
    <tr>
      <td style="padding: 6px 12px;">👵 Elderly Population (%)</td>
      <td style="padding: 6px 12px;"><b>20%</b></td>
    </tr>
    <tr>
      <td style="padding: 6px 12px;">🏠 People Living Alone (%)</td>
      <td style="padding: 6px 12px;"><b>15%</b></td>
    </tr>
    <tr>
      <td style="padding: 6px 12px;">💸 Low-Income Households (%)</td>
      <td style="padding: 6px 12px;"><b>10%</b></td>
    </tr>
  </table>
  <p style="font-size: 0.9rem; color: #ccc; margin-top: 0.5rem;">
    Satellite data covers <b>June 1 – August 31, 2024</b>, reflecting Toronto’s summer conditions.
  </p>
</div>
""", unsafe_allow_html = True)

center = st.columns([1, 6, 1])[1] 
with center:
    st.markdown("""
    <div style="text-align:center; margin: 1.25rem 0;">
      <h4 style="margin:0;">📐 Heat Risk Index Formula</h4>
      <p style="color:#ccc; font-size:0.95rem; margin:0.4rem 0 0;">
        The HRI is a weighted combination of the above normalized factors:
      </p>
    </div>
    """, unsafe_allow_html = True)

    st.latex(r"""
    HRI = w_1 \cdot LST_{norm} + w_2 \cdot (1 - NDVI_{norm})
    + w_3 \cdot Elderly_{norm} + w_4 \cdot LivingAlone_{norm}
    + w_5 \cdot LowIncome_{norm}
    """)

    st.latex(r"""
    \text{where } w_1, w_2, \dots, w_5 \text{ are the applied weights and all inputs are min-max normalized to } [0, 1].
    """)


# ---------- Data Sources ----------
st.markdown("""
<div style="text-align: center; margin: 2rem auto; max-width: 850px;">
  <h3>📚 Data Sources</h3>
  <p>All datasets were reprojected, cleaned, and spatially joined at the neighbourhood level 
  before generating the final index. All processing was done with Python.</p>
</div>
""", unsafe_allow_html = True)

st.markdown("""
<div style="text-align: center; margin: 0 auto; max-width: 700px;">
<ul style="list-style-position: inside; padding-left: 0; text-align: left; display: inline-block;">
  <li><b>🌡 MODIS LST (MOD11A1)</b> — 
      <a href="https://appeears.earthdatacloud.nasa.gov" target="_blank" style="color:#1E90FF;">
      NASA LP DAAC AppEEARS</a>, daily land surface temperature, June 1 – Aug 31, 2024.
  </li>
  <li><b>🌱 MODIS NDVI (MOD13Q1)</b> — 
      <a href="https://appeears.earthdatacloud.nasa.gov" target="_blank" style="color:#1E90FF;">
      NASA LP DAAC AppEEARS</a>, 16-day vegetation index composites for Summer 2024.
  </li>
  <li><b>🏙 Toronto Neighbourhood Boundaries</b> — 
      <a href="https://open.toronto.ca/dataset/neighbourhoods/" target="_blank" style="color:#1E90FF;">
      City of Toronto Open Data Portal</a>.
  </li>
  <li><b>👵 Demographics</b> — 
      <a href="https://open.toronto.ca/dataset/neighbourhood-profiles/" target="_blank" style="color:#1E90FF;">
      Toronto Neighbourhood Profiles (2021 Census)</a> for elderly population, low-income prevalence, 
      and single-person households.
  </li>
</ul>
</div>
""", unsafe_allow_html = True)

# ---------- Download Section ----------
st.markdown("""
<div style="text-align: center; margin: 2rem auto; max-width: 850px;">
  <h3>📥 Download Results</h3>
  <p style="color:#ccc; font-size: 1rem;">
    Download the complete neighbourhood-level <b>Heat Risk Index</b> dataset for Toronto.
  </p>
</div>
""", unsafe_allow_html = True)

try:
    gdf = gpd.read_file("data/processed/final_heat_risk_index.geojson")
    df_preview = gdf.drop(columns = "geometry").copy()

    st.markdown(
        """
        <div style="text-align: center; margin: 1rem auto; max-width: 900px;">
          <p style="font-size: 0.9rem; color:#ccc;">Preview of first 5 rows:</p>
        </div>
        """,
        unsafe_allow_html = True
    )

    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html = True)
    st.dataframe(
        df_preview.head(5).style.format(precision = 2),
        use_container_width = True
    )
    st.markdown("</div>", unsafe_allow_html = True)

    # Download button
    csv_bytes = df_preview.to_csv(index = False).encode("utf-8")
    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <a href="data:file/csv;base64,{csv_bytes.decode('latin1')}" download="toronto_heat_risk_index.csv"
                style="
                    display:inline-block;
                    padding: 0.7rem 1.5rem;
                    background: rgba(255,255,255,0.06);
                    border: 1px solid rgba(255,255,255,0.2);
                    border-radius: 12px;
                    backdrop-filter: blur(6px);
                    color: #fff;
                    text-decoration: none;
                    font-weight: bold;
                    box-shadow: 0 0 20px rgba(255, 150, 0, 0.3);
                ">
                    ⬇️ Download Heat Risk Data (CSV)
                </a>
            </div>
            """,
            unsafe_allow_html = True
        )

except FileNotFoundError:
    st.error("❌ Could not find `final_heat_risk_index.geojson`. Please check the file path.")
except Exception as e:
    st.error(f"⚠️ An unexpected error occurred while reading the GeoJSON: {e}")

# ---------- Credits ----------
st.markdown("""
<div style="text-align: center; margin: 2rem auto; max-width: 850px;">
  <h3>🤝 Acknowledgements</h3>
</div>
""", unsafe_allow_html = True)
st.markdown("""
<div style="text-align: center; margin: 1rem auto; max-width: 700px;">
  <p style="color: #aaa; font-size: 0.9rem;">
    Landing page image courtesy of 
    <a href="https://unsplash.com/@aerialshooter" target="_blank" style="color:#1E90FF;">
    Charan S / Unsplash</a>.
  </p>
</div>
""", unsafe_allow_html = True)

st.markdown("""
<div style="display: flex; justify-content: center; gap: 1.5rem; margin-top: 2rem;">

  <!-- Home Button -->
  <a href="/app" target="_self" style="
      background: rgba(255,255,255,0.06);
      color: white;
      padding: 0.7rem 1.5rem;
      border-radius: 12px;
      text-decoration: none;
      font-weight: bold;
      border: 1px solid rgba(255,255,255,0.2);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      box-shadow: 0 0 20px rgba(255, 150, 0, 0.3);
      transition: all 0.2s ease-in-out;">
      🏠 Home
  </a>

  <!-- Launch Explorer Button -->
  <a href="/explore_map" target="_self" style="
      background: rgba(255,255,255,0.06);
      color: white;
      padding: 0.7rem 1.5rem;
      border-radius: 12px;
      text-decoration: none;
      font-weight: bold;
      border: 1px solid rgba(255,255,255,0.2);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      box-shadow: 0 0 20px rgba(255, 150, 0, 0.3);
      transition: all 0.2s ease-in-out;">
      🗺️ Launch Heat Risk Explorer
  </a>

</div>
""", unsafe_allow_html = True)

footer_message()