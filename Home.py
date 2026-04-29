from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="AgriVista Lab", layout="wide", page_icon=":seedling:")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }
    .hero {
        background: linear-gradient(120deg, #1f4037 0%, #99f2c8 100%);
        padding: 2.2rem;
        border-radius: 22px;
        color: #0f1a16;
        margin-bottom: 1rem;
    }
    .hero h1,
    .hero p {
        color: #0f1a16;
    }
    .card {
        background: #f8f5ed;
        border: 1px solid #d8ceb8;
        border-radius: 18px;
        padding: 1rem;
        min-height: 170px;
        color: #1b1a17;
    }
    .card h3,
    .card p {
        color: #1b1a17;
    }
    @media (prefers-color-scheme: dark) {
        .card {
            background: #f1ebdc;
            border-color: #cbbd9c;
            color: #171612;
        }
        .card h3,
        .card p {
            color: #171612;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin:0; font-size:3rem;">AgriVista Lab</h1>
        <p style="margin: 0.4rem 0 0 0; font-size:1.1rem; max-width: 850px;">
            A practical farm analytics workspace inspired by AgriSmart-style workflows.
            Predict crop suitability, estimate quality and yield, calculate fertilizer and irrigation plans,
            and track profit and historical trends.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="card">
            <h3>Crop Advisor</h3>
            <p>Input soil and climate values to get recommended crops, quality score, and expected yield.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="card">
            <h3>Fertilizer + Irrigation</h3>
            <p>Compute nutrient deficits and weekly water demand with rainfall adjustments.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="card">
            <h3>Profit + History</h3>
            <p>Estimate ROI, break-even yield, and review downloadable analytics history.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.info("Use the left sidebar to open each module page.")
