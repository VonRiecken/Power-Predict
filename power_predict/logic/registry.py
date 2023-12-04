import glob
import os
import time
import pickle

from power_predict.params import *
# from google.cloud import storage

# function to save the results of a model for evaluating performance
def save_performance(model: str, params: dict, metrics: dict) -> None:
    """
    Persist params & metrics locally on the hard drive at
    "{LOCAL_REGISTRY_PATH}/params/{current_timestamp}.pickle"
    "{LOCAL_REGISTRY_PATH}/metrics/{current_timestamp}.pickle"
    """

    model_name = model
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    if params is not None:
        params_path = os.path.join(LOCAL_PATH_PARAMS, 'models', 'model_results', model_name + '-params', timestamp + '.pickle')
        with open(params_path, 'wb') as file:
            pickle.dump(params, file)

    if metrics is not None:
        metrics_path = os.path.join(LOCAL_PATH_PARAMS, 'models', 'model_results', model_name + '-metrics', timestamp + '.pickle')
        with open(metrics_path, 'b') as file:
            pickle.dump(metrics, file)

    print("✅ Results saved locally")


def save_model(model, model_name: str) -> None:
    """
    Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='gcs', also persist it in your bucket on GCS at "models/{timestamp}.h5"
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save model locally
    model_path = os.path.join(LOCAL_PATH_PARAMS, 'models', 'saved_models', f"{model_name}-{timestamp}.h5")
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

    return None


def load_model(model_name: str):
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'
    Return None (but do not Raise) if no model is found

    """
    print(f"Load latest model from local registry.")

    # Get the latest model version name by the timestamp on disk
    local_model_directory = os.path.join(LOCAL_PATH_PARAMS, 'models', 'saved_models')
    local_model_paths = glob.glob(f"{local_model_directory}/{model_name}*")

    if not local_model_paths:
        print('No models found in the directory')
        return None

    most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

    print(f"Load latest model from disk...")

    with open(most_recent_model_path_on_disk, 'rb') as file:
        latest_model = pickle.load(file)

    print("✅ Model loaded from local disk")

    return latest_model
