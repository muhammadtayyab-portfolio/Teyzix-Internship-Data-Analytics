import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Electronics Store Sales Dashboard", layout="wide")

# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_csv("electronics_sales_clean.csv")
    df["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"])
    return df

df = load_data()

st.title("📊 Electronics Store Sales & Customer Behavior Dashboard")
st.markdown("**Teyzix Internship — Task 2 (DA-2)** | UAE Electronics Retail Analytics")

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.header("Filters")

city_filter = st.sidebar.multiselect(
    "Customer City", options=sorted(df["Customer_City"].unique()),
    default=sorted(df["Customer_City"].unique())
)
category_filter = st.sidebar.multiselect(
    "Product Category", options=sorted(df["Product_Category"].unique()),
    default=sorted(df["Product_Category"].unique())
)
payment_filter = st.sidebar.multiselect(
    "Payment Method", options=sorted(df["Payment_Method"].unique()),
    default=sorted(df["Payment_Method"].unique())
)
date_range = st.sidebar.date_input(
    "Purchase Date Range",
    value=(df["Purchase_Date"].min(), df["Purchase_Date"].max())
)

# ---- Apply filters ----
filtered = df[
    (df["Customer_City"].isin(city_filter)) &
    (df["Product_Category"].isin(category_filter)) &
    (df["Payment_Method"].isin(payment_filter)) &
    (df["Purchase_Date"] >= pd.to_datetime(date_range[0])) &
    (df["Purchase_Date"] <= pd.to_datetime(date_range[1]))
]

# ============================================
# KPI ROW
# ============================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"AED {filtered['Total_Amount'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered.shape[0]:,}")
col3.metric("Avg Order Value", f"AED {filtered['Total_Amount'].mean():,.2f}")
col4.metric("Unique Customers", f"{filtered['Customer_ID'].nunique():,}")

st.markdown("---")

# ============================================
# ROW 1: Revenue Trend + Category Performance
# ============================================
c1, c2 = st.columns(2)

with c1:
    monthly = filtered.groupby(filtered["Purchase_Date"].dt.to_period("M"))["Total_Amount"].sum().reset_index()
    monthly["Purchase_Date"] = monthly["Purchase_Date"].astype(str)
    fig1 = px.line(monthly, x="Purchase_Date", y="Total_Amount", markers=True,
                    title="Monthly Revenue Trend")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    cat_rev = filtered.groupby("Product_Category")["Total_Amount"].sum().sort_values(ascending=False).reset_index()
    fig2 = px.bar(cat_rev, x="Total_Amount", y="Product_Category", orientation="h",
                  title="Revenue by Category")
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# ROW 2: Geographic Analysis + Top Products
# ============================================
c3, c4 = st.columns(2)

with c3:
    city_rev = filtered.groupby("Customer_City")["Total_Amount"].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(city_rev, x="Total_Amount", y="Customer_City", orientation="h",
                  title="Revenue by City")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    top_products = filtered.groupby("Product_Name")["Quantity"].sum().sort_values(ascending=False).head(10).reset_index()
    fig4 = px.bar(top_products, x="Quantity", y="Product_Name", orientation="h",
                  title="Top 10 Best-Selling Products")
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# ROW 3: Payment Methods + Customer Segments
# ============================================
c5, c6 = st.columns(2)

with c5:
    pay_dist = filtered["Payment_Method"].value_counts().reset_index()
    pay_dist.columns = ["Payment_Method", "Count"]
    fig5 = px.pie(pay_dist, names="Payment_Method", values="Count",
                  title="Payment Method Distribution")
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    if "Segment" in filtered.columns:
        seg_dist = filtered.drop_duplicates("Customer_ID")["Segment"].value_counts().reset_index()
        seg_dist.columns = ["Segment", "Count"]
        fig6 = px.bar(seg_dist, x="Count", y="Segment", orientation="h",
                      title="Customer Segments")
        st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.caption("Built by Muhammad Tayyab | Teyzix Internship — Data Analytics Domain")