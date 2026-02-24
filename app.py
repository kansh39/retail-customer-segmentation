import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Customer Intelligence", layout="wide")

st.title("🛒 Retail Customer Segmentation Dashboard")

# Load data
rfm = pd.read_csv("rfm_data.csv")

# ---------------------------
# Segment Filter
# ---------------------------
selected_segment = st.selectbox(
    "Select Customer Segment",
    options=["All"] + list(rfm['Segment'].unique())
)

if selected_segment != "All":
    filtered_rfm = rfm[rfm['Segment'] == selected_segment]
else:
    filtered_rfm = rfm

# ---------------------------
# KPI Metrics
# ---------------------------
total_customers = rfm['CustomerID'].nunique()
total_revenue = rfm['Monetary'].sum()
avg_revenue = rfm['Monetary'].mean()
champions_count = rfm[rfm['Segment'] == 'Champions'].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Avg Revenue/Customer", f"${avg_revenue:,.0f}")
col4.metric("Champions", champions_count)

st.markdown("---")
st.header("Customer Analytics Dashboard")

# ---------------------------
# Dataset Preview
# ---------------------------
st.subheader("Dataset Preview")
st.dataframe(rfm.head())

# ---------------------------
# Segment Distribution Chart
# ---------------------------
st.subheader("Customer Segment Distribution")

segment_counts = filtered_rfm['Segment'].value_counts()

fig, ax = plt.subplots(figsize=(8,4))

colors = ['#2E86C1','#28B463','#F39C12','#E74C3C']

bars = ax.bar(segment_counts.index, segment_counts.values, color=colors)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, height,
            int(height), ha='center', va='bottom')

plt.xticks(rotation=25)
plt.grid(axis='y', linestyle='--', alpha=0.4)

st.pyplot(fig)

# ---------------------------
# Revenue Chart
# ---------------------------
st.subheader("Revenue Contribution by Segment")

revenue = filtered_rfm.groupby('Segment')['Monetary'].sum()

fig, ax = plt.subplots(figsize=(8,4))

colors = ['#1ABC9C','#3498DB','#9B59B6','#F4D03F']

bars = ax.bar(revenue.index, revenue.values, color=colors)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, height,
            f'{int(height):,}', ha='center', va='bottom')

plt.xticks(rotation=25)
plt.grid(axis='y', linestyle='--', alpha=0.4)

st.pyplot(fig)

# ---------------------------
# Business Insights Section
# ---------------------------
st.markdown("---")
st.subheader("Business Insights")

st.write("""
- Champion customers generate the highest revenue and should be prioritized with VIP programs.
- Loyal customers provide stable repeat revenue and respond well to retention strategies.
- Lost customers represent churn risk and require reactivation campaigns.
- New customers need onboarding and personalized engagement.
""")

# ---------------------------
# K-Means Cluster Insights
# ---------------------------
st.markdown("---")
st.subheader("K-Means Cluster Insights")

cluster_summary = rfm.groupby('Cluster')[['Recency','Frequency','Monetary']].mean()
st.dataframe(cluster_summary)

st.write("""
Cluster 0 → Regular customers  
Cluster 1 → Inactive customers  
Cluster 2 → Elite high-spending customers  
Cluster 3 → High-value frequent buyers
""")
