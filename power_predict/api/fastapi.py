import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from power_predict.interface.main import load_target_model, get_target_index
# from power_predict.logic.preprocessor import ordinal_month

app = FastAPI()

# Allowing middleware as it's good practice (from the taxifare template)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/predict')
def predict(
    country: str,
    target: str,
    temp: float,
    humidity: float,
    irradiance: float,
    # date: pd.Timestamp,
    precipitation: float
):
    """
    Make prediciton for country renewable electricy production,  given certain weather conditions
    """
    # ordinal_month = ordinal_month(date)

    data_X = {
    'Country': [country],
    'value_Temperature': [temp],
    'value_Relative_Humidty': [humidity],
    'value_Global_Horizontal_Irrandiance': [irradiance],
    'value_Total_Precipitation': [precipitation],
    #'ordinal_month': [ordinal_month]
    }

    X_pred = pd.DataFrame(data_X, index=[0])

    model = load_target_model(target)
    y_pred_spec_model = model.predict(X_pred)[0][get_target_index(target)]

    if target == 'Solar':
        y_pred = y_pred_spec_model
    else:
        y_pred = np.expm1(y_pred_spec_model)

    return dict(target_production=float(y_pred))


@app.get('/')
def root():
    return {'check': 'true'}
