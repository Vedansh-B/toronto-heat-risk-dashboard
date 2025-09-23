import streamlit as st

def inject_starry_bg():
    st.markdown("""
    <style>
    /* Let our background show through Streamlit containers */
    html, body { background:#000; }
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    .block-container, main, .stApp { background: transparent !important; }

    /* Two fixed parallax layers of subtle stars */
    #starfield, #starfield2 {
      position: fixed; inset: 0; z-index: -1; pointer-events: none; background-repeat: repeat;
    }
    #starfield {
      background-image:
        radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,.9) 50%, transparent 52%),
        radial-gradient(1.5px 1.5px at 80px 70px, rgba(255,255,255,.8) 50%, transparent 52%),
        radial-gradient(1.5px 1.5px at 60px 20px, rgba(255,255,255,.85) 50%, transparent 52%),
        radial-gradient(1px 1px at 40px 80px, rgba(255,255,255,.7) 50%, transparent 52%),
        radial-gradient(1px 1px at 140px 120px, rgba(255,255,255,.75) 50%, transparent 52%),
        radial-gradient(1.5px 1.5px at 100px 160px, rgba(255,255,255,.8) 50%, transparent 52%),
        radial-gradient(2px 2px at 50px 200px, rgba(255,255,255,.85) 50%, transparent 52%);
      background-size: 200px 200px, 240px 240px, 320px 320px, 280px 280px, 360px 360px, 300px 300px, 400px 400px;
      animation: driftA 120s linear infinite;
      opacity: .6;
    }
    #starfield2 {
      background-image:
        radial-gradient(1.2px 1.2px at 30px 60px, rgba(255,255,255,.6) 50%, transparent 52%),
        radial-gradient(1.2px 1.2px at 10px 10px, rgba(255,255,255,.55) 50%, transparent 52%),
        radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,.5) 50%, transparent 52%),
        radial-gradient(.8px .8px at 70px 90px, rgba(255,255,255,.45) 50%, transparent 52%),
        radial-gradient(1px 1px at 130px 150px, rgba(255,255,255,.5) 50%, transparent 52%);
      background-size: 220px 220px, 300px 300px, 360px 360px, 280px 280px, 400px 400px;
      animation: driftB 200s linear infinite;
      opacity: .35;
    }
    @keyframes driftA {
      from { background-position: 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; }
      to   { background-position: -900px 500px, 650px -700px, -950px -350px, 550px 800px, -700px 600px, 400px -900px, -500px 1000px; }
    }
    @keyframes driftB {
      from { background-position: 0 0, 0 0, 0 0, 0 0, 0 0; }
      to   { background-position: 1100px -600px, -800px 950px, 700px -1200px, -900px 650px, 600px -800px; }
    }
    </style>
    <div id="starfield"></div><div id="starfield2"></div>
    """, unsafe_allow_html=True)
