from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.agri_engine import soil_health_score

st.set_page_config(page_title="Soil Health Analyser", layout="wide")
st.title("Soil Health Analyser")
st.caption("Figure 4.7 - Evaluate core soil indicators and receive management advice.")

c1, c2 = st.columns(2)
with c1:
    ph = st.slider("Soil pH", 3.5, 9.5, 6.8)
    ec = st.slider("Electrical conductivity (dS/m)", 0.0, 3.0, 0.6, 0.1)
    organic_carbon = st.slider("Organic carbon (%)", 0.1, 2.0, 0.7, 0.1)
with c2:
    n = st.slider("Available nitrogen (kg/ha)", 0.0, 200.0, 72.0, 1.0)
    p = st.slider("Available phosphorus (kg/ha)", 0.0, 100.0, 28.0, 1.0)
    k = st.slider("Available potassium (kg/ha)", 0.0, 200.0, 38.0, 1.0)

moisture = st.slider("Soil moisture (%)", 0.0, 100.0, 52.0, 1.0)

report = soil_health_score(
    {
        "ph": ph,
        "ec": ec,
        "organic_carbon": organic_carbon,
        "n": n,
        "p": p,
        "k": k,
        "moisture": moisture,
    }
)

m1, m2, m3 = st.columns(3)
m1.metric("Health status", report["status"])
m2.metric("Overall score", f"{report['overall_score']} / 100")
m3.metric("Soil moisture score", f"{report['moisture_score']} / 100")

st.subheader("Component Scores")
component_df = pd.DataFrame(
    {
        "indicator": ["pH", "EC", "Organic Carbon", "NPK", "Moisture"],
        "score": [report["ph_score"], report["ec_score"], report["organic_carbon_score"], report["npk_score"], report["moisture_score"]],
    }
)
fig = px.bar(component_df, x="indicator", y="score", color="score", title="Soil health components")
fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Advisory Notes")
if report["advice"]:
    for item in report["advice"]:
        st.write(f"- {item}")
else:
    st.success("Soil indicators are balanced. Continue current management practices.")

st.caption("Figure 4.7 is designed for rule-based analysis. A lab-report integration can be added later if needed.")
