import streamlit as st
from power_predict.app.app import add_bg_from_local
import base64

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

add_bg_from_local('power_predict/app/wind.jpg')

st.subheader("Data Sources:")
st.markdown("""
    Acknowledgement is given to the International Energy Agency (IEA) for use of their data
""")
