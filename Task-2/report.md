# Electronics Store Sales & Customer Behavior Analysis
**Teyzix Internship Program — Task DA-2**

**Intern:** Muhammad Tayyab
**Domain:** Data Analytics
**Assigned Date:** 20 June 2026
**Submission Deadline:** 29 June 2026

---

## 1. Project Overview

This project simulates an end-to-end data analytics workflow for a UAE-based electronics retail store. Since no ready-made dataset was provided, a realistic synthetic dataset was generated, intentionally injected with common real-world data quality issues, cleaned, analyzed, and presented through an interactive Streamlit dashboard.

The objective was to act as a Data Analyst for the business and answer: *which products, categories, cities, and customer segments drive revenue — and what should the business do about it?*

---

## 2. Dataset Description

The dataset was generated using Python's **Faker** library combined with custom business logic, simulating electronics store transactions across the UAE.

**Size:** 1,200 final records (1,215 generated, including injected duplicates)

**Fields included:**

| Field | Description |
|---|---|
| Transaction_ID | Unique transaction identifier |
| Customer_ID | Customer identifier (pool of 280 customers, enabling repeat-purchase behavior) |
| Customer_Age, Customer_Gender | Demographic fields, kept consistent per customer |
| Product_Category | 10 categories: Mobiles, Laptops, Tablets, Audio, TVs, Gaming, Smart Home, Accessories, Wearables, Cameras |
| Product_Name | Specific product per category |
| Quantity | Units purchased per transaction |
| Unit_Price, Discount_Percent, Total_Amount | Pricing and final transaction value (AED) |
| Purchase_Date | Date of purchase, weighted toward known UAE retail peak periods (Jan/DSF, Nov/Black Friday, Dec/year-end) |
| Customer_City | UAE city: Dubai, Sharjah, Abu Dhabi, Ajman, Al Ain, Ras Al Khaimah, Fujairah |
| Payment_Method | Credit Card, Debit Card, Cash, Apple Pay, Tabby (BNPL) |
| Store_Branch | Mall Branch, Downtown Branch, Online Store, Outlet Branch |
| Rating | Customer satisfaction rating (1-5) |

To simulate a realistic business scenario, the following data quality issues were deliberately introduced before cleaning: missing values, duplicate transactions, inconsistent text formatting, and invalid numeric entries.

---

## 3. Data Cleaning Process

| Issue | Found | Action Taken |
|---|---|---|
| Missing `Customer_City` | 40 records | Filled with "Unknown" (preserves revenue data without dropping rows) |
| Missing `Unit_Price` | 25 records | Imputed using the average price of the corresponding `Product_Category` |
| Missing `Rating` | 50 records | Filled with the dataset median rating |
| Duplicate `Transaction_ID` | 15 records | Removed, keeping the first occurrence |
| Inconsistent city naming (e.g. "dubai ", "DXB", "AbuDhabi") | 8 spelling variants across 7 cities | Standardized via mapping dictionary after trimming/lowercasing |
| Inconsistent payment method casing (e.g. "cash", "CASH") | 5 variants | Standardized via mapping dictionary |
| Invalid `Quantity` (0 or negative) | 10 records | Corrected to a minimum valid value of 1 |
| `Total_Amount` recalculation | — | Recomputed after price/quantity corrections to ensure consistency |

**Result:** Dataset reduced from 1,215 → 1,200 clean records, with zero remaining missing values, zero duplicate transaction IDs, and fully standardized categorical fields.

---

## 4. Analysis Methodology

The analysis was performed using **Python** (Pandas, NumPy, Matplotlib, Seaborn) inside Google Colab, followed by an interactive dashboard built with **Streamlit** and **Plotly**.

Workflow:
1. Synthetic data generation (Faker)
2. Controlled messiness injection
3. Data cleaning and standardization
4. Exploratory Data Analysis (EDA)
5. Business insight generation
6. RFM-based customer segmentation (bonus)
7. Interactive dashboard development

---

## 5. Visualizations & Key Findings

**Monthly Sales Trend:** Revenue peaked in January, November, and December (AED ~655K, ~687K, and ~691K respectively), aligning with the Dubai Shopping Festival and Black Friday/year-end promotional periods. February and August were the weakest months.

