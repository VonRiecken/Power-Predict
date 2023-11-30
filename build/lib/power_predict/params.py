import os
import numpy as np

##################  VARIABLES  ##################
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
INSTANCE = os.environ.get("INSTANCE")

GAR_IMAGE = os.environ.get("GAR_IMAGE")
GAR_MEMORY = os.environ.get("GAR_MEMORY")

##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "final_project", "data")
LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "final_project", "training_outputs")

COLUMN_NAMES_RAW = ['Month_year','Country','Balance','Combustible Renewables','Hydro','Other Renewables','Solar',
                    'Total Renewables (Hydro, Geo, Solar, Wind, Other)', 'Wind','value_CDD_18','value_CDD_21',
                    'value_Global_Horizontal_Irrandiance','value_HDD_16','value_HDD_18','value_Heat_index',
                    'value_Relative_Humidty','value_Temperature','value_Total_Precipitation','total target (wind, solar, hydro)']

DTYPES_RAW = {
    "Month_year": "datetime64[ns, UTC]",
    "Country": "object",
    "Balance": "object",
    "Combustible Renewables": "float32",
    "Hydro": "float32",
    "Other Renewables": "float32",
    "Solar": "float32",
    "Toal Renewables (Hydro, Geo, Solar, Wind, Other)": "float32",
    "Wind": "float32",
    "value_CDD_18": "float32",
    "value_CDD_21": "float32",
    "value_Global_Horizontal_Irrandiance": "float32",
    "value_HDD_16": "float32",
    "value_HDD_18": "float32",
    "value_Heat_index": "float32",
    "value_Relative_Humidty": "float32",
    "value_Temperature": "float32",
    "value_Total_Precipitation": "float32",
    "total target (wind, solar, hydro)": "float32"
}

DTYPES_PROCESSED = np.float32



################## VALIDATIONS #################

env_valid_options = dict(
    MODEL_TARGET=["local", "gcs", "mlflow"],
)

def validate_env_value(env, valid_options):
    env_value = os.environ[env]
    if env_value not in valid_options:
        raise NameError(f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}")


for env, valid_options in env_valid_options.items():
    validate_env_value(env, valid_options)
