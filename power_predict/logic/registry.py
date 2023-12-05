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
    "{LOCAL_PATH_PARAMS}/models/model_results/{model_name}-params-{timestamp}.pickle"
    "{LOCAL_PATH_PARAMS}/models/model_results/{model_name}-metrics-{timestamp}.pickle"
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    model_name = model

    # Save the Best Parameters with Timestamp
    if params is not None:
        params_path = os.path.join(LOCAL_PATH_PARAMS, 'models', 'model_results', f"{model_name}-params-{timestamp}.pickle")
        try:
            with open(params_path, 'wb') as file:
                pickle.dump(params, file)
        except Exception as e:
            print(f"Error saving parameters: {e}")
            return None

    # Save Performance Metrics with Timestamp
    if metrics is not None:
        metrics_path = os.path.join(LOCAL_PATH_PARAMS, 'models', 'model_results', f"{model_name}-metrics-{timestamp}.pickle")
        try:
            with open(metrics_path, 'wb') as file:
                pickle.dump(metrics, file)
        except Exception as e:
            print(f"Error saving metrics: {e}")
            return None

    print(f"✅ Results saved locally for {model_name}")


def save_model(model, model_name: str) -> None:
    """
    Persist trained model locally on the hard drive at
    "{LOCAL_PATH_PARAMS}/models/saved_models/{model_name}-{timestamp}.pkl"
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save model locally
    model_path = os.path.join(LOCAL_PATH_PARAMS, 'models', 'saved_models', f"{model_name}-{timestamp}.pkl")

    try:
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)
    except Exception as e:
        print(f"Error saving model: {e}")
        return None

    print(f"✅ Model saved locally at {model_path}")


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
