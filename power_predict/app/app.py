import streamlit as st
import requests

<<<<<<< Updated upstream
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
=======
# Function to set the background image
def add_bg_from_local(image_file, local=True):
    if local:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
    else:
        response = requests.get(image_file)
        encoded_string = base64.b64encode(response.content)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
        }}
        .reportview-container .main .block-container{{
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
            background-color: rgba(255, 255, 255, 0.6); /* White with 60% opacity */
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Page configuration
st.set_page_config(
    page_title="Renewable Energy Production Forecast",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state='expanded'
)

# Dropdown lists
target_list = ['--Select--', 'Solar', 'Wind', 'Hydro', 'Total']
country_list = ['Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Colombia',
                'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
                'Greece', 'Hungary', 'Iceland', 'India', 'Ireland', 'Italy', 'Japan', 'Korea', 'Latvia', 'Lithuania',
                'Luxembourg', 'Malta', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', "People's Republic of China",
                'Poland', 'Portugal', 'Romania', 'Serbia', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
                'United Kingdom', 'United States']

st.title('Renewable Power Prediction')
st.markdown('Estimate the renewable energy production potential for various energy sources and countries.')

target = st.selectbox('Energy source ⚡️', target_list)
country = st.selectbox('Country 🌍', country_list)
date = st.date_input('Select month and year of prediction 📅')
formatted_date = pd.to_datetime(date).strftime('%Y-%m')
temp = st.number_input('Average temperature 🌡️ (°C)', format='%.2f')
irradiance = st.number_input('Global Horizontal Irradiance 🌤️ (W/m²)', format='%.0f')
precipitation = st.number_input('Total precipitation ☔️ (mm)', format='%.4f')
humidity = st.slider('Relative humidity 💦 (%)', 0.0, 100.0, 50.0, 0.01)

# Dynamic background update logic
background_image = {
    '--Select--': 'power_predict/app/earth_spin.gif',
    'Solar': 'power_predict/app/solar.jpg',
    'Wind': 'power_predict/app/wind.jpg',
    'Hydro': 'power_predict/app/hydro.jpg',
    'Total': 'power_predict/app/total.jpg'
}

if target in background_image:
    add_bg_from_local(background_image[target])

# API URL
api_url_ = 'http://127.0.0.1:8000/predict'

# Button and API request logic
if st.button('Get Renewable Energy Production'):
    params_ = {
        "target": target,
        "country": country,
        "irradiance": irradiance,
        "humidity": humidity,
        "temp": temp,
        "precipitation": precipitation
    }
>>>>>>> Stashed changes
    res = requests.get(url=api_url_, params=params_)

    if res.status_code != 200:
        st.error('Error in API connection')
    else:
        prediction = round(res.json()['target_production'], 2)
        st.success(f"{country}'s {target} production will be {prediction} GWh")
