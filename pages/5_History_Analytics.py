from __future__ import annotations

import streamlit as st
import plotly.express as px

from utils.storage import history_df

st.set_page_config(page_title="History & Analytics", layout="wide")
st.title("History & Analytics")

df = history_df()
if df.empty:
    st.warning("No records yet. Save predictions from Crop Advisor to populate analytics.")
    st.stop()

df["timestamp"] = df["timestamp"].astype("datetime64[ns]")

c1, c2, c3 = st.columns(3)
c1.metric("Records", int(df.shape[0]))
c2.metric("Avg quality", round(df["quality_score"].mean(), 1))
c3.metric("Avg net profit", f"INR {round(df['net_profit'].mean(), 2)}")

line = px.line(df.sort_values("timestamp"), x="timestamp", y="quality_score", title="Quality Trend")
line.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(line, use_container_width=True)

bars = px.bar(df.groupby("crop", as_index=False)["net_profit"].mean(), x="crop", y="net_profit", title="Average Net Profit by Crop")
bars.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(bars, use_container_width=True)

st.subheader("Saved Records")
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button("Download history as CSV", data=csv_bytes, file_name="agrivista_history.csv", mime="text/csv")
