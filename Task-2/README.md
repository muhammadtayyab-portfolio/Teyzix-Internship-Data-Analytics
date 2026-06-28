# Task 2 — Electronics Store Sales & Customer Behavior Analysis

**Teyzix Internship Program (June 2026 Batch)**
**Task ID:** DA-2 | **Domain:** Data Analytics
**Assigned:** 20 June 2026 | **Deadline:** 29 June 2026

## 📌 Project Overview

End-to-end data analytics project simulating a UAE-based electronics retail store. A realistic synthetic dataset (1,200 records) was generated, deliberately injected with real-world data quality issues, cleaned, analyzed, and presented through an interactive dashboard — covering the full Data Analyst workflow from raw data to business recommendations.

## 🎯 Objective

Act as a Data Analyst for an electronics retail company: create the dataset, clean it, perform exploratory analysis, generate business insights, and build an interactive dashboard for decision-making.

## 📂 Repository Structure

```
Task-2/
├── DA_INT_2_Electronics_Sales_Analysis.ipynb   # Full analysis notebook
├── electronics_sales_raw.csv                   # Generated dataset (with injected issues)
├── electronics_sales_clean.csv                 # Cleaned dataset
├── customer_segments.csv                       # RFM segmentation output
├── app.py                                      # Streamlit dashboard
├── requirements.txt                            # Python dependencies
├── report.md                                   # Full analytics report
└── README.md
```

## 🛠️ Tech Stack

- **Python** — Pandas, NumPy
- **Faker** — Synthetic data generation
- **Matplotlib, Seaborn** — Exploratory data analysis
- **Streamlit + Plotly** — Interactive dashboard
- **Google Colab** — Development environment

## 🔍 What Was Done

1. **Dataset Generation** — 1,200+ synthetic transaction records (UAE cities, electronics categories, AED pricing) using Faker + custom business logic
2. **Data Cleaning** — Handled missing values, removed duplicates, standardized inconsistent text formats, fixed invalid entries (full breakdown in `report.md`)
3. **Exploratory Data Analysis** — Monthly trends, top products/categories, revenue by city, payment method distribution, AOV, peak sales periods
4. **Business Insights** — Best/underperforming categories, seasonal trends, customer behavior, actionable recommendations
5. **Bonus: Customer Segmentation** — RFM-based segmentation into High-Value, Loyal/Regular, At-Risk, and Low-Engagement customers
6. **Dashboard** — Interactive Streamlit dashboard with KPIs, filters (city/category/payment/date), and visual breakdowns

## 📊 Key Highlights

- **AED 3,914.99** average order value
- **96%** repeat customer rate
- Peak revenue months: **January, November, December** (DSF / Black Friday / year-end)
- **Laptops** = highest revenue category; **Accessories** = lowest

Full findings and recommendations are documented in [`report.md`](./report.md).

## 🚀 Running the Dashboard Locally

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

## 🌐 Live Dashboard

🔗 *[Add Streamlit Cloud link here after deployment]*

## 👤 Author

**Muhammad Tayyab**
Data Analyst Intern — Teyzix Core
🔗 [LinkedIn](https://linkedin.com/in/muhammad-tayyab-python-uae) | [GitHub](https://github.com/muhammadtayyab-portfolio)