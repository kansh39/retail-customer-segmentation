import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Retail Customer Segmentation Dashboard")

# Load data
rfm = pd.read_csv("rfm_data.csv")

st.subheader("Dataset Preview")
st.dataframe(rfm.head())

st.subheader("Customer Segment Distribution")

segment_counts = rfm['Segment'].value_counts()

fig, ax = plt.subplots()
ax.bar(segment_counts.index, segment_counts.values)
plt.xticks(rotation=30)

st.pyplot(fig)

st.subheader("Revenue by Segment")

revenue = rfm.groupby('Segment')['Monetary'].sum()

fig, ax = plt.subplots()
ax.bar(revenue.index, revenue.values)
plt.xticks(rotation=30)

st.pyplot(fig)
