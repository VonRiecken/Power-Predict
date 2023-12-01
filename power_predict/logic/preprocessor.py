import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

def prepare_target(X:pd.DataFrame, target:str, five_features=False) -> pd.DataFrame + pd.DataFrame:
    target_cols = X.columns != ['Hydro', 'Solar', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind']

    X_ready = X.drop(columns=['Month_year', 'Balance', 'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind'])
    # if five_features == True:
    #     X_ready.drop(columns=)

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
