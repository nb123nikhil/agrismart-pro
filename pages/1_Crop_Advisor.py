from __future__ import annotations

import streamlit as st
import plotly.express as px
import pandas as pd

from utils.agri_engine import (
    recommend_crop,
    estimate_yield,
    profit_estimate,
    fertilizer_plan,
    irrigation_plan,
)
from utils.storage import add_history


def inr(amount: float) -> str:
    return f"INR {amount:,.2f}"

st.set_page_config(page_title="Crop Advisor", layout="wide")
st.title("Crop Advisor")
st.caption("End-to-end crop decision support: suitability, yield, fertilizer, irrigation, and profitability.")

presets = {
    "Custom": None,
    "Monsoon Paddy Zone": {"N": 95, "P": 45, "K": 40, "temperature": 28.0, "humidity": 82.0, "ph": 6.3, "rainfall": 220.0},
    "Dryland Cereal Zone": {"N": 70, "P": 32, "K": 25, "temperature": 30.0, "humidity": 48.0, "ph": 7.1, "rainfall": 65.0},
    "Balanced Field": {"N": 80, "P": 40, "K": 35, "temperature": 27.0, "humidity": 68.0, "ph": 6.4, "rainfall": 120.0},
}

left, right = st.columns([1.1, 1])

with left:
    st.subheader("Field Inputs")
    preset = st.selectbox("Quick profile", list(presets.keys()), index=2)
    values = presets[preset] or presets["Balanced Field"]

    region = st.text_input("Region", value="Demo Farm Zone")
    area = st.number_input("Field area (hectare)", min_value=0.1, max_value=500.0, value=2.0, step=0.1)

    n = st.slider("Nitrogen (N)", 0, 200, int(values["N"]))
    p = st.slider("Phosphorus (P)", 0, 120, int(values["P"]))
    k = st.slider("Potassium (K)", 0, 120, int(values["K"]))
    temperature = st.slider("Temperature (C)", 5.0, 45.0, float(values["temperature"]))
    humidity = st.slider("Humidity (%)", 15.0, 100.0, float(values["humidity"]))
    ph = st.slider("Soil pH", 3.5, 9.5, float(values["ph"]))
    rainfall = st.slider("Rainfall (mm)", 0.0, 400.0, float(values["rainfall"]))

inputs = {
    "N": float(n),
    "P": float(p),
    "K": float(k),
    "temperature": float(temperature),
    "humidity": float(humidity),
    "ph": float(ph),
    "rainfall": float(rainfall),
}

best_crop, scores = recommend_crop(inputs)
quality = scores[best_crop]
yield_t = estimate_yield(best_crop, quality, area)
fert = fertilizer_plan(best_crop, area, inputs["N"], inputs["P"], inputs["K"])
irrigation = irrigation_plan(best_crop, temperature, humidity, rainfall / 4.0, area)
finance = profit_estimate(best_crop, yield_t, area, extra_cost=fert["estimated_cost"])

comparison_rows = []
for crop, score in list(scores.items())[:3]:
    crop_yield = estimate_yield(crop, score, area)
    crop_fert = fertilizer_plan(crop, area, inputs["N"], inputs["P"], inputs["K"])
    crop_irr = irrigation_plan(crop, temperature, humidity, rainfall / 4.0, area)
    crop_fin = profit_estimate(crop, crop_yield, area, extra_cost=crop_fert["estimated_cost"])
    comparison_rows.append(
        {
            "Crop": crop,
            "Score (%)": score,
            "Yield (t)": crop_yield,
            "Fertilizer Cost (INR)": crop_fert["estimated_cost"],
            "Irrigation Need (mm/week)": crop_irr["required_irrigation_mm"],
            "Revenue (INR)": crop_fin["revenue"],
            "Total Cost (INR)": crop_fin["total_cost"],
            "Net Profit (INR)": crop_fin["net_profit"],
            "ROI (%)": crop_fin["roi_percent"],
        }
    )

compare_df = pd.DataFrame(comparison_rows)

with right:
    st.subheader("Recommendation")
    st.metric("Best crop", best_crop)
    st.metric("Quality score", f"{quality}%")
    st.metric("Estimated yield", f"{yield_t} t")

    st.subheader("Profit Snapshot")
    c1, c2 = st.columns(2)
    c1.metric("Revenue", inr(finance["revenue"]))
    c1.metric("ROI", f"{finance['roi_percent']}%")
    c2.metric("Cost", inr(finance["total_cost"]))
    c2.metric("Net", inr(finance["net_profit"]))

    st.subheader("Resource Planning")
    p1, p2 = st.columns(2)
    p1.metric("Fertilizer budget", inr(fert["estimated_cost"]))
    p1.metric("Urea", f"{fert['urea_kg']} kg")
    p2.metric("Irrigation need", f"{irrigation['required_irrigation_mm']} mm/week")
    p2.metric("Water volume", f"{irrigation['required_irrigation_m3']} m3/week")

rank_df = pd.DataFrame({"crop": list(scores.keys()), "score": list(scores.values())})
fig = px.bar(rank_df, x="crop", y="score", color="score", color_continuous_scale="YlGn")
fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Crop Comparison")
st.dataframe(compare_df, use_container_width=True, hide_index=True)

advice = []
if ph < 5.8:
    advice.append("Soil is acidic. Consider liming and split nutrient doses.")
elif ph > 7.8:
    advice.append("Soil is alkaline. Use sulfur-based amendments and organic matter.")

if rainfall < 80:
    advice.append("Low rainfall scenario. Prioritize moisture conservation and timely irrigation.")
if humidity > 82:
    advice.append("High humidity may increase disease pressure. Plan preventive crop protection.")
if n < 50 or p < 25 or k < 20:
    advice.append("NPK appears low. Review fertilizer calculator recommendations before sowing.")

st.subheader("Advisor Notes")
if advice:
    for line in advice:
        st.write(f"- {line}")
else:
    st.write("- Soil and climate profile looks balanced for standard management practices.")

report_df = compare_df.copy()
report_df.insert(0, "Region", region)
report_df.insert(1, "Area (ha)", area)
report_bytes = report_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download crop advisory report (CSV)",
    data=report_bytes,
    file_name="crop_advisory_report.csv",
    mime="text/csv",
)

if st.button("Save to history", type="primary"):
    add_history(
        {
            "crop": best_crop,
            "quality_score": quality,
            "estimated_yield_t_ha": round(yield_t / area, 2),
            "net_profit": finance["net_profit"],
            "region": region,
            "fertilizer_cost": fert["estimated_cost"],
            "irrigation_mm_week": irrigation["required_irrigation_mm"],
        }
    )
    st.success("Saved.")
