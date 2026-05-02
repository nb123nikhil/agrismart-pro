# AgriSmart Pro

AgriSmart Pro is an original, Streamlit-based agricultural analytics project inspired by multi-module farm intelligence apps.

## Features

- Crop advisor with suitability scoring
- Quality score and yield estimation
- Fertilizer requirement calculator
- Irrigation planner with rainfall credit
- Profit and ROI analyzer
- History tracking and CSV export
- Disease Detection module for symptom-based demo diagnosis
- Soil Health Analyser for soil quality scoring

## Tech Stack

- Python 3.10+
- Streamlit
- Pandas
- NumPy
- Plotly

## Run Locally (Windows PowerShell)

```powershell
cd "c:\Users\nikhi\OneDrive\Desktop\MAVEN demo vs\agrismart-pro"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run Home.py
```

## Notes

- This app runs fully with built-in calculation logic; no external dataset is required.
- Currency in all cost/profit modules is set to INR (Indian Rupee).
- For production usage, replace demo formulas with validated agronomy and local market datasets.
