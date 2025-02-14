import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load trained AI model
model = joblib.load("phishing_detector.pkl")

# Rule-Based Function
def rule_based_prediction(features):
    score = 0  
    if features['Shortining_Service'] == 1:  
        score += 1  
    if features['having_At_Symbol'] == 1:
        score += 1  
    if features['age_of_domain'] == -1:
        score += 1  
    if features['SSLfinal_State'] == -1 and features['Google_Index'] == -1:
        score += 2  

    if score >= 4:  
        return -1  
    elif score >= 3:
        return 0  
    else:
        return 1  

# Hybrid Model Function
def hybrid_prediction(X_row):
    rule_based_result = rule_based_prediction(X_row)
    if rule_based_result == -1:
        return "⚠️ Phishing Website (-1)"
    
    X_df = pd.DataFrame([X_row], columns=X_test.columns)  
    ai_prediction = model.predict(X_df)[0]  
    
    return "✅ Legitimate Website (1)" if ai_prediction == 1 else "⚠️ Phishing Website (-1)"

# Streamlit UI
st.title("🔍 Phishing Website Detector")
st.write("Enter the URL features below to check if it's Phishing or Legitimate.")

# User inputs for key features
short_url = st.selectbox("Is the URL shortened?", [1, 0])
at_symbol = st.selectbox("Does the URL contain '@' symbol?", [1, 0])
domain_age = st.selectbox("Is the domain new (-1) or old (1)?", [-1, 1])
ssl_state = st.selectbox("Does the website have SSL (1) or not (-1)?", [-1, 1])
google_index = st.selectbox("Is the website indexed by Google? (1 for Yes, -1 for No)", [-1, 1])

# Make prediction
if st.button("Check Website"):
    user_input = {
        "Shortining_Service": short_url,
        "having_At_Symbol": at_symbol,
        "age_of_domain": domain_age,
        "SSLfinal_State": ssl_state,
        "Google_Index": google_index
    }
    prediction = hybrid_prediction(user_input)
    st.subheader(f"Prediction: {prediction}")
