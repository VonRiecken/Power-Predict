import streamlit as st
import requests

from power_predict.params import COUNTRIES_LIST, PREDICTION_TARGETS, SERVICE_URL

st.title('Power Predict')

country_list = COUNTRIES_LIST
target_list = PREDICTION_TARGETS

# call parameters
# add units
target = st.selectbox('Energy source', target_list)
country = st.selectbox('Country', country_list)
cdd_18 = st.number_input('Cooling Degree Days above 18', format='%.4f')
cdd_21 = st.number_input('Cooling Degree Days above 21', format='%.4f')
irradiance = st.number_input('Global Horizontal Irrandiance', format='%.4f')
hdd_16 = st.number_input('Heating Degree Days below 16', format='%.4f')
hdd_18 = st.number_input('Heating Degree Days below 18', format='%.4f')
heat_index = st.number_input('Heat Index', format='%.4f')
humidity = st.number_input('Relative humidity', format='%.4f')
temp = st.number_input('Avergage temperature', format='%.4f')
precipitation = st.number_input('Total precipitaiton mm', format='%.4f')

params_ = {
    "target": target,
    "country": country,
    "cdd_18": cdd_18,
    "cdd_21": cdd_21,
    "irradiance": irradiance,
    "hdd_16": hdd_16,
    "hdd_18": hdd_18,
    "heat_index": heat_index,
    "humidity": humidity,
    "temp": temp,
    "precipitation": precipitation
    }

#  local
# api_url_ = 'http://127.0.0.1:8000/predict'
# cloud image

api_url_ = 'https://mvp-irosqzxbhq-ew.a.run.app/predict'

if st.button('Get Renewable Energy prediction'):
    res = requests.get(url=api_url_, params=params_)

    if res.status_code != 200:
        st.error('Error in API connection')
    else:
        prediction = round(res.json()['target_pred'], 2)


st.success(f"{country}'s {target} production will be {prediction} GWh")
