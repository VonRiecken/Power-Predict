from power_predict.logic.registry import load_model
from power_predict.params import PREDICTION_TARGETS

def load_target_model(target:str = None):
    if target not in PREDICTION_TARGETS:
        return 'Target not in scope'

    if target == 'Solar':
        model = load_model('test_john')
    elif target == 'Hydro':
        model = load_model('best_hydro_model')
    elif target == 'Wind':
        model = load_model('best_wind_model')
    else:
        model = load_model('best_total_model')

    return model

# Best Models
best_hydro = 'knn_4feats_log'
best_solar = 'knn_4feats'
best_wind = 'knn_poly_4feats_log'
best_total = 'knn_poly_4feats_log'
