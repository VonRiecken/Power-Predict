import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder


def targets_and_features(X: pd.DataFrame) -> pd.DataFrame:
    to_drop = ['Unnamed: 0', 'Month_year','Balance', 'Combustible_Renewables',
               'Other_Renewables', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_']

    X_useful = X.drop(columns=to_drop)

    return X_useful


# def prepare_target(X:pd.DataFrame, target:str, five_features=False) -> pd.DataFrame and pd.DataFrame:
#     target_cols = X['Hydro', 'Solar', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind']

#     X_ready = X.drop(columns=['Month_year', 'Balance', 'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind'])
#     # if five_features == True:
#     #     X_ready.drop(columns=)

def log_transform_target():
    return None

def preprocess_features(X: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess features
    """
    if 'Country' not in X.columns:
        print('No Country column found')
        return None

    encoder = OneHotEncoder(sparse=False)
    df = pd.DataFrame(encoder.fit_transform(X[['Country']]), columns=encoder.get_feature_names_out(['Country']))

    return df
