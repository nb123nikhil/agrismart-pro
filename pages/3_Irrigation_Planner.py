from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

from utils.agri_engine import irrigation_plan

st.set_page_config(page_title="Irrigation Planner", layout="wide")
st.title("Irrigation Planner")

crop = st.selectbox("Crop", ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Soybean"])
area = st.number_input("Area (hectare)", min_value=0.1, value=2.0, step=0.1)

c1, c2, c3 = st.columns(3)
temp = c1.slider("Avg weekly temperature (C)", 5.0, 45.0, 28.0)
humidity = c2.slider("Avg humidity (%)", 15.0, 100.0, 65.0)
rainfall = c3.slider("Weekly rainfall (mm)", 0.0, 180.0, 18.0)

result = irrigation_plan(crop, temp, humidity, rainfall, area)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total demand", f"{result['weekly_demand_mm']} mm/week")
m2.metric("Rainfall credit", f"{result['rainfall_credit_mm']} mm")
m3.metric("Irrigation need", f"{result['required_irrigation_mm']} mm")
m4.metric("Water volume", f"{result['required_irrigation_m3']} m3")

fig = go.Figure(
    data=[
        go.Bar(name="Demand", x=["Weekly water (mm)"], y=[result["weekly_demand_mm"]], marker_color="#2A9D8F"),
        go.Bar(name="Rainfall", x=["Weekly water (mm)"], y=[result["rainfall_credit_mm"]], marker_color="#E9C46A"),
        go.Bar(name="Irrigation", x=["Weekly water (mm)"], y=[result["required_irrigation_mm"]], marker_color="#E76F51"),
    ]
)
fig.update_layout(barmode="group", height=380, margin=dict(l=10, r=10, t=20, b=10))
st.plotly_chart(fig, use_container_width=True)
