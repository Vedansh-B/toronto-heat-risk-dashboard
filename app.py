import streamlit as st
from streamlit.components.v1 import html
from PIL import Image
from theme import inject_starry_bg, footer_message

st.set_page_config(
    page_title="Urban Heat Risk Explorer",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


inject_starry_bg()
html("""
<div id="particles-js" style="position: fixed; width: 100%; height: 100%; top: 0; left: 0; z-index: -1;"></div>

<!-- Include particles.js from CDN -->
<script src="https://cdn.jsdelivr.net/npm/particles.js"></script>

<script>
  particlesJS("particles-js", {
    "particles": {
      "number": {
        "value": 100,
        "density": {
          "enable": true,
          "value_area": 800
        }
      },
      "color": { "value": "#ffffff" },
      "shape": { "type": "circle" },
      "opacity": {
        "value": 0.6,
        "random": true,
        "anim": { "enable": true, "speed": 1, "opacity_min": 0.2 }
      },
      "size": {
        "value": 3,
        "random": true
      },
      "move": {
        "enable": true,
        "speed": 0.2,
        "direction": "none",
        "out_mode": "out"
      }
    }
  });
</script>
""")

st.markdown("""
<div style="display: flex; justify-content: center; margin-top: 3rem; margin-bottom: 3rem;">
  <div style="
    max-width: 950px;
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, rgba(0,0,20,0.4) 0%, rgba(0,30,50,0.4) 100%);
    color: #fff;
    padding: 2rem;
    border-radius: 16px;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 0 25px rgba(0, 150, 255, 0.3);
  ">
    <h1 style="margin-top: 0; font-size: 2.5rem;">🌌 Urban Heat Risk Explorer</h1>
    <p style="font-size: 1.2rem; line-height: 1.5; max-width: 80%; margin: 0 auto; color: #bbb;">
      An interactive look at Toronto's neighbourhood-level vulnerability to urban heat
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div style="
            max-width: 950px;
            width: 100%;
            text-align: center;
            background: linear-gradient(135deg, rgba(0,0,20,0.4) 0%, rgba(0,30,50,0.4) 100%);
            color: #fff;
            padding: 2rem;
            border-radius: 16px;
            backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 25px rgba(0, 150, 255, 0.3);
        ">
        <h2 style="text-align: center; margin-top: 0;">🌍 <b>Why This Project Exists</b></h2>
        <ul style="list-style-type: disc; text-align: left; line-height: 1.8; font-size: 1.1rem; max-width: 85%; margin: 0 auto;">
            <li><b>Premise:</b> 🌡️ Urban heat is a growing challenge that affects all of us, especially those in <u>vulnerable communities</u>.
            <li><b>Goal:</b> ✅ Make climate data <b>accessible</b> and <b>actionable</b> by combining <b>satellite imagery</b>, <b>climate indicators</b>, and <b>social vulnerability metrics</b> into one place.</li>
            <li><b>Audience:</b> 🌱 Designed for <b>residents</b>, <b>researchers</b>, and <b>decision-makers</b> who wish to <b>drive meaningful change</b>.</li>
            <li><b>Personal mission:</b> 🚀 Apply my skills in <b>data and analytics</b> to <i>make a difference</i> in the lives of real people.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("data/raw/charan-s-SYoCXP3JHiE-unsplash.jpg", caption="Toronto from above, Summer", use_container_width=True)

st.markdown("---")

st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
  <h2 style="margin-bottom: 0.3rem;">🚀 Ready to Explore?</h2>
  <p style="margin-top: 0; font-size: 1.1rem; color: #ccc;">
    Click below to begin visualizing Toronto’s heat vulnerability or learn how it works.
  </p>
</div>

<div style="display: flex; justify-content: center; align-items:center; gap: 2rem; flex-wrap: wrap; margin-top: 1rem;">
  <a class="glass-btn" href="/explore_map" target="_self">
    🗺️ Launch Heat Risk Explorer
  </a>
  <a class="glass-btn" href="/how_it_works" target="_self">
    🧠 See Methodology
  </a>
</div>

<style>
.glass-btn {
  display: inline-block;                
  background: rgba(255, 255, 255, 0.08);
  padding: 0.8rem 1.6rem;
  border-radius: 12px;
  text-decoration: none !important;
  font-weight: bold;
  color: white !important;             
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 4px 20px rgba(0, 150, 255, 0.25);
  transition: transform .2s ease, box-shadow .2s ease, background .2s ease;
  text-align: center;
  cursor: pointer;
}
.glass-btn:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  box-shadow: 0 6px 25px rgba(0, 150, 255, 0.4) !important;
  transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

footer_message()
