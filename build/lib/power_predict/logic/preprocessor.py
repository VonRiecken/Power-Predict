import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder




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