**Top-Selling Products (by quantity):** USB-C Cable Pack, Canon EOS R50, iPad Air, Xiaomi Pad 6, and GoPro Hero 12 led in units sold — a mix of low-cost accessories and mid-to-high-value electronics.

**Revenue by Category:** Laptops generated the highest total revenue (~AED 1.15M), followed by TVs (~AED 880K) and Cameras (~AED 745K). Accessories generated the lowest revenue (~AED 40K) despite reasonable unit sales, due to low unit price.

**Revenue by City:** Fujairah and Ras Al Khaimah generated the highest revenue per city (AED ~840K and ~775K), followed by Al Ain, Ajman, Abu Dhabi, Sharjah, and Dubai. Revenue was relatively well-distributed across all seven cities rather than concentrated in one location.

**Customer Purchasing Patterns:** 96% of customers were repeat buyers, with only 4% making a single purchase — indicating strong customer retention.

**Payment Method Distribution:** Fairly even spread across Debit Card, Tabby (BNPL), Apple Pay, Cash, and Credit Card (roughly 225-250 transactions each), showing no single dominant payment preference.

**Average Order Value (AOV):** AED 3,914.99 overall. By category, Laptops had the highest AOV (AED 8,614), followed by TVs (AED 7,781) and Cameras (AED 6,313). Accessories had the lowest AOV (AED 314).

---

## 6. Business Insights

**Best-Performing Products/Categories**
- Laptops generated the highest total revenue despite moderate unit sales, driven by a high average order value.
- Canon EOS R50 was a standout performer in both unit sales and category revenue contribution.
- TVs were the second-highest revenue category, reinforcing that high-ticket electronics drive overall sales.

**Underperforming Categories**
- Accessories generated the lowest total revenue despite reasonable sales volume, due to its low price point.
- Smart Home and Audio categories underperformed relative to unit sales, suggesting limited cross-sell or bundling.

**Seasonal Trends**
- Clear peaks in January, November, and December align with the Dubai Shopping Festival and Black Friday/year-end promotions.
- February and August were the weakest months, reflecting a post-holiday demand drop and a typical summer slowdown.

**Customer Behavior Patterns**
- A 96% repeat-purchase rate indicates strong customer loyalty rather than one-off buying.
- Payment preferences were evenly distributed, with digital/flexible options (Tabby BNPL, Apple Pay) performing on par with traditional cards — showing a shift toward flexible payment adoption.

**Customer Segmentation (RFM Analysis)**

| Segment | Customers | Avg. Spend (AED) |
|---|---|---|
| High-Value | 78 | 30,594 |
| Loyal/Regular | 87 | 15,703 |
| At-Risk | 95 | 9,375 |
| Low-Engagement | 16 | 3,431 |

The largest segment (At-Risk, 95 customers) represents customers who were previously active but have not purchased recently — a key re-engagement opportunity. High-Value customers, while fewer in number, contribute disproportionately to revenue (nearly 9x the spend of Low-Engagement customers).

---

## 7. Recommendations

1. **Bundle low-revenue Accessories with high-ticket items** (e.g. a free cable or sleeve with a Laptop/Camera purchase) to lift Accessories revenue and increase basket size.
2. **Run targeted promotions during low-demand months** (February, April, August) to flatten the seasonal dip — e.g. mid-year clearance or loyalty discounts.
3. **Launch a re-engagement campaign for the At-Risk segment** (95 customers, the largest group) through personalized offers, since they have purchase history but reduced recent activity.
4. **Introduce a loyalty/rewards program** to convert Loyal/Regular customers into High-Value customers, leveraging the already-strong 96% repeat-purchase behavior.
5. **Prioritize stock and marketing budget for Laptops, TVs, and Cameras ahead of the Nov-Jan peak**, given their outsized contribution to revenue during this period.
6. **Promote BNPL (Tabby) more visibly at checkout**, since adoption is already comparable to traditional cards and could further lift conversion on high-ticket categories.

---

## 8. Tools & Technologies Used

- **Python** — Pandas, NumPy, Faker (data generation), Matplotlib, Seaborn (EDA)
- **Streamlit + Plotly** — Interactive dashboard
- **Google Colab** — Development environment
- **GitHub** — Version control and project hosting

---

*Prepared by Muhammad Tayyab — Teyzix Internship Program, June 2026 Batch*
