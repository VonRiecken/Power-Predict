import streamlit as st
import requests
import base64
import pandas as pd

target_list = ['--Select--','Solar', 'Wind', 'Hydro', 'Total']
country_list = ['Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Colombia',
                'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
                'Greece', 'Hungary', 'Iceland', 'India', 'Ireland', 'Italy', 'Japan', 'Korea', 'Latvia', 'Lithuania',
                'Luxembourg', 'Malta', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', "People's Republic of China",
                'Poland', 'Portugal', 'Romania', 'Serbia', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
                'United Kingdom', 'United States']

st.set_page_config(
    page_title="Renewable Energy Production Forecast",
    page_icon="🍃",
    layout="centered",
    initial_sidebar_state='expanded'
)

# Background image
def add_bg_from_local(image_file, local=True):
    if local == True:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
    elif local == False:
        response = requests.get(image_file)

        encoded_string = base64.b64encode(response.content)

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
    </style>
    """,
    unsafe_allow_html=True
    )


add_bg_from_local('power_predict/app/earth_spin.gif')

# App title and subtitle
st.title('Renewable Power Prediction')
st.markdown('Estimate the renewable energy production potential for various energy sources and countries.')

# call parameters
target = st.selectbox('Energy source ⚡️', target_list)
country = st.selectbox('Country 🌍', country_list)
date = st.date_input('Select month and year of prediction 📅')
formatted_date = pd.to_datetime(date).strftime('%Y-%m')
temp = st.number_input('Avergage temperature 🌡️ (°C)', format='%.2f')
irradiance = st.number_input('Global Horizontal Irrandiance 🌤️ (W/m²)', format='%.0f')
precipitation = st.number_input('Total precipitaiton ☔️ (mm)', format='%.4f')
humidity = st.slider('Relative humidity 💦 (%)', 0.0, 100.0, 50.0, 0.01)

# Set background
if target == '--Select--':
    add_bg_from_local('power_predict/app/solar.jpg')
    # add_bg_from_local('power_predict/app/earth_spin.gif')
elif target == 'Solar':
    add_bg_from_local('power_predict/app/solar.jpg')
elif target == 'Wind':
    add_bg_from_local('power_predict/app/wind.jpg')
elif target == 'Hydro':
    add_bg_from_local('power_predict/app/hydro.jpg')
elif target == 'Total':
    add_bg_from_local('power_predict/app/total.jpg')

#  local
api_url_ = 'http://127.0.0.1:8000/predict'

# cloud image
# api_url_ = 'https://stage1-irosqzxbhq-ew.a.run.app/predict'
# 'https://mvp-irosqzxbhq-ew.a.run.app/predict'


if st.button('Get Renewable Energy Production'):
    params_ = {
        "target": target,
        "country": country,
        "irradiance": irradiance,
        "humidity": humidity,
        "temp": temp,
        "precipitation": precipitation,
        # "date": date
    }
    res = requests.get(url=api_url_, params=params_)

    if res.status_code != 200:
        st.error('Please select target')
    else:
        prediction = round(res.json()['target_production'], 2)
        st.success(f"{country}'s {target} production will be {prediction} GWh")
