"""
app.py
------
A simple Streamlit dashboard for the motor speed model.
Someone can type in sensor readings and get a prediction instantly.

Run locally with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Motor Speed Predictor", page_icon="🌡️")


@st.cache_resource
def load_model():
    return joblib.load('model.joblib')


model = load_model()

st.title("🌡️ Motor Speed Predictor")
st.write("Enter the sensor readings below to predict motor speed.")

col1, col2 = st.columns(2)

with col1:
    ambient = st.number_input("Ambient temperature", value=20.0)
    coolant = st.number_input("Coolant temperature", value=20.0)
    u_d = st.number_input("Voltage d-component (u_d)", value=0.0)
    u_q = st.number_input("Voltage q-component (u_q)", value=0.0)
    torque = st.number_input("Torque", value=0.0)
    i_d = st.number_input("Current d-component (i_d)", value=0.0)

with col2:
    i_q = st.number_input("Current q-component (i_q)", value=0.0)
    pm = st.number_input("Permanent magnet temperature (pm)", value=20.0)
    stator_yoke = st.number_input("Stator yoke temperature", value=20.0)
    stator_tooth = st.number_input("Stator tooth temperature", value=20.0)
    stator_winding = st.number_input("Stator winding temperature", value=20.0)
    profile_id = st.number_input("Profile ID", value=0, step=1)

if st.button("Predict Motor Speed", type="primary"):
    input_df = pd.DataFrame([{
        'ambient': ambient,
        'coolant': coolant,
        'u_d': u_d,
        'u_q': u_q,
        'torque': torque,
        'i_d': i_d,
        'i_q': i_q,
        'pm': pm,
        'stator_yoke': stator_yoke,
        'stator_tooth': stator_tooth,
        'stator_winding': stator_winding,
        'profile_id': profile_id,
    }])

    prediction = model.predict(input_df)[0]
    st.success(f"Predicted Motor Speed: **{prediction:.4f}**")
