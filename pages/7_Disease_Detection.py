from __future__ import annotations

import streamlit as st
import plotly.express as px

from utils.agri_engine import disease_assessment

st.set_page_config(page_title="Disease Detection", layout="wide")
st.title("Disease Detection")
st.caption("Figure 4.6 - Demo diagnosis based on crop symptoms and uploaded leaf images.")
st.info("This module is a rule-based demo. For production use, connect a trained image-classification model.")

crop = st.selectbox("Crop", ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Soybean"])
leaf_image = st.file_uploader("Upload leaf image", type=["png", "jpg", "jpeg"], key="leaf_image")
if leaf_image is not None:
    st.image(leaf_image, caption="Uploaded leaf image", use_container_width=True)

st.subheader("Visible Symptoms")
col1, col2 = st.columns(2)
with col1:
    yellowing = st.slider("Yellowing severity", 0, 10, 3)
    spots = st.slider("Leaf spots severity", 0, 10, 4)
    wilting = st.slider("Wilting severity", 0, 10, 2)
with col2:
    holes = st.slider("Leaf holes / chewing damage", 0, 10, 2)
    mold = st.slider("Mold / fungus severity", 0, 10, 3)
    recent_rain = st.slider("Recent wet weather pressure", 0, 10, 5)

assessment = disease_assessment(
    {
        "crop": crop,
        "yellowing": yellowing,
        "spots": spots,
        "wilting": wilting,
        "holes": holes,
        "mold": mold,
        "recent_rain": recent_rain,
    }
)

m1, m2, m3 = st.columns(3)
m1.metric("Likely diagnosis", assessment["diagnosis"])
m2.metric("Confidence", f"{assessment['confidence']}%")
m3.metric("Severity", f"{assessment['severity']} / 10")

st.subheader("Risk Breakdown")
chart_df = {
    "diagnosis": list(assessment["scores"].keys()),
    "score": list(assessment["scores"].values()),
}
fig = px.bar(chart_df, x="diagnosis", y="score", color="score", title="Symptom-based disease likelihood")
fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Recommendations")
for item in assessment["recommendations"]:
    st.write(f"- {item}")

st.caption("Figure 4.6 supports a demonstration workflow. Replace it with a trained vision model for real disease classification.")
