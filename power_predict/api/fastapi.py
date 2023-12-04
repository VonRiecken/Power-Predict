import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from power_predict.logic.registry import load_model
from power_predict.logic.preprocessor import preprocess_features
from power_predict.interface.main import *


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
    heat_index: float,
    irradiance: float,
    precipitation: float
):
    """
    Make prediciton for country renewable electricy production,  given certain weather conditions
    """
# call unclean stuff from main

    df = pd.DataFrame(locals, index=[0])
    X_pred = df.drop(columns=['target'])
    X_pred_preprocessed = preprocess_features(X_pred)

    model = load_target_model(target)
    # y_pred_spec_model = app.state.model.predict(X_pred_preprocessed)

    # return dict(total_renewable=float(y_pred))
    return precipitation * temp

@app.get('/')
def root():
    return {'check': 'true'}
