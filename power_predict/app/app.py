import streamlit as st
import requests

st.title('Power Predict')

target_list = ['Solar', 'Wind', 'Hydro', 'Total']
country_list = ['Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Colombia',
                  'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
                  'Greece', 'Hungary', 'Iceland', 'India', 'Ireland', 'Italy', 'Japan', 'Korea', 'Latvia', 'Lithuania',
                  'Luxembourg', 'Malta', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', "People's Republic of China",
                  'Poland', 'Portugal', 'Romania', 'Serbia', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
                  'United Kingdom', 'United States']

# call parameters
target = st.selectbox('Energy source', target_list)
country = st.selectbox('Country', country_list)
irradiance = st.number_input('Global Horizontal Irrandiance (W/m²)', format='%.0f')
humidity = st.slider('Relative humidity (%)', 0.0, 100.0, 50.0, 0.01)
temp = st.number_input('Avergage temperature (°C)', format='%.2f')
precipitation = st.number_input('Total precipitaiton (mm)', format='%.4f')

params_ = {
    "target": target,
    "country": country,
    "irradiance": irradiance,
    "humidity": humidity,
    "temp": temp,
    "precipitation": precipitation
    }

#  local
# api_url_ = 'http://127.0.0.1:8000/predict'

# cloud image
api_url_ = 'https://stage1-irosqzxbhq-ew.a.run.app/predict'
# 'https://mvp-irosqzxbhq-ew.a.run.app/predict'


if st.button('Get Renewable Energy Production'):
    res = requests.get(url=api_url_, params=params_)

    if res.status_code != 200:
        st.error('Error in API connection')
    else:
        prediction = round(res.json()['target_production'], 2)
        st.success(f"{country}'s {target} production will be {prediction} GWh")
