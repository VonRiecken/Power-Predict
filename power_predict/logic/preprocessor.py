import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from power_predict.logic.data import load_local_df


def targets_and_features(X: pd.DataFrame) -> pd.DataFrame:
    to_drop = ['Unnamed: 0', 'Month_year','Balance', 'Combustible_Renewables',
               'Other_Renewables', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_']

    X_useful = X.drop(columns=to_drop)

    return X_useful


# Functions or Classes
def prepare_target(X:pd.DataFrame, target:str, five_features=False) -> pd.DataFrame and pd.DataFrame:
    target_cols = X['Hydro', 'Solar', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind']

    X_ready = X.drop(columns=['Month_year', 'Balance', 'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar', 'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind'])
    # if five_features == True:
    #     X_ready.drop(columns=)

    return X_ready

def log_transform_target():
    df = load_local_df()

    #####logic for log transformation here
    df['Country_Month'] = df['Country'] + '_' + df['Month_year'].astype(str)
    df = df.set_index('Country_Month')

    # Separating features and target variables
    X = df.drop(['Unnamed: 0', 'Month_year', 'Balance',
             'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar',
             'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind',
             'total_sol_wind_hyd'], axis=1)

    # Applying logistic (log) transformation to the target variables
    y_log_transformed = log_transform_target(df)

    y = np.log1p(df[['Hydro', 'Solar', 'Wind', 'total_sol_wind_hyd']])

    return y #update to return the log transformed target



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
