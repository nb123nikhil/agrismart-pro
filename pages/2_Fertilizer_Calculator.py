from __future__ import annotations

import streamlit as st
import pandas as pd

from utils.agri_engine import fertilizer_plan

st.set_page_config(page_title="Fertilizer Calculator", layout="wide")
st.title("Fertilizer Calculator")

c1, c2 = st.columns(2)

with c1:
    crop = st.selectbox("Crop", ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Soybean"])
    area = st.number_input("Area (hectare)", min_value=0.1, value=2.0, step=0.1)

with c2:
    n = st.number_input("Current N (kg/ha)", min_value=0.0, value=45.0)
    p = st.number_input("Current P (kg/ha)", min_value=0.0, value=20.0)
    k = st.number_input("Current K (kg/ha)", min_value=0.0, value=15.0)

result = fertilizer_plan(crop, area, n, p, k)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Required N", f"{result['required_n_kg']} kg")
m2.metric("Required P", f"{result['required_p_kg']} kg")
m3.metric("Required K", f"{result['required_k_kg']} kg")
m4.metric("Estimated cost", f"INR {result['estimated_cost']}")

st.subheader("Suggested materials")
mat = pd.DataFrame(
    {
        "Material": ["Urea", "DAP", "MOP"],
        "Quantity (kg)": [result["urea_kg"], result["dap_kg"], result["mop_kg"]],
    }
)
st.dataframe(mat, use_container_width=True)

st.caption("Cost model is a demo estimate. Replace with your local pricing data for production use.")
