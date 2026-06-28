# 🔍 Customer Churn Prediction Dashboard

### Teyzix Core Internship | Task DA-INT-1 | June 2026

---

## 🌐 Live Demo

🚀 **Try the Live App:**
👉 [https://teyzix-internship-data-analytics-muhammadtayyab.streamlit.app/](https://muhammadtayyab-portfolio-hc4dkprqerwgvjsbsvxsjq.streamlit.app/)

---

## 📌 Project Overview

An end-to-end Customer Behavior Analytics & Churn Prediction system built for Teyzix Core Internship. This project analyzes telecom customer data to predict churn probability and generate actionable business insights.

---

## 🎯 Objective

Build a complete ML pipeline that:

* Analyzes customer behavior patterns
* Predicts churn probability using Machine Learning
* Segments customers by value
* Provides actionable business recommendations

---

## 📊 Dataset

- **Source:** [Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Size:** 7,043 customers | 21 features
- **Target:** Churn (Yes/No)
- **Note:** Dataset not included due to licensing. Download from Kaggle link above.

---

## 🛠️ Tech Stack

| Tool                 | Purpose                       |
| -------------------- | ------------------------------|
| Python               | Core language                 |
| Pandas & NumPy       | Data manipulation             |
| Matplotlib & Seaborn | Visualizations                |
| Scikit-learn         | ML Models                     |
| Streamlit            | Interactive Dashboard         |
| Joblib               | Model serialization           |
| SHAP                 | Model explainability          |
| SMTP / Gmail         | Email report automation       |
| python-dotenv        | Secure credentials management |
---

## 📁 Project Structure

```
Task-1/
├── streamlit_app/
│   ├── app.py                  # Streamlit dashboard
│   ├── churn_model.pkl         # Trained ML model
│   ├── scaler.pkl              # Feature scaler
│   └── feature_columns.pkl     # Feature columns
├── DA_INT_1_Customer_Churn_Analysis.ipynb  # Main notebook
├── requirements.txt                        # exact versions, current environment
├── requirements_minimal.txt                # anyone can install easily
└── README.md                               # Project documentation
├── weekly_pipeline.py          # Automated weekly churn pipeline
├── reports/                    # Generated CSV reports
└── .env                        # Email credentials (not in GitHub)
```

---

## 🔬 Project Pipeline

### 1️⃣ Exploratory Data Analysis (EDA)

* Dataset shape, dtypes, missing values
* Churn distribution analysis
* Visualizations — Gender, Contract, Tenure

### 2️⃣ Data Cleaning

* TotalCharges — string to numeric conversion
* 11 hidden missing values dropped
* Churn encoded — Yes/No → 1/0
* Categorical encoding — get_dummies()
* Boolean → Integer conversion

### 3️⃣ Feature Engineering

* `tenure_group` — New/Mid/Loyal (0/1/2)
* `avg_monthly_spend` — TotalCharges/tenure
* `services_count` — total services used
* `has_internet` — internet service flag

### 4️⃣ Machine Learning Models

| Model               | Accuracy | ROC-AUC | Class 1 Recall |
| ------------------- | -------- | ------- | -------------- |
| Logistic Regression | 75%      | 0.773   | 0.82 ✅         |
| Random Forest       | 80%      | 0.686   | 0.45           |

**Winner: Logistic Regression** — better churn detection (82% recall)

### 5️⃣ Customer Segmentation

| Segment         | Customers   | Churn Rate |
| --------------- | ----------- | ---------- |
| 🥇 High Value   | 1,481 (21%) | Low        |
| 🥈 Medium Value | 2,271 (32%) | Medium     |
| 🥉 Low Value    | 3,291 (47%) | High       |

### 6️⃣ Business Insights

* 💸 **Annual Revenue Loss:** $1,452,475
* 📉 **Month-to-month** customers churn 42.7%
* 🆕 **New customers** (0-12 months) highest risk
* 📡 **Fiber optic** users churn more despite higher charges

---

## 🚀 How to Run

### Jupyter Notebook

Open `DA_INT_1_Customer_Churn_Analysis.ipynb` in Google Colab or Jupyter

### Streamlit Dashboard

```bash
# Install dependencies for exact versions, current environment
pip install -r requirements.txt

# Install dependencies for minimal setup
pip install -r requirements_minimal.txt

# Run dashboard
cd streamlit_app
streamlit run app.py
```

---

## 📈 Results Summary

* ✅ ML Model Accuracy: **75-80%**
* ✅ Churn Detection Recall: **82%**
* ✅ Customer Segments: **3 tiers**
* ✅ Business Insights: **4 key findings**
* ✅ Interactive Dashboard: **Streamlit**
* ✅ SHAP Explainability: **Feature importance visualized**
* ✅ Email Automation: **CSV report via Streamlit dashboard**
* ✅ Weekly Pipeline: **Automated churn analysis script**

---

## 👤 Author

**Muhammad Tayyab**
Data Analyst Intern | Teyzix Core
Ref ID: TC-INT-20260606-661

🔗 LinkedIn: https://linkedin.com/in/muhammad-tayyab-python-uae
💻 GitHub: https://github.com/muhammadtayyab-portfolio

---

*Built with ❤️ as part of TEYZIX CORE Data Analytics Internship — June 2026*
