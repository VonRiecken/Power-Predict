from power_predict.logic.registry import load_model
from power_predict.params import PREDICTION_TARGETS

def load_target_model(target:str = None):
    if target not in PREDICTION_TARGETS:
        return 'Target not in scope'

    if target == 'Solar':
        model = load_model('knn_log')
    elif target == 'Hydro':
        model = load_model('knn_log')
    elif target == 'Wind':
        model = load_model('knn_log')
    elif target == 'Total':
        model = load_model('knn_log')
    else:
        model = load_model('knn_log')

    return model


def get_target_index(target: str) -> int:
    if target not in PREDICTION_TARGETS:
        return 'Target not in scope'

    if target == 'Hydro':
        return 0
    elif target == 'Solar':
        return 1
    elif target == 'Wind':
        return 2
    else:
        return 3
