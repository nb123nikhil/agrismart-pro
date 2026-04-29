from __future__ import annotations

import streamlit as st
import plotly.express as px
import pandas as pd

from utils.agri_engine import estimate_yield, profit_estimate

st.set_page_config(page_title="Profit Analyzer", layout="wide")
st.title("Profit Analyzer")

crop = st.selectbox("Crop", ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Soybean"])
area = st.number_input("Area (hectare)", min_value=0.1, value=2.0, step=0.1)
quality = st.slider("Expected quality score (%)", 35.0, 100.0, 74.0)
extra_cost = st.number_input("Additional costs (INR)", min_value=0.0, value=10000.0)

yield_t = estimate_yield(crop, quality, area)
report = profit_estimate(crop, yield_t, area, extra_cost)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Estimated yield", f"{yield_t} t")
c2.metric("Revenue", f"INR {report['revenue']}")
c3.metric("Total cost", f"INR {report['total_cost']}")
c4.metric("Net profit", f"INR {report['net_profit']}")

c5, c6 = st.columns(2)
c5.metric("ROI", f"{report['roi_percent']}%")
c6.metric("Break-even yield", f"{report['breakeven_tons']} t")

waterfall_df = pd.DataFrame(
    {
        "stage": ["Revenue", "Costs", "Net"],
        "amount": [report["revenue"], -report["total_cost"], report["net_profit"]],
    }
)
fig = px.bar(waterfall_df, x="stage", y="amount", color="stage", color_discrete_map={"Revenue": "#2A9D8F", "Costs": "#E76F51", "Net": "#264653"})
fig.update_layout(height=380, margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
st.plotly_chart(fig, use_container_width=True)
