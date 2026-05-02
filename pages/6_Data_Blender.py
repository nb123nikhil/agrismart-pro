from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.agri_engine import blend_datasets

st.set_page_config(page_title="Data Blender", layout="wide")
st.title("Data Blender")
st.caption("Figure 4.4 - Blend two related datasets into a single analysis-ready table.")

left_file = st.file_uploader("Upload first CSV", type=["csv"], key="left_csv")
right_file = st.file_uploader("Upload second CSV", type=["csv"], key="right_csv")
left_weight = st.slider("First dataset weight", 0.0, 1.0, 0.5, 0.05)
right_weight = 1.0 - left_weight
st.write(f"Second dataset weight: {right_weight:.2f}")

sample_left = pd.DataFrame(
    {
        "plot_id": [1, 2, 3, 4],
        "soil_moisture": [42, 48, 39, 51],
        "yield_index": [61, 67, 59, 72],
    }
)
sample_right = pd.DataFrame(
    {
        "plot_id": [1, 2, 3, 4],
        "soil_moisture": [46, 44, 41, 55],
        "yield_index": [63, 70, 60, 74],
    }
)

left_df = pd.read_csv(left_file) if left_file is not None else sample_left
right_df = pd.read_csv(right_file) if right_file is not None else sample_right

st.subheader("Input Datasets")
col1, col2 = st.columns(2)
col1.dataframe(left_df, use_container_width=True)
col2.dataframe(right_df, use_container_width=True)

blended_df, summary = blend_datasets(left_df, right_df, left_weight=left_weight, right_weight=right_weight)

st.subheader("Blended Output")
st.dataframe(blended_df, use_container_width=True)

metric_cols = st.columns(3)
metric_cols[0].metric("Common numeric columns", len(summary["columns"]))
metric_cols[1].metric("Rows blended", summary["rows"])
metric_cols[2].metric("Weights", f"{left_weight:.2f} / {right_weight:.2f}")

if summary["columns"]:
    chart_df = pd.DataFrame(
        {
            "column": list(summary["blended_means"].keys()),
            "mean": list(summary["blended_means"].values()),
        }
    )
    fig = px.bar(chart_df, x="column", y="mean", title="Average of blended numeric columns", color="mean")
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No shared numeric columns were found. Use CSV files with overlapping numeric fields for blending.")

st.download_button(
    "Download blended CSV",
    data=blended_df.to_csv(index=False).encode("utf-8"),
    file_name="blended_dataset.csv",
    mime="text/csv",
)
