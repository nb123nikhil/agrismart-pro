# A REPORT OF PROJECT-I ON AGRISMART PRO
**On Project Title:** AgriSmart Pro - A Streamlit-Based Agricultural Decision Support System
I, **[Your Name]**, hereby declare that I have undertaken this software project on **AgriSmart Pro** during the period **[start date] to [end date]** in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering.
... this project presents **AgriSmart Pro**, a Streamlit-based agricultural analytics application that provides practical decision support using rule-based computation.
### Figure 1.1: Architecture of AgriSmart Pro
AgriSmart Pro is a web-based agricultural decision support system developed using Streamlit. The main purpose of the project is to assist users in making better crop-related decisions by converting field inputs into practical recommendations. It brings together crop selection, fertilizer planning, irrigation estimation, and profitability analysis in one interactive dashboard.
AgriSmart Pro focuses on a lightweight, understandable approach. Instead of training a model, it uses crop profiles and mathematical scoring rules. This makes the project easier to maintain, debug, and demonstrate in class.
AgriSmart Pro successfully demonstrates how a small web-based decision support system can assist with agricultural planning. The project integrates crop recommendation, fertilizer planning, irrigation estimation, profit analysis, and historical tracking into a single user-friendly interface. It meets the primary objective of providing a working, transparent, and interactive agriculture analytics application.
Figure 1.1 Architecture of AgriSmart Pro  
- `Home.py` for the landing page
# A REPORT OF PROJECT-I ON AGRIVISTA LAB

## Title Page / Front Page

**A REPORT OF PROJECT-I**

**On Project Title:** AgriVista Lab - A Streamlit-Based Agricultural Decision Support System

Submitted in partial fulfillment of the requirement for the award of the degree of

**Bachelor of Technology**

(Computer Science and Engineering)

Submitted by: **[Your Name]**  
College / Roll No.: **[Your Roll No.]**  
Submitted to: **Dr. Ashima Mehta**  
Department of Computer Science and Engineering  
Dronacharya College of Engineering, Gurugram, Haryana

Session: **2025-26**

---

## Candidate's Declaration

I, **[Your Name]**, hereby declare that I have undertaken this software project on **AgriVista Lab** during the period **[start date] to [end date]** in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering.

The work presented in this project report is an authentic record of my own project work carried out under academic guidance. I have not copied the work from any unauthorized source, and all references used in the preparation of this report have been properly acknowledged.

Signature of the Student: ____________________

The project viva-voce examination of **[date]** has been held and accepted.

Signature of HOD: ____________________

---

## Abstract

Agriculture is highly dependent on climate, soil fertility, irrigation availability, and economic planning. Small and medium-scale farmers often make decisions using experience alone, which can lead to low yield, inefficient fertilizer use, poor irrigation scheduling, and uncertain profitability. To address these challenges, this project presents **AgriVista Lab**, a Streamlit-based agricultural analytics application that provides practical decision support using rule-based computation.

The system contains five major modules: Crop Advisor, Fertilizer Calculator, Irrigation Planner, Profit Analyzer, and History & Analytics. The Crop Advisor evaluates soil and climate inputs such as nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall to recommend the most suitable crop. The Fertilizer Calculator estimates nutrient requirements and input material quantities. The Irrigation Planner computes weekly water demand after accounting for rainfall credit. The Profit Analyzer estimates revenue, total cost, net profit, ROI, and break-even yield. The History module stores user predictions in session memory and provides analytics with CSV export.

The project is built using Python, Streamlit, Pandas, NumPy, and Plotly. It does not require any external dataset or machine learning model. Instead, it uses transparent agronomic scoring and financial formulas so that results are easy to understand and modify. The application is designed as a compact, interactive, and user-friendly decision support tool for agricultural planning.

---

## Acknowledgement

I express my sincere gratitude to **Dr. Ashima Mehta** for guidance and support throughout this project. I also thank the faculty members of the Department of Computer Science and Engineering for their valuable suggestions and encouragement.

I am also thankful to my family and friends for their support during the completion of this work. Finally, I acknowledge the open-source Python ecosystem, especially Streamlit, Pandas, NumPy, and Plotly, which made this project practical and efficient to implement.

---

## List of Figures

Figure 1.1 Architecture of AgriVista Lab  
Figure 2.1 Crop scoring and recommendation flow  
Figure 3.1 Fertilizer planning workflow  
Figure 4.1 Irrigation planning workflow  
Figure 5.1 Profit analysis workflow  
Figure 6.1 History and analytics workflow

---

## List of Tables

Table 1.1 Software tools used in the project  
Table 2.1 Crop profile parameters stored in the engine  
Table 3.1 Fertilizer output summary  
Table 4.1 Irrigation output summary  
Table 5.1 Profit analysis summary  
Table 6.1 Saved history fields

