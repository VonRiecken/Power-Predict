import streamlit as st
import base64

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

st.subheader("Data Sources:")
st.markdown("""
    Acknowledgement is given to the International Energy Agency (IEA) for use of their data
""")
