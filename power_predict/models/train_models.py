# run/train/fit and save all models

import subprocess
import importlib
# from power_predict.models import random_forest, tpot, test_john
from power_predict.logic.registry import save_model

# Choose one of the below options (with scripts or with functions)

# Go through each model scipt listed to train and save model (save_model needs to be in script)
scripts_to_train = ['test_john.py']

for model in scripts_to_train:
    subprocess.run(['python', f'power_predict/models/{model}'])


# if models are in functions -> must all be defined with 'def train_model():'
# models_to_train_functions = ['test_john']

# for model in models_to_train_functions:
#     module = importlib.import_module(model)
#     train_model_function = getattr(module, "train_model", None)

#     if train_model_function is not None and callable(train_model_function):
#         trained_model = train_model_function()
#         save_model(trained_model, model)
#     else:
#         print(f"Module {model} does not have a callable 'train_model' function.")
