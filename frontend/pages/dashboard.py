import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Petrolytics Dashboard",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto",
)

hide_buttons_css = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap');

button[data-testid="stDeployButton"],
button[data-testid="stSettingsButton"],
button[data-testid="stOptionButton"],
button[data-testid="stBaseButton-header"] { display: none; }

.stTitle { font-size: 4rem; font-weight: 700; font-family: 'Roboto Slab', serif; margin: 0; }
.summary { font-size: 1.5rem; font-family: 'Roboto Slab', serif; line-height:1.4; }
</style>
'''
st.markdown(hide_buttons_css, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<h1 class='stTitle'>Petrolytics Analytical Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='summary'><br/>"
        "Unlock deep insights into global oil production, reserves, and trade flows.<br/>"
        "Explore interactive visualizations, real-time maps, and comprehensive datasets "
        "tailored for petroleum industry decision-makers."
        "</div>", unsafe_allow_html=True
    )
with col2:
    components.html(
        """
        <div style='position: relative; top: -65px; left: 240px;'>
           <script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>

            <dotlottie-player
                src="https://lottie.host/03d864c6-a4c1-4bce-9a8f-01214b46259e/ckbRaCf3KR.lottie"
                background="transparent"
                speed="1"
                style="width: 350px; height: 350px"
                loop
                autoplay
            ></dotlottie-player>
        </div>
        """,
        height=350
    )

st.markdown("---")
REAL_FIELDS = [
    "Ghawar", "Burgan", "Safaniya", "Rumaila", "Zakum", "West Qurna", "Kashagan", "Tengiz",
    "Cantarell", "Prudhoe Bay", "North Field", "Hassi Messaoud", "Hassi R'Mel", "Samotlor",
    "Daqing", "Bolivar Coastal", "Marcellus Shale", "Permian Basin", "Eagle Ford", "Bakken",
    "Orinoco Belt", "South Pars", "Al-Shaheen", "Kirkuk", "Matti", "Karachaganak",
    "Sergipe-Alagoas", "Kovykta", "Zaafarana", "Zagros", "Kirkuk", "Troll",
    "Campos Basin", "Bouri", "Es Sider", "Sepandan", "Jebel Dogr", "Mahakam",
    "Bayhan-Umm", "Chicontepec", "Rumaila", "Alberta Oil Sands", "Urals",
    "Bowen", "Ivishak", "Gum Deniz", "Foinaven", "Liza", "Buckskin", "Zhigansk"
]

def generate_oil_data(fields_list):
    np.random.seed(42)
    num_points = len(fields_list)
    latitudes  = np.random.uniform(-25, 60, size=num_points)
    longitudes = np.random.uniform(-100, 80, size=num_points)
    production = np.random.uniform(1e5, 5e7, size=num_points)
    reserves    = np.random.uniform(1e6, 1e9, size=num_points)
    df = pd.DataFrame({
        "Field": fields_list,
        "latitude": latitudes,
        "longitude": longitudes,
        "production_bbl": production.astype(int),
        "reserves_bbl": reserves.astype(int)
    })
    return df

oil_df = generate_oil_data(REAL_FIELDS)

st.subheader("Oil Feature Data")
st.dataframe(oil_df, use_container_width=True)

st.subheader("Global Production & Reserves 3D Map")
mid = [oil_df.latitude.mean(), oil_df.longitude.mean()]
prod_layer = pdk.Layer(
    "ColumnLayer", data=oil_df,
    get_position=["longitude", "latitude"],
    get_elevation="production_bbl / 1000", elevation_scale=0.05,
    radius=150000, pickable=True, auto_highlight=True,
    get_fill_color="[0, 128, 255, 200]"
)
res_layer = pdk.Layer(
    "ColumnLayer", data=oil_df,
    get_position=["longitude", "latitude"],
    get_elevation="reserves_bbl / 1e6", elevation_scale=0.5,
    radius=75000, pickable=True, auto_highlight=True,
    get_fill_color="[255, 165, 0, 200]"
)
view = pdk.ViewState(latitude=mid[0], longitude=mid[1], zoom=1, pitch=45)
deck = pdk.Deck(
    layers=[prod_layer, res_layer],
    initial_view_state=view,
    tooltip={
        "html": "<b>Field:</b> {Field}<br/><b>Prod:</b> {production_bbl} bbl<br/><b>Res:</b> {reserves_bbl} bbl",
        "style": {"color": "white"}
    }
)
st.pydeck_chart(deck)

top5 = oil_df.nlargest(5, "production_bbl").copy()
top5["production_m"] = (top5["production_bbl"] / 1e6).round(2)
chart = alt.Chart(top5).mark_bar().encode(
    x=alt.X("production_m:Q", title="Production (M bbl)"),
    y=alt.Y("Field:N", sort="-x", title="Field"),
    color=alt.Color("production_m:Q", scale=alt.Scale(scheme="tealblues"), legend=None),
    tooltip=[alt.Tooltip("Field:N"), alt.Tooltip("production_m:Q", title="Production (M bbl)")]
).properties(height=300)
st.subheader("Top 5 Production Fields")
st.altair_chart(chart, use_container_width=True)

with st.expander("OPEC & Corporate Production Details"):
    st.markdown(
        "- Official OPEC Site: [opec.org](https://www.opec.org)  \n- ASB Reports: [report](https://asb.opec.org)"
    )
    opec_members = ["Algeria","Angola","Congo","Eq. Guinea","Gabon","Iran","Iraq",
                    "Kuwait","Libya","Nigeria","Saudi Arabia","UAE","Venezuela"]
    np.random.seed(123)
    prod = np.random.uniform(1e6,12e6,len(opec_members)).astype(int)
    exp = (prod * np.random.uniform(0.5,0.9,len(opec_members))).astype(int)
    opec_df = pd.DataFrame({"Country": opec_members,
                             "Production (M bbl)": (prod/1e6).round(2),
                             "Exports (M bbl)": (exp/1e6).round(2)})
    st.subheader("OPEC Production Data")
    st.dataframe(opec_df, use_container_width=True)

    companies = ["Saudi Aramco","ExxonMobil","Shell","BP","Chevron","TotalEnergies",
                  "CNPC","Gazprom","PetroChina","Lukoil","Rosneft","ENI","ConocoPhillips",
                  "Equinor","Phillips 66"]
    np.random.seed(321)
    annual = np.random.uniform(0.5e9,3e9,len(companies)).astype(int)
    corp_df = pd.DataFrame({"Corporation": companies,
                             "Annual Prod (M bbl)": (annual/1e6).round(2)})
    st.subheader("Major Corporate Production")
    st.dataframe(corp_df, use_container_width=True)
