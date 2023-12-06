import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from power_predict.interface.main import load_target_model, get_target_index
from power_predict.logic.preprocessor import ordinal_mapping_string

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
    date: str,
    precipitation: float
):
    """
    Make prediciton for country renewable electricy production,  given certain weather conditions
    """
    ordinal_month = ordinal_mapping_string(date)

    data_X = {
    'Country': [country],
    'value_Temperature': [temp],
    'value_Relative_Humidty': [humidity],
    'value_Global_Horizontal_Irrandiance': [irradiance],
    'value_Total_Precipitation': [precipitation],
    'ordinal_month': [ordinal_month]
    }

    X_pred = pd.DataFrame(data_X, index=[0])

    model = load_target_model(target)
    y_array_spec_model = model.predict(X_pred)


    if target == 'Total':
        y_pred = np.expm1(y_array_spec_model[0])
        return dict(target_production=list(y_pred))
    else:
        y_pred = np.expm1(y_array_spec_model[0][get_target_index(target)])
        return dict(target_production=float(y_pred))


@app.get('/')
def root():
    return {'check': 'true'}
