import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datarobot.models.dataset import Dataset

# Load the customer data
#df = pd.read_csv('customers_data.csv')

# Retrieve a dataset from AI Catalog using its ID
dataset_id = "66bb9a2dea25038602dbaa61" # change to your customer_data id!
dataset = Dataset.get(dataset_id)

# Load the dataset into an in-memory pandas dataframe
df = dataset.get_as_dataframe()

# Set the page layout to wide
st.set_page_config(layout="wide")

# Title of the app
st.title("Customer 360 Dashboard")

# Sidebar for customer selection
st.sidebar.header("Select a Customer")
customer_id = st.sidebar.selectbox(
    'Customer ID',
    df['CustomerID'].unique()
)

# Filter the data based on selected customer
customer_data = df[df['CustomerID'] == customer_id].squeeze()

# Customer Information Layout
st.subheader(f"Customer Information - {customer_id}")
col1, col2 = st.columns(2)

with col1:
    st.metric("Age", customer_data['Age'])
    st.metric("Location", customer_data['Location'])
    st.metric("Tenure (Years)", customer_data['Tenure'])

with col2:
    st.metric("Number of Products", customer_data['NumProducts'])
    st.metric("Cross-Sell Motor Score", f"{customer_data['CrossSell_Motor']:.2f}")
    st.metric("Cross-Sell Haushalt Score", f"{customer_data['CrossSell_Haushalt']:.2f}")
    st.metric("Storno Score", f"{customer_data['Storno']:.2f}")

# Plotting Section
st.subheader("Customer Scores Overview")
col3, col4 = st.columns(2)

# Plot 1: Cross-Sell Motor vs. Cross-Sell Haushalt
with col3:
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='CrossSell_Motor', y='CrossSell_Haushalt', hue='NumProducts', palette='coolwarm', s=100)
    plt.axvline(customer_data['CrossSell_Motor'], color='green', linestyle='--')
    plt.axhline(customer_data['CrossSell_Haushalt'], color='green', linestyle='--')
    plt.title('Cross-Sell Motor vs. Haushalt')
    plt.xlabel('Cross-Sell Motor')
    plt.ylabel('Cross-Sell Haushalt')
    st.pyplot(fig)

# Plot 2: Customer's Tenure vs. Number of Products
with col4:
    fig, ax = plt.subplots()
    sns.histplot(df['Tenure'], bins=10, kde=True, color='skyblue', ax=ax)
    plt.axvline(customer_data['Tenure'], color='red', linestyle='--')
    plt.title('Customer Tenure Distribution')
    plt.xlabel('Tenure (Years)')
    plt.ylabel('Frequency')
    st.pyplot(fig)

# Bottom Line Section
st.subheader("Bottom Line")
st.write(f"""
**Customer {customer_id}** is a {customer_data['Age']} year old customer from {customer_data['Location']}. 
They have been with us for {customer_data['Tenure']} years and currently hold {customer_data['NumProducts']} products. 
Based on their scores:
- **Cross-Sell Motor**: {customer_data['CrossSell_Motor']:.2f}
- **Cross-Sell Haushalt**: {customer_data['CrossSell_Haushalt']:.2f}
- **Storno**: {customer_data['Storno']:.2f}

**Actionable Insights:**
You might consider focusing on cross-selling motor products to this customer, given their score is slightly above average. 
Their tenure suggests they are a loyal customer, but the storno score indicates there may be a risk of churn that should be addressed.
""")