---

## Definitions, Acronyms and Abbreviations

- **N**: Nitrogen
- **P**: Phosphorus
- **K**: Potassium
- **pH**: Measure of soil acidity or alkalinity
- **ROI**: Return on Investment
- **ET0**: Reference evapotranspiration
- **Kc**: Crop coefficient
- **CSV**: Comma-Separated Values
- **UI**: User Interface
- **INR**: Indian Rupee

---

## Table of Contents

1. Introduction to Project  
2. Background and Motivation  
3. Literature Survey  
4. Project Work  
5. Results and Discussion  
6. Conclusion and Future Scope  
References  
Appendix

---

# Chapter 1: Introduction to Project

## 1.1 Overview

AgriVista Lab is a web-based agricultural decision support system developed using Streamlit. The main purpose of the project is to assist users in making better crop-related decisions by converting field inputs into practical recommendations. It brings together crop selection, fertilizer planning, irrigation estimation, and profitability analysis in one interactive dashboard.

## 1.2 Problem Statement

Farmers often face difficulty in selecting the right crop and planning resource usage because field conditions change with soil quality, climate, and rainfall. Manual decision making can lead to overuse or underuse of fertilizer, improper irrigation scheduling, and uncertain profit. A simple, transparent, and easy-to-use digital tool can help reduce these problems.

## 1.3 Objectives

- Recommend suitable crops based on soil and climate conditions.
- Estimate yield using crop quality score and land area.
- Calculate fertilizer requirements from current soil nutrient levels.
- Estimate weekly irrigation demand after rainfall adjustment.
- Compute revenue, total cost, net profit, ROI, and break-even yield.
- Store previous results and show analytics for comparison.

## 1.4 Scope of the Project

The project is designed as a working prototype for agricultural planning. It can be used for educational demonstrations, basic farm advisory, and proof-of-concept analytics. It is not a replacement for field surveys or expert agronomist judgment, but it provides a structured starting point for decision making.

## 1.5 Architecture

The application follows a simple layered structure:

1. User interface layer built with Streamlit.
2. Computation layer in `utils/agri_engine.py`.
3. Session history layer in `utils/storage.py`.
4. Visualization layer using Plotly and Pandas.

### Figure 1.1: Architecture of AgriVista Lab

User Inputs -> Streamlit Pages -> Agri Engine Calculations -> Results, Charts, and History Storage

---

# Chapter 2: Background and Motivation

## 2.1 Agricultural Decision Support

Agriculture is influenced by many variables such as soil nutrients, temperature, humidity, rainfall, and crop economics. Decisions based only on intuition can be inaccurate when environmental conditions vary. Decision support tools help translate field data into actionable recommendations.

## 2.2 Why a Rule-Based System Was Chosen

This project uses a formula-based approach instead of machine learning because it is:

- Easier to understand and explain.
- Faster to run in a small Streamlit application.
- Suitable when no large labeled dataset is available.
- Transparent, so users can see how recommendations are formed.

## 2.3 Software Tools Used

Table 2.1 summarizes the main tools used in the project.

| Tool | Purpose |
| --- | --- |
| Python | Core programming language |
| Streamlit | Web app and dashboard interface |
| Pandas | Tabular data handling and CSV export |
| NumPy | Numerical scoring functions |
| Plotly | Interactive charts |

## 2.4 Currency and Localization

All cost-related outputs are shown in **INR (Indian Rupee)**. This makes the output relevant for Indian agricultural use cases and easier to interpret for local users.

## 2.5 Motivation

The motivation behind this project is to create a compact farm analytics tool that is simple enough for demonstration yet meaningful enough to show how software can support agricultural planning.

---

# Chapter 3: Literature Survey

## 3.1 Traditional Farming Decisions

Earlier farming decisions were mostly based on personal experience, local knowledge, and weather observation. While valuable, these methods are not always precise or scalable for modern farming needs.

## 3.2 Digital Advisory Systems

Various digital farming tools provide crop recommendations, fertilizer suggestions, and irrigation guidance. Many systems depend on mobile apps, cloud APIs, or data-heavy machine learning models.

## 3.3 Advantages of Existing Approaches

- Faster access to decision support.
- Better data organization.
- Reusable calculations and reports.

## 3.4 Limitations of Existing Approaches

- Some tools need internet connectivity.
- Many are too complex for simple academic implementation.
- Machine learning systems often require datasets and training time.

## 3.5 How This Project Differs

AgriVista Lab focuses on a lightweight, understandable approach. Instead of training a model, it uses crop profiles and mathematical scoring rules. This makes the project easier to maintain, debug, and demonstrate in class.

---

# Chapter 4: Project Work

