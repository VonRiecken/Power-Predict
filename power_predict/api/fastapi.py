import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from power_predict.logic.registry import load_model
from power_predict.logic.preprocessor import preprocess_features
from power_predict.interface.main import *
from power_predict.params import *

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

app = FastAPI()

# How do you add a CONTENT-TYPE = application/json header to the response provided by this endpoint? This will allow you to call .json() on the otherside.
# What library do you use to transform the response from this endpoint into JSON?

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
    precipitation: float,
    cdd_18: float,
    cdd_21: float,
    hdd_16: float,
    hdd_18: float,
    heat_index: float
):
    """
    Make prediciton for country renewable electricy production,  given certain weather conditions
    """
# call unclean stuff from main
    # exclude_var = target
    # filtered_locals = {key: value for key, value in locals().items() if key != exclude_var}

    data_X = {
    'Country': [country],
    'value_Temperature': [temp],
    'value_Relative_Humidty': [humidity],
    'value_Global_Horizontal_Irrandiance': [irradiance],
    'value_Total_Precipitation': [precipitation],
    'value_CDD_18': [cdd_18],
    'value_CDD_21': [cdd_21],
    'value_HDD_16': [hdd_16],
    'value_HDD_18': [hdd_18],
    'value_Heat_index': [heat_index]
    }

    X_pred = pd.DataFrame(data_X, index=[0])


    model = load_target_model(target)
    y_pred_spec_model = model.predict(X_pred)[0][get_target_index(target)]
    y_pred = np.expm1(y_pred_spec_model)

    return dict(target_production=float(y_pred))

    # return 100

@app.get('/')
def root():
    return {'check': 'true'}
