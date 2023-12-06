import streamlit as st
import pandas as pd
import requests

from power_predict.app.app import add_bg_from_local, target_list,  country_list

add_bg_from_local('power_predict/app/earth_spin.gif')

# App title and subtitle
st.title('Renewable Power Prediction')
# st.markdown('Estimate the renewable energy production potential for various energy sources and countries.')

if st.button('Go back to Landing'):
    st.experimental_set_query_params(page='landing')
#     st.experimental_rerun()

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
    add_bg_from_local('power_predict/app/earth_spin.gif')
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
