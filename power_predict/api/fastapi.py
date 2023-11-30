import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from power_predict.logic.registry import load_model
# from power_predict.logic.preprocessor import preprocess_features


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
    cdd18: float,
    cdd21: float,
    hdd16: float,
    hdd18: float,
    temp: float,
    humidity: float,
    heat_index: float,
    irradiance: float,
    precipitation: float
):
    """
    Make prediciton for country renewable electricy production,  given certain weather conditions
    """

    df = pd.DataFrame(locals, index=[0])
    X_pred = df.drop(columns=['target'])

    X_pred_preprocessed = preprocess_features(X_pred)

    app.state.model = load_model()
    y_pred = app.state.model.predict(X_pred_preprocessed)

    return dict(total_renewable=float(y_pred))

@app.get('/')
def root():
    return {'check': 'true'}
