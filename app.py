import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Retail Customer Segmentation Dashboard")

# Load data
rfm = pd.read_csv("rfm_data.csv")
# Segment Filter
selected_segment = st.selectbox(
    "Select Customer Segment",
    options=["All"] + list(rfm['Segment'].unique())
)

if selected_segment != "All":
    filtered_rfm = rfm[rfm['Segment'] == selected_segment]
else:
    filtered_rfm = rfm

# KPI Metrics
total_customers = rfm['CustomerID'].nunique()
total_revenue = rfm['Monetary'].sum()
avg_revenue = rfm['Monetary'].mean()
champions_count = rfm[rfm['Segment'] == 'Champions'].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Avg Revenue/Customer", f"${avg_revenue:,.0f}")
col4.metric("Champions", champions_count)


st.subheader("Dataset Preview")
st.dataframe(rfm.head())

st.subheader("Customer Segment Distribution")

segment_counts = filtered_rfm['Segment'].value_counts()

fig, ax = plt.subplots()
ax.bar(segment_counts.index, segment_counts.values)
plt.xticks(rotation=30)

st.pyplot(fig)

st.subheader("Revenue by Segment")

revenue = filtered_rfm.groupby('Segment')['Monetary'].sum()

fig, ax = plt.subplots()
ax.bar(revenue.index, revenue.values)
plt.xticks(rotation=30)

st.pyplot(fig)
