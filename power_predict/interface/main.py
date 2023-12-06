from power_predict.logic.registry import load_model
from power_predict.params import PREDICTION_TARGETS

def load_target_model(target:str = None):
    if target not in PREDICTION_TARGETS:
        return 'Target not in scope'

    if target == 'Solar':
        model = load_model(best_solar)
    elif target == 'Hydro':
        model = load_model(best_hydro)
    elif target == 'Wind':
        model = load_model(best_wind)
    else:
        model = load_model(best_total)

    return model

# Best Models
best_hydro = 'knn_4feats_log'
best_solar = 'knn_poly_4feats_time_log'
best_wind = 'knn_poly_4feats_time_log'
best_total = 'knn_poly_4feats_time_log'

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
