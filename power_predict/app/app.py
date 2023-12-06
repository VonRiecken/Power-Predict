import streamlit as st
import requests
import base64
import pandas as pd

st.set_page_config(
    page_title="Renewable Energy Production Prediction",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state='collapsed'
)

# Background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
    }}

    .st-emotion-cache-1wmy9hl {{
            flex-direction: column;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
        }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('power_predict/app/earth_spin.gif')

st.title("Welcome to our Renewable Energy Production Prediction")
st.subheader("About Us 👋")
st.markdown("""
    The Power Production Prediction project aims to contribute to sustainable energy practices by providing actionable insights into renewable energy production.
    Through data analysis, model development, and user-friendly interfaces, we seek to empower green initiatives and facilitate informed decision-making in the energy sector.
""")

st.subheader("Let's Get To It! 🌍")
st.markdown("""
    Based on historical weather data you can predict a country’s renewable energy production!
    Just click on the Prediction page, pick a country, enter the month, weather forecast and viola!
""")
