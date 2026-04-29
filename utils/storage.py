from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import pandas as pd
import streamlit as st

HISTORY_KEY = "prediction_history"


def init_history() -> None:
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []


def add_history(record: Dict[str, Any]) -> None:
    init_history()
    payload = {"timestamp": datetime.now().isoformat(timespec="seconds"), **record}
    st.session_state[HISTORY_KEY].append(payload)


def history_df() -> pd.DataFrame:
    init_history()
    rows = st.session_state[HISTORY_KEY]
    if not rows:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "crop",
                "quality_score",
                "estimated_yield_t_ha",
                "net_profit",
                "region",
            ]
        )
    return pd.DataFrame(rows)
