import streamlit as st
import base64

st.set_page_config(
    page_title="Renewable Energy Production Prediction",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state='collapsed'
)

st.markdown(
    """
    <style>
        body {
            zoom: 130%;
        }
    </style>
    """,
    unsafe_allow_html=True
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
                document.body.style.zoom = '150%';
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

set_dark_mode_and_zoom()
add_bg_from_local('power_predict/app/earth.png')

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
