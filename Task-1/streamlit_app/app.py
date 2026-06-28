import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, 'churn_model.pkl')

# Page config
st.set_page_config(
    page_title="Churn Prediction Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2d3250);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #3d4470;
        margin: 5px;
    }
    .high-risk { border-left: 5px solid #ff4b4b; }
    .medium-risk { border-left: 5px solid #ffa500; }
    .low-risk { border-left: 5px solid #00cc96; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
        transform: scale(1.02);
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2130, #2d3250);
        border: 1px solid #3d4470;
        border-radius: 10px;
        padding: 15px;
    }
    .section-header {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border-left: 4px solid #667eea;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load(model_path)
scaler = joblib.load(os.path.join(BASE_DIR,'scaler.pkl'))
feature_columns = joblib.load(os.path.join(BASE_DIR,'feature_columns.pkl'))
shap_vals = joblib.load(os.path.join(BASE_DIR,'shap_values.pkl'))  

# ─── HEADER ───────────────────────────────────────────────
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #667eea; font-size: 2.5em; margin-bottom: 5px;'>
            🔍 Customer Churn Prediction Dashboard
        </h1>
        <p style='color: #888; font-size: 1.1em;'>
            Teyzix Core Internship &nbsp;|&nbsp; DA-INT-1 &nbsp;|&nbsp; Muhammad Tayyab
        </p>
    </div>
    <hr style='border: 1px solid #3d4470; margin-bottom: 25px;'>
""", unsafe_allow_html=True)

# ─── OVERVIEW METRICS ─────────────────────────────────────
st.markdown("<div class='section-header'><b>📊 Business Overview</b></div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👥 Total Customers", "7,043", delta=None)
with col2:
    st.metric("📉 Churn Rate", "26.5%", delta="-2.1% vs last month", delta_color="inverse")
with col3:
    st.metric("💸 Monthly Loss", "$121,039", delta=None)
with col4:
    st.metric("📅 Annual Loss", "$1.45M", delta=None)

st.markdown("<br>", unsafe_allow_html=True)

# ─── CHARTS ROW ───────────────────────────────────────────
st.markdown("<div class='section-header'><b>📈 Analytics Overview</b></div>", unsafe_allow_html=True)

chart1, chart2, chart3 = st.columns(3)

# Chart 1 — Pie Chart Customer Segments
with chart1:
    st.markdown("**👥 Customer Segments**")
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    fig1.patch.set_facecolor('#0e1117')
    ax1.set_facecolor('#0e1117')
    sizes = [21.0, 32.2, 46.7]
    labels = ['High Value\n21%', 'Medium Value\n32.2%', 'Low Value\n46.7%']
    colors = ['#00cc96', '#667eea', '#ff4b4b']
    explode = (0.05, 0.05, 0.05)
    wedges, texts = ax1.pie(sizes, explode=explode, labels=labels,
                             colors=colors, startangle=90,
                             textprops={'color': 'white', 'fontsize': 9},
                             wedgeprops={'linewidth': 2, 'edgecolor': '#0e1117'})
    ax1.set_title('Customer Segments', color='white', fontsize=11, pad=10)
    st.pyplot(fig1)

# Chart 2 — Bar Chart Churn by Contract
with chart2:
    st.markdown("**📄 Churn by Contract Type**")
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    fig2.patch.set_facecolor('#0e1117')
    ax2.set_facecolor('#0e1117')
    contracts = ['Month-to-\nmonth', 'One\nyear', 'Two\nyear']
    churn_rates = [42.7, 11.3, 2.8]
    colors_bar = ['#ff4b4b', '#ffa500', '#00cc96']
    bars = ax2.bar(contracts, churn_rates, color=colors_bar,
                   edgecolor='#0e1117', linewidth=1.5, width=0.5)
    for bar, val in zip(bars, churn_rates):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val}%', ha='center', va='bottom', color='white', fontsize=9)
    ax2.set_ylabel('Churn Rate %', color='white', fontsize=9)
    ax2.set_title('Churn by Contract', color='white', fontsize=11)
    ax2.tick_params(colors='white', labelsize=8)
    ax2.set_ylim(0, 55)
    for spine in ax2.spines.values():
        spine.set_color('#3d4470')
    ax2.set_facecolor('#1e2130')
    ax2.yaxis.grid(True, color='#3d4470', linestyle='--', alpha=0.5)
    ax2.set_axisbelow(True)
    st.pyplot(fig2)

# Chart 3 — Churn by Tenure Group
with chart3:
    st.markdown("**📅 Churn by Tenure Group**")
    fig3, ax3 = plt.subplots(figsize=(4, 4))
    fig3.patch.set_facecolor('#0e1117')
    ax3.set_facecolor('#1e2130')
    groups = ['New\n(0-12m)', 'Mid\n(12-48m)', 'Loyal\n(48m+)']
    churn_pct = [47.4, 26.3, 9.8]
    colors3 = ['#ff4b4b', '#ffa500', '#00cc96']
    bars3 = ax3.barh(groups, churn_pct, color=colors3,
                     edgecolor='#0e1117', linewidth=1.5, height=0.4)
    for bar, val in zip(bars3, churn_pct):
        ax3.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', color='white', fontsize=9)
    ax3.set_xlabel('Churn Rate %', color='white', fontsize=9)
    ax3.set_title('Churn by Tenure', color='white', fontsize=11)
    ax3.tick_params(colors='white', labelsize=8)
    ax3.set_xlim(0, 60)
    for spine in ax3.spines.values():
        spine.set_color('#3d4470')
    ax3.xaxis.grid(True, color='#3d4470', linestyle='--', alpha=0.5)
    ax3.set_axisbelow(True)
    st.pyplot(fig3)

st.markdown("<br>", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────
st.sidebar.markdown("""
    <div style='text-align:center; padding: 10px;'>
        <h2 style='color: #667eea;'>📋 Customer Input</h2>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("**📊 Usage & Billing**")
tenure = st.sidebar.slider('📅 Tenure (Months)', 0, 72, 12)
monthly_charges = st.sidebar.slider('💰 Monthly Charges ($)', 18, 119, 65)
total_charges = tenure * monthly_charges

st.sidebar.markdown("---")
st.sidebar.markdown("**📄 Contract & Service**")
contract = st.sidebar.selectbox('Contract Type',
    ['Month-to-month', 'One year', 'Two year'])
internet = st.sidebar.selectbox('Internet Service',
    ['DSL', 'Fiber optic', 'No'])
payment = st.sidebar.selectbox('Payment Method',
    ['Electronic check', 'Mailed check',
     'Bank transfer (automatic)', 'Credit card (automatic)'])

st.sidebar.markdown("---")
st.sidebar.markdown("**👤 Demographics**")
senior = st.sidebar.checkbox('👴 Senior Citizen')
partner = st.sidebar.checkbox('👫 Has Partner')
dependents = st.sidebar.checkbox('👨‍👧 Has Dependents')

st.sidebar.markdown("---")
st.sidebar.markdown(f"💵 **Estimated Total Charges:** ${total_charges:,}")
predict_btn = st.sidebar.button('🔮 Predict Churn Risk')

# ─── PREDICTION ───────────────────────────────────────────
if predict_btn:
    input_dict = {
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges,
        'avg_monthly_spend': monthly_charges,
        'services_count': 3,
        'has_internet': 0 if internet == 'No' else 1,
        'tenure_group': 0 if tenure <= 12 else (1 if tenure <= 48 else 2),
        'gender_Male': 0,
        'SeniorCitizen_1': 1 if senior else 0,
        'Partner_Yes': 1 if partner else 0,
        'Dependents_Yes': 1 if dependents else 0,
        'PhoneService_Yes': 1,
        'MultipleLines_No phone service': 0,
        'MultipleLines_Yes': 0,
        'InternetService_Fiber optic': 1 if internet == 'Fiber optic' else 0,
        'InternetService_No': 1 if internet == 'No' else 0,
        'OnlineSecurity_No internet service': 0,
        'OnlineSecurity_Yes': 0,
        'OnlineBackup_No internet service': 0,
        'OnlineBackup_Yes': 0,
        'DeviceProtection_No internet service': 0,
        'DeviceProtection_Yes': 0,
        'TechSupport_No internet service': 0,
        'TechSupport_Yes': 0,
        'StreamingTV_No internet service': 0,
        'StreamingTV_Yes': 0,
        'StreamingMovies_No internet service': 0,
        'StreamingMovies_Yes': 0,
        'Contract_One year': 1 if contract == 'One year' else 0,
        'Contract_Two year': 1 if contract == 'Two year' else 0,
        'PaperlessBilling_Yes': 0,
        'PaymentMethod_Credit card (automatic)': 1 if payment == 'Credit card (automatic)' else 0,
        'PaymentMethod_Electronic check': 1 if payment == 'Electronic check' else 0,
        'PaymentMethod_Mailed check': 1 if payment == 'Mailed check' else 0,
    }

    input_df = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df[feature_columns].values)
    prob = model.predict_proba(input_scaled)[0][1]
    retention = 1 - prob

    if prob < 0.3:
        risk = '🟢 Low Risk'
        color = '#00cc96'
        risk_class = 'low-risk'
        risk_emoji = '✅'
    elif prob < 0.6:
        risk = '🟡 Medium Risk'
        color = '#ffa500'
        risk_class = 'medium-risk'
        risk_emoji = '⚠️'
    else:
        risk = '🔴 High Risk'
        color = '#ff4b4b'
        risk_class = 'high-risk'
        risk_emoji = '🚨'

    # Results Header
    st.markdown("<div class='section-header'><b>🎯 Prediction Results</b></div>", unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""
            <div class='metric-card {risk_class}'>
                <h2 style='color: {color}; font-size: 2em;'>{prob*100:.1f}%</h2>
                <p style='color: #aaa; margin: 0;'>Churn Probability</p>
            </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
            <div class='metric-card {risk_class}'>
                <h2 style='color: {color}; font-size: 1.5em;'>{risk}</h2>
                <p style='color: #aaa; margin: 0;'>Risk Category</p>
            </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
            <div class='metric-card low-risk'>
                <h2 style='color: #00cc96; font-size: 2em;'>{retention*100:.1f}%</h2>
                <p style='color: #aaa; margin: 0;'>Retention Probability</p>
            </div>
        """, unsafe_allow_html=True)
    with r4:
        monthly_risk = monthly_charges * prob
        st.markdown(f"""
            <div class='metric-card'>
                <h2 style='color: #667eea; font-size: 2em;'>${monthly_risk:.0f}</h2>
                <p style='color: #aaa; margin: 0;'>Revenue at Risk/Month</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gauge + Customer Info
    g1, g2 = st.columns([1.5, 1])

    with g1:
        st.markdown("**📊 Churn Probability Gauge**")
        fig_g, ax_g = plt.subplots(figsize=(7, 2.5))
        fig_g.patch.set_facecolor('#0e1117')
        ax_g.set_facecolor('#1e2130')

        # Background bar
        ax_g.barh(['Risk'], [100], color='#2d3250', height=0.5, edgecolor='#3d4470')
        # Low zone
        ax_g.barh(['Risk'], [30], color='#00cc9633', height=0.5)
        # Medium zone
        ax_g.barh(['Risk'], [30], left=30, color='#ffa50033', height=0.5)
        # High zone
        ax_g.barh(['Risk'], [40], left=60, color='#ff4b4b33', height=0.5)
        # Actual probability
        ax_g.barh(['Risk'], [prob*100], color=color, height=0.3, alpha=0.9)

        ax_g.axvline(x=30, color='#00cc96', linestyle='--', alpha=0.7, linewidth=1.5)
        ax_g.axvline(x=60, color='#ffa500', linestyle='--', alpha=0.7, linewidth=1.5)
        ax_g.axvline(x=prob*100, color=color, linestyle='-', linewidth=3)

        ax_g.text(15, 0.6, 'LOW', ha='center', color='#00cc96', fontsize=9, fontweight='bold')
        ax_g.text(45, 0.6, 'MEDIUM', ha='center', color='#ffa500', fontsize=9, fontweight='bold')
        ax_g.text(80, 0.6, 'HIGH', ha='center', color='#ff4b4b', fontsize=9, fontweight='bold')
        ax_g.text(prob*100, -0.45, f'{prob*100:.1f}%', ha='center',
                 color=color, fontsize=12, fontweight='bold')

        ax_g.set_xlim(0, 100)
        ax_g.set_xlabel('Churn Probability %', color='white', fontsize=9)
        ax_g.tick_params(colors='white', labelsize=8)
        for spine in ax_g.spines.values():
            spine.set_color('#3d4470')
        st.pyplot(fig_g)

    with g2:
        st.markdown("**👤 Customer Profile**")
        st.markdown(f"""
            <div class='metric-card'>
                <table style='width:100%; color: white; font-size: 13px;'>
                    <tr><td>📅 Tenure</td><td><b>{tenure} months</b></td></tr>
                    <tr><td>💰 Monthly</td><td><b>${monthly_charges}</b></td></tr>
                    <tr><td>💵 Total</td><td><b>${total_charges:,}</b></td></tr>
                    <tr><td>📄 Contract</td><td><b>{contract}</b></td></tr>
                    <tr><td>🌐 Internet</td><td><b>{internet}</b></td></tr>
                    <tr><td>💳 Payment</td><td><b>{payment.split('(')[0]}</b></td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Recommendation
    st.markdown("<div class='section-header'><b>💡 Action Recommendation</b></div>", unsafe_allow_html=True)

    if prob >= 0.6:
        st.error(f"""
        🚨 **HIGH RISK CUSTOMER — Immediate Action Required!**

        **Recommended Actions:**
        - 🎁 Offer 20-30% discount on annual contract upgrade
        - 📞 Assign dedicated customer success manager
        - 🔧 Conduct service quality review immediately
        - 💌 Send personalized retention email within 24 hours
        - 🎯 Revenue at risk: **${monthly_charges * 12:,}/year**
        """)
    elif prob >= 0.3:
        st.warning(f"""
        ⚠️ **MEDIUM RISK — Proactive Retention Needed**

        **Recommended Actions:**
        - 📧 Send personalized loyalty offer within 1 week
        - 📊 Monitor usage patterns closely
        - 🔄 Suggest contract upgrade with incentive
        - 📱 Check service satisfaction via survey
        """)
    else:
        st.success(f"""
        ✅ **LOW RISK — Customer is Loyal & Satisfied!**

        **Recommended Actions:**
        - 🌟 Enroll in VIP loyalty program
        - ⬆️ Upsell premium features or add-ons
        - 🎁 Reward with exclusive benefits
        - 📣 Consider for referral program
        """)
    
    # SHAP Section
    st.markdown("<div class='section-header'><b>🔬 SHAP Feature Importance</b></div>", unsafe_allow_html=True)

    fig_shap, ax_shap = plt.subplots(figsize=(8, 6))
    fig_shap.patch.set_facecolor('#0e1117')
    ax_shap.set_facecolor('#1e2130')

    # Top 10 features
    feature_importance = pd.DataFrame({
        'Feature': feature_columns,
        'Importance': abs(shap_vals).mean(axis=0)
    }).sort_values('Importance', ascending=True).tail(10)

    bars = ax_shap.barh(feature_importance['Feature'], 
                        feature_importance['Importance'],
                        color='#667eea', edgecolor='#0e1117')

    ax_shap.set_xlabel('Mean |SHAP Value|', color='white', fontsize=9)
    ax_shap.set_title('Top 10 Most Important Features', color='white', fontsize=11)
    ax_shap.tick_params(colors='white', labelsize=8)
    for spine in ax_shap.spines.values():
        spine.set_color('#3d4470')
    ax_shap.set_facecolor('#1e2130')
    ax_shap.xaxis.grid(True, color='#3d4470', linestyle='--', alpha=0.5)

    st.pyplot(fig_shap)
    st.caption("💡 Higher value = More impact on churn prediction")

else:
    # Default landing view
    st.markdown("<div class='section-header'><b>🚀 How to Use This Dashboard</b></div>", unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown("""
            <div class='metric-card'>
                <h3 style='color: #667eea;'>1️⃣ Enter Details</h3>
                <p style='color: #aaa;'>Fill in customer information in the sidebar — tenure, charges, contract type, and more.</p>
            </div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown("""
            <div class='metric-card'>
                <h3 style='color: #667eea;'>2️⃣ Click Predict</h3>
                <p style='color: #aaa;'>Our ML model (Logistic Regression, 82% accuracy) will analyze the customer profile instantly.</p>
            </div>
        """, unsafe_allow_html=True)
    with h3:
        st.markdown("""
            <div class='metric-card'>
                <h3 style='color: #667eea;'>3️⃣ Take Action</h3>
                <p style='color: #aaa;'>Get risk category, churn probability, and personalized retention recommendations.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Risk categories info
    st.markdown("<div class='section-header'><b>🎯 Risk Categories</b></div>", unsafe_allow_html=True)
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.markdown("""
            <div class='metric-card low-risk'>
                <h3 style='color: #00cc96;'>🟢 Low Risk</h3>
                <h4 style='color: white;'>< 30% Churn Probability</h4>
                <p style='color: #aaa;'>Customer is loyal and satisfied. Focus on upselling and rewarding loyalty.</p>
            </div>
        """, unsafe_allow_html=True)
    with rc2:
        st.markdown("""
            <div class='metric-card medium-risk'>
                <h3 style='color: #ffa500;'>🟡 Medium Risk</h3>
                <h4 style='color: white;'>30-60% Churn Probability</h4>
                <p style='color: #aaa;'>Customer needs attention. Send retention offers and monitor closely.</p>
            </div>
        """, unsafe_allow_html=True)
    with rc3:
        st.markdown("""
            <div class='metric-card high-risk'>
                <h3 style='color: #ff4b4b;'>🔴 High Risk</h3>
                <h4 style='color: white;'>> 60% Churn Probability</h4>
                <p style='color: #aaa;'>Immediate action required! Assign support agent and offer special discount.</p>
            </div>
        """, unsafe_allow_html=True)
    
# ─── EMAIL REPORT SECTION ─────────────────────────────────
st.markdown("<div class='section-header'><b>📧 Send Churn Report via Email</b></div>", unsafe_allow_html=True)

e1, e2 = st.columns(2)

with e1:
    receiver_email = st.text_input('📮 Enter Email Address', placeholder='example@gmail.com')

with e2:
    uploaded_file = st.file_uploader('📁 Upload CSV Report', type=['csv'])

send_btn = st.button('📧 Send Report to Email')

if send_btn:
    if not receiver_email:
        st.error('❌ Please enter an email address!')
    elif not uploaded_file:
        st.error('❌ Please upload a CSV file!')
    else:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        from dotenv import load_dotenv
        from datetime import datetime
        load_dotenv()

        try:
            sender = os.getenv('EMAIL_SENDER')
            password = os.getenv('EMAIL_PASSWORD')
            today = datetime.now().strftime('%Y-%m-%d')

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver_email
            msg['Subject'] = f"📊 Customer Churn Report — {today}"

            body = f"""
            <html><body style="font-family: Arial; color: #333;">
                <h2 style="color: #667eea;">🔍 Customer Churn Report</h2>
                <p>Date: <b>{today}</b></p>
                <hr>
                <p>Please find the attached churn analysis report.</p>
                <br>
                <p style="color: #888; font-size: 12px;">
                    Generated by Churn Prediction Dashboard<br>
                    Teyzix Core Internship | DA-INT-1 | Muhammad Tayyab
                </p>
            </body></html>
            """
            msg.attach(MIMEText(body, 'html'))

            # Attach uploaded CSV
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(uploaded_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition',
                                f'attachment; filename={uploaded_file.name}')
            msg.attach(attachment)

            # Send
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver_email, msg.as_string())
            server.quit()

            st.success(f'✅ Report sent successfully to {receiver_email}!')

        except Exception as e:
            st.error(f'❌ Failed to send email: {e}')

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <hr style='border: 1px solid #3d4470;'>
    <p style='text-align: center; color: #555; font-size: 12px;'>
        Built by Muhammad Tayyab &nbsp;|&nbsp; Teyzix Core Internship DA-INT-1 &nbsp;|&nbsp; 
        Powered by Logistic Regression + Streamlit
    </p>
""", unsafe_allow_html=True)