import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv


import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

load_dotenv()
# ─── CONFIG ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STREAMLIT_DIR = os.path.join(BASE_DIR, 'streamlit_app')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

# ─── LOAD MODEL ───────────────────────────────────────────
print("Loading model...")
model = joblib.load(os.path.join(STREAMLIT_DIR, 'churn_model.pkl'))
scaler = joblib.load(os.path.join(STREAMLIT_DIR, 'scaler.pkl'))
feature_columns = joblib.load(os.path.join(STREAMLIT_DIR, 'feature_columns.pkl'))

# ─── LOAD DATA ────────────────────────────────────────────
print("Loading dataset...")
df = pd.read_csv(os.path.join(BASE_DIR, 'WA_Fn-UseC_-Telco-Customer-Churn.csv'))

# ─── PREPROCESSING ────────────────────────────────────────
print("Preprocessing...")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

# Feature Engineering
df['tenure_group'] = df['tenure'].apply(
    lambda x: 0 if x <= 12 else (1 if x <= 48 else 2))
df['avg_monthly_spend'] = df['TotalCharges'] / df['tenure']
df['avg_monthly_spend'] = df['avg_monthly_spend'].fillna(0)

service_cols_raw = ['PhoneService', 'OnlineSecurity', 'OnlineBackup',
                    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
df['services_count'] = df[service_cols_raw].apply(
    lambda row: sum(1 for v in row if v == 'Yes'), axis=1)
df['has_internet'] = df['InternetService'].apply(lambda x: 0 if x == 'No' else 1)

# Encode
df_encoded = pd.get_dummies(df.drop(columns=['customerID', 'Churn']),
                             drop_first=True)
df_encoded = df_encoded.astype({col: int for col in df_encoded.select_dtypes(bool).columns})

# Align columns
for col in feature_columns:
    if col not in df_encoded.columns:
        df_encoded[col] = 0
df_encoded = df_encoded[feature_columns]

# ─── PREDICT ──────────────────────────────────────────────
print("Predicting churn...")
X_scaled = scaler.transform(df_encoded.values)
probs = model.predict_proba(X_scaled)[:, 1]

df['churn_probability'] = probs
df['risk_category'] = df['churn_probability'].apply(
    lambda p: 'High Risk 🔴' if p >= 0.6 else ('Medium Risk 🟡' if p >= 0.3 else 'Low Risk 🟢'))

# ─── REPORT ───────────────────────────────────────────────
today = datetime.now().strftime('%Y-%m-%d')
report_path = os.path.join(REPORTS_DIR, f'churn_report_{today}.csv')

# High risk customers
high_risk = df[df['risk_category'] == 'High Risk 🔴'][[
    'customerID', 'tenure', 'MonthlyCharges',
    'Contract', 'InternetService',
    'churn_probability', 'risk_category'
]].sort_values('churn_probability', ascending=False)

high_risk.to_csv(report_path, index=False)

# ─── SUMMARY ──────────────────────────────────────────────
print("\n" + "="*50)
print(f"📅 Weekly Churn Report — {today}")
print("="*50)
print(f"Total Customers Analyzed : {len(df)}")
print(f"🔴 High Risk             : {len(df[df['risk_category'] == 'High Risk 🔴'])}")
print(f"🟡 Medium Risk           : {len(df[df['risk_category'] == 'Medium Risk 🟡'])}")
print(f"🟢 Low Risk              : {len(df[df['risk_category'] == 'Low Risk 🟢'])}")
print(f"\n💸 Revenue at Risk       : ${high_risk['MonthlyCharges'].sum():,.2f}/month")
print(f"📁 Report saved          : {report_path}")
print("="*50)

# ─── EMAIL REPORT ─────────────────────────────────────────
def send_email_report(report_path, summary):
    sender = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')
    receiver = os.getenv('EMAIL_RECEIVER')

    # Email setup
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = f"📊 Weekly Churn Report — {today}"

    # Email body
    body = f"""
    <html><body style="font-family: Arial; color: #333;">
        <h2 style="color: #667eea;">🔍 Weekly Churn Report</h2>
        <p>Date: <b>{today}</b></p>
        <hr>
        <h3>📊 Summary</h3>
        <table border="1" cellpadding="8" style="border-collapse: collapse;">
            <tr style="background: #667eea; color: white;">
                <th>Category</th><th>Count</th>
            </tr>
            <tr><td>Total Customers</td><td>{summary['total']}</td></tr>
            <tr style="color: red;"><td>🔴 High Risk</td><td>{summary['high']}</td></tr>
            <tr style="color: orange;"><td>🟡 Medium Risk</td><td>{summary['medium']}</td></tr>
            <tr style="color: green;"><td>🟢 Low Risk</td><td>{summary['low']}</td></tr>
            <tr><td>💸 Revenue at Risk</td><td>${summary['revenue']:,.2f}/month</td></tr>
        </table>
        <br>
        <p>📁 Full report attached as CSV.</p>
        <hr>
        <p style="color: #888; font-size: 12px;">
            Generated by Churn Prediction Pipeline | Teyzix Core Internship
        </p>
    </body></html>
    """

    msg.attach(MIMEText(body, 'html'))

    # Attach CSV
    with open(report_path, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                            f'attachment; filename=churn_report_{today}.csv')
        msg.attach(attachment)

    # Send
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print(f"\n✅ Email sent successfully to {receiver}!")
    except Exception as e:
        print(f"\n❌ Email failed: {e}")

# Call email function
summary = {
    'total': len(df),
    'high': len(df[df['risk_category'] == 'High Risk 🔴']),
    'medium': len(df[df['risk_category'] == 'Medium Risk 🟡']),
    'low': len(df[df['risk_category'] == 'Low Risk 🟢']),
    'revenue': high_risk['MonthlyCharges'].sum()
}

send_email_report(report_path, summary)