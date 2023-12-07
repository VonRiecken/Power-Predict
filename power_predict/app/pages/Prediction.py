import streamlit as st
import pandas as pd
import requests
import base64

st.set_page_config(
    page_title="Renewable Energy Production Prediction",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state='collapsed'
)
def set_dark_mode_and_zoom():
    dark_mode_and_zoom_script = """
        <script>
            const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            const body = document.body;

            function setDarkModePreference() {
                if (darkModeMediaQuery.matches) {
                    body.classList.add('dark-mode');
                } else {
                    body.classList.remove('dark-mode');
                }
            }

            function setZoomLevel() {
                document.body.style.zoom = '200%';
            }

            setDarkModePreference(); // Set initial dark mode preference
            setZoomLevel(); // Set initial zoom level

            // Listen for changes in the system dark mode preference
            darkModeMediaQuery.addEventListener('change', setDarkModePreference);
        </script>
    """
    st.markdown(dark_mode_and_zoom_script, unsafe_allow_html=True)

# Background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

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

def add_bg_as_earth(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: conatin;
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


target_list = ['--Select--','Solar', 'Wind', 'Hydro', 'Total']
country_list = ['Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Colombia',
                'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
                'Greece', 'Hungary', 'Iceland', 'India', 'Ireland', 'Italy', 'Japan', 'Korea', 'Latvia', 'Lithuania',
                'Luxembourg', 'Malta', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', "People's Republic of China",
                'Poland', 'Portugal', 'Romania', 'Serbia', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
                'United Kingdom', 'United States']

st.title('Renewable Power Prediction')
st.markdown('Estimate the renewable energy production potential for various energy sources and countries.')

set_dark_mode_and_zoom()
add_bg_as_earth('power_predict/app/earth.png')

# call parameters
target = st.selectbox('Energy source ⚡️', target_list)
country = st.selectbox('Country 🌍', country_list)
date = st.date_input('Select month and year of prediction 📅 (any day in the month)')
# formatted_date = pd.to_datetime(date).strftime('%Y-%m')
formatted_date = date.strftime('%Y-%m')
temp = st.number_input('Avergage temperature 🌡️ (°C)', format='%.2f')
irradiance = st.number_input('Global Horizontal Irrandiance 🌤️ (W/m²)', format='%.0f')
precipitation = st.number_input('Total precipitaiton ☔️ (mm)', format='%.4f')
humidity = st.slider('Relative humidity 💦 (%)', 0, 100, 50, 1)

# Set background
if target == '--Select--':
    add_bg_as_earth('power_predict/app/earth.png')
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
# api_url_ = 'https://prod-irosqzxbhq-ew.a.run.app/predict'
# 'https://mvp-irosqzxbhq-ew.a.run.app/predict'


if st.button('Get Renewable Energy Production'):
    params_ = {
        "target": target,
        "country": country,
        "irradiance": irradiance,
        "humidity": humidity,
        "temp": temp,
        "precipitation": precipitation,
        "date": formatted_date
    }
    res = requests.get(url=api_url_, params=params_)

    if res.status_code != 200:
        st.error('Please select target')
    elif target == 'Total':
        prediction = res.json()['target_production']
        st.success(f"🌍 {country}'s Solar production will be {round(prediction[1], 2)} GWh ☀️")
        st.success(f"🌍 {country}'s Wind production will be {round(prediction[2], 2)} GWh 🌀")
        st.success(f"🌍 {country}'s Hydro production will be {round(prediction[0], 2)} GWh 💧")
        st.success(f"🌍 {country}'s Total production will be {round(prediction[3], 2)} GWh ⚡️")
    else:
        prediction = round(res.json()['target_production'], 2)
        st.success(f"🌍 {country}'s {target} production will be {prediction} GWh ⚡️")