## 4.1 Major Problem Addressed

The major problem addressed is helping users evaluate crop suitability and farm planning decisions using a single integrated web application.

## 4.2 Methodology

The methodology is based on the following steps:

1. Collect crop and field inputs from the user.
2. Compare the inputs against crop profiles.
3. Compute quality score using similarity-based weighting.
4. Estimate yield, fertilizer requirement, irrigation need, and profit.
5. Display the results using metrics, tables, and charts.
6. Save selected results to session history.

## 4.3 Core Modules

### 4.3.1 Crop Advisor

This module combines crop recommendation, yield estimation, fertilizer planning, irrigation planning, and profit estimation. It is the most complete decision support module in the project.

### 4.3.2 Fertilizer Calculator

This module calculates nutrient deficits and converts them into fertilizer material quantities.

### 4.3.3 Irrigation Planner

This module estimates weekly water demand based on climate and crop type and subtracts rainfall credit.

### 4.3.4 Profit Analyzer

This module estimates farming economics by combining yield and cost calculations.

### 4.3.5 History and Analytics

This module stores previous predictions and displays their trends.

## 4.4 Implementation Details

The main logic is implemented in `utils/agri_engine.py` through these functions:

- `quality_score()` for crop suitability scoring
- `recommend_crop()` for best crop selection
- `estimate_yield()` for production estimation
- `fertilizer_plan()` for nutrient and cost planning
- `irrigation_plan()` for water requirement estimation
- `profit_estimate()` for financial analysis

Session data is managed by `utils/storage.py` using Streamlit session state.

## 4.5 Workflow Diagram

### Figure 4.1: Project Workflow

Input -> Crop Profiles -> Calculations -> Metrics/Charts -> Save to History -> CSV Export

---

# Chapter 5: Results and Discussion

## 5.1 Crop Advisor Results

The Crop Advisor displays the best crop according to the entered field profile, quality score, estimated yield, fertilizer budget, and irrigation need. It also shows a comparison table for the top crops so the user can compare options.

## 5.2 Fertilizer and Irrigation Results

The fertilizer module outputs required N, P, K along with material quantities such as urea, DAP, and MOP. The irrigation module displays weekly demand, rainfall credit, irrigation need, and water volume in cubic meters.

## 5.3 Profit Analysis Results

The profit analyzer computes revenue, total cost, net profit, ROI, and break-even yield. These outputs help the user understand whether a crop choice is economically viable.

## 5.4 History and Visualization

The history page stores saved recommendations in session memory and shows analytics such as average quality score, average profit, quality trend, and crop-wise profit comparison.

## 5.5 Discussion

The results are easy to interpret because they are displayed using metrics, tables, and charts. Since the system is deterministic, two users with the same inputs will get the same outputs, which improves explainability. However, the current formulas are still demo-level approximations and should be replaced with real local agronomy data for production use.

### Figure 5.1: Profit Analysis Workflow

Yield and price -> Revenue -> Cost -> Net Profit -> ROI

---

# Chapter 6: Conclusion and Future Scope

## 6.1 Conclusion

AgriVista Lab successfully demonstrates how a small web-based decision support system can assist with agricultural planning. The project integrates crop recommendation, fertilizer planning, irrigation estimation, profit analysis, and historical tracking into a single user-friendly interface. It meets the primary objective of providing a working, transparent, and interactive agriculture analytics application.

## 6.2 Future Scope

Future enhancements may include:

- Real weather API integration.
- Local soil and market database support.
- Persistent storage using SQLite or PostgreSQL.
- Machine learning-based recommendation models.
- User login and multi-farmer profiles.
- Mobile-friendly deployment.

---

# References

[1] Streamlit Documentation, https://docs.streamlit.io/  
[2] Pandas Documentation, https://pandas.pydata.org/docs/  
[3] NumPy Documentation, https://numpy.org/doc/  
[4] Plotly Documentation, https://plotly.com/python/  
[5] Python Documentation, https://docs.python.org/3/

---

# Appendix

## Appendix A: Program Summary

The project is organized into the following files:

- `Home.py` for the landing page
- `pages/1_Crop_Advisor.py` for crop recommendation and full advisory
- `pages/2_Fertilizer_Calculator.py` for fertilizer estimation
- `pages/3_Irrigation_Planner.py` for irrigation planning
- `pages/4_Profit_Analyzer.py` for financial analysis
- `pages/5_History_Analytics.py` for saved record analysis
- `utils/agri_engine.py` for calculation logic
- `utils/storage.py` for session history management

## Appendix B: Notes

- The project is built without an external dataset.
- The system uses formula-based logic for transparency.
- Monetary values are represented in INR.
- The report can be copied into a Word document and formatted according to the college template.
