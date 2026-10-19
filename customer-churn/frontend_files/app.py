import os

import requests
import streamlit as st
import pandas as pd

st.title("Customer Churn Prediction")

# Docker Compose sets this to the backend service address; local runs default to localhost.
BACKEND_URL = st.sidebar.text_input(
    "Backend Server URL",
    value=os.getenv("BACKEND_URL", "http://127.0.0.1:5000"),
)

# Online Prediction
st.subheader("Online Prediction")

# Input fields for customer data
CustomerID = st.number_input("Customer ID", min_value=10000000, max_value=99999999)
CreditScore = st.number_input("Credit Score (customer's credit score)", min_value=300, max_value=900, value=650)
Geography = st.selectbox("Geography (country where the customer resides)", ["France", "Germany", "Spain"])
Age = st.number_input("Age (customer's age in years)", min_value=18, max_value=100, value=30)
Tenure = st.number_input("Tenure (number of years the customer has been with the bank)", value=12)
Balance = st.number_input("Account Balance (customer’s account balance)", min_value=0.0, value=10000.0)
NumOfProducts = st.number_input("Number of Products (number of products the customer has with the bank)", min_value=1, value=1)
HasCrCard = st.selectbox("Has Credit Card?", ["Yes", "No"])
IsActiveMember = st.selectbox("Is Active Member?", ["Yes", "No"])
EstimatedSalary = st.number_input("Estimated Salary (customer’s estimated salary)", min_value=0.0, value=50000.0)

customer_data = {
    'CreditScore': CreditScore,
    'Geography': Geography,
    'Age': Age,
    'Tenure': Tenure,
    'Balance': Balance,
    'NumOfProducts': NumOfProducts,
    'HasCrCard': 1 if HasCrCard == "Yes" else 0,
    'IsActiveMember': 1 if IsActiveMember == "Yes" else 0,
    'EstimatedSalary': EstimatedSalary
}

if st.button("Predict", type='primary'):
    endpoint = f"{BACKEND_URL.rstrip('/')}/v1/customer"
    try:
        response = requests.post(endpoint, json=customer_data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            churn_prediction = result["Prediction"]
            st.write(f"Based on the information provided, the customer with ID {CustomerID} is likely to {churn_prediction}.")
        else:
            st.error(f"Prediction failed (HTTP {response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection failed: {e}")

# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])
if file is not None:
    if st.button("Predict for Batch", type='primary'):
        endpoint = f"{BACKEND_URL.rstrip('/')}/v1/customerbatch"
        try:
            response = requests.post(endpoint, files={"file": file}, timeout=60)
            if response.status_code == 200:
                result = response.json()
                st.header("Batch Prediction Results")
                st.write(result)
            else:
                st.error(f"Batch prediction failed (HTTP {response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection failed: {e}")
