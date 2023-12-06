import pandas as pd
from pandas import Period
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


# Ordinal Mapping function

ordinal_map = {
 Period('2010-01', 'M'): 1, Period('2010-02', 'M'): 2, Period('2010-03', 'M'): 3, Period('2010-04', 'M'): 4, Period('2010-05', 'M'): 5,
 Period('2010-06', 'M'): 6, Period('2010-07', 'M'): 7, Period('2010-08', 'M'): 8, Period('2010-09', 'M'): 9, Period('2010-10', 'M'): 10,
 Period('2010-11', 'M'): 11, Period('2010-12', 'M'): 12, Period('2011-01', 'M'): 13, Period('2011-02', 'M'): 14, Period('2011-03', 'M'): 15,
 Period('2011-04', 'M'): 16, Period('2011-05', 'M'): 17, Period('2011-06', 'M'): 18, Period('2011-07', 'M'): 19, Period('2011-08', 'M'): 20,
 Period('2011-09', 'M'): 21, Period('2011-10', 'M'): 22, Period('2011-11', 'M'): 23, Period('2011-12', 'M'): 24, Period('2012-01', 'M'): 25,
 Period('2012-02', 'M'): 26, Period('2012-03', 'M'): 27, Period('2012-04', 'M'): 28, Period('2012-05', 'M'): 29, Period('2012-06', 'M'): 30,
 Period('2012-07', 'M'): 31, Period('2012-08', 'M'): 32, Period('2012-09', 'M'): 33, Period('2012-10', 'M'): 34, Period('2012-11', 'M'): 35,
 Period('2012-12', 'M'): 36, Period('2013-01', 'M'): 37, Period('2013-02', 'M'): 38, Period('2013-03', 'M'): 39, Period('2013-04', 'M'): 40,
 Period('2013-05', 'M'): 41, Period('2013-06', 'M'): 42, Period('2013-07', 'M'): 43, Period('2013-08', 'M'): 44, Period('2013-09', 'M'): 45,
 Period('2013-10', 'M'): 46, Period('2013-11', 'M'): 47, Period('2013-12', 'M'): 48, Period('2014-01', 'M'): 49, Period('2014-02', 'M'): 50,
 Period('2014-03', 'M'): 51, Period('2014-04', 'M'): 52, Period('2014-05', 'M'): 53, Period('2014-06', 'M'): 54, Period('2014-07', 'M'): 55,
 Period('2014-08', 'M'): 56, Period('2014-09', 'M'): 57, Period('2014-10', 'M'): 58, Period('2014-11', 'M'): 59,
 Period('2014-12', 'M'): 60, Period('2015-01', 'M'): 61, Period('2015-02', 'M'): 62, Period('2015-03', 'M'): 63, Period('2015-04', 'M'): 64,
 Period('2015-05', 'M'): 65, Period('2015-06', 'M'): 66, Period('2015-07', 'M'): 67, Period('2015-08', 'M'): 68, Period('2015-09', 'M'): 69,
 Period('2015-10', 'M'): 70, Period('2015-11', 'M'): 71, Period('2015-12', 'M'): 72, Period('2016-01', 'M'): 73, Period('2016-02', 'M'): 74,
 Period('2016-03', 'M'): 75, Period('2016-04', 'M'): 76, Period('2016-05', 'M'): 77, Period('2016-06', 'M'): 78, Period('2016-07', 'M'): 79,
 Period('2016-08', 'M'): 80, Period('2016-09', 'M'): 81, Period('2016-10', 'M'): 82, Period('2016-11', 'M'): 83, Period('2016-12', 'M'): 84,
 Period('2017-01', 'M'): 85, Period('2017-02', 'M'): 86, Period('2017-03', 'M'): 87, Period('2017-04', 'M'): 88, Period('2017-05', 'M'): 89,
 Period('2017-06', 'M'): 90, Period('2017-07', 'M'): 91, Period('2017-08', 'M'): 92, Period('2017-09', 'M'): 93,
 Period('2017-10', 'M'): 94, Period('2017-11', 'M'): 95, Period('2017-12', 'M'): 96, Period('2018-01', 'M'): 97, Period('2018-02', 'M'): 98,
 Period('2018-03', 'M'): 99, Period('2018-04', 'M'): 100, Period('2018-05', 'M'): 101, Period('2018-06', 'M'): 102, Period('2018-07', 'M'): 103,
 Period('2018-08', 'M'): 104, Period('2018-09', 'M'): 105, Period('2018-10', 'M'): 106, Period('2018-11', 'M'): 107, Period('2018-12', 'M'): 108,
 Period('2019-01', 'M'): 109, Period('2019-02', 'M'): 110, Period('2019-03', 'M'): 111, Period('2019-04', 'M'): 112, Period('2019-05', 'M'): 113,
 Period('2019-06', 'M'): 114, Period('2019-07', 'M'): 115, Period('2019-08', 'M'): 116, Period('2019-09', 'M'): 117, Period('2019-10', 'M'): 118,
 Period('2019-11', 'M'): 119, Period('2019-12', 'M'): 120, Period('2020-01', 'M'): 121, Period('2020-02', 'M'): 122, Period('2020-03', 'M'): 123,
 Period('2020-04', 'M'): 124, Period('2020-05', 'M'): 125, Period('2020-06', 'M'): 126, Period('2020-07', 'M'): 127, Period('2020-08', 'M'): 128,
 Period('2020-09', 'M'): 129, Period('2020-10', 'M'): 130, Period('2020-11', 'M'): 131, Period('2020-12', 'M'): 132, Period('2021-01', 'M'): 133,
 Period('2021-02', 'M'): 134, Period('2021-03', 'M'): 135, Period('2021-04', 'M'): 136, Period('2021-05', 'M'): 137, Period('2021-06', 'M'): 138,
 Period('2021-07', 'M'): 139, Period('2021-08', 'M'): 140, Period('2021-09', 'M'): 141, Period('2021-10', 'M'): 142, Period('2021-11', 'M'): 143,
 Period('2021-12', 'M'): 144, Period('2022-01', 'M'): 145, Period('2022-02', 'M'): 146, Period('2022-03', 'M'): 147, Period('2022-04', 'M'): 148,
 Period('2022-05', 'M'): 149, Period('2022-06', 'M'): 150, Period('2022-07', 'M'): 151, Period('2022-08', 'M'): 152, Period('2022-09', 'M'): 153,
 Period('2022-10', 'M'): 154, Period('2022-11', 'M'): 155, Period('2022-12', 'M'): 156, Period('2023-01', 'M'): 157, Period('2023-02', 'M'): 158,
 Period('2023-03', 'M'): 159, Period('2023-04', 'M'): 160, Period('2023-05', 'M'): 161, Period('2023-06', 'M'): 162, Period('2023-07', 'M'): 163,
 Period('2023-08', 'M'): 164, Period('2023-09', 'M'): 165, Period('2023-10', 'M'): 166, Period('2023-11', 'M'): 167, Period('2023-12', 'M'): 168,
 Period('2024-01', 'M'): 169, Period('2024-02', 'M'): 170, Period('2024-03', 'M'): 171, Period('2024-04', 'M'): 172, Period('2024-05', 'M'): 173,
 Period('2024-06', 'M'): 174, Period('2024-07', 'M'): 175, Period('2024-08', 'M'): 176, Period('2024-09', 'M'): 177, Period('2024-10', 'M'): 178,
 Period('2024-11', 'M'): 179, Period('2024-12', 'M'): 180, Period('2025-01', 'M'): 181, Period('2025-02', 'M'): 182, Period('2025-03', 'M'): 183,
 Period('2025-04', 'M'): 184, Period('2025-05', 'M'): 185, Period('2025-06', 'M'): 186, Period('2025-07', 'M'): 187, Period('2025-08', 'M'): 188,
 Period('2025-09', 'M'): 189, Period('2025-10', 'M'): 190, Period('2025-11', 'M'): 191, Period('2025-12', 'M'): 192, Period('2026-01', 'M'): 193,
 Period('2026-02', 'M'): 194, Period('2026-03', 'M'): 195, Period('2026-04', 'M'): 196, Period('2026-05', 'M'): 197, Period('2026-06', 'M'): 198,
 Period('2026-07', 'M'): 199, Period('2026-08', 'M'): 200, Period('2026-09', 'M'): 201, Period('2026-10', 'M'): 202, Period('2026-11', 'M'): 203,
 Period('2026-12', 'M'): 204, Period('2027-01', 'M'): 205, Period('2027-02', 'M'): 206, Period('2027-03', 'M'): 207, Period('2027-04', 'M'): 208,
 Period('2027-05', 'M'): 209, Period('2027-06', 'M'): 210, Period('2027-07', 'M'): 211, Period('2027-08', 'M'): 212, Period('2027-09', 'M'): 213,
 Period('2027-10', 'M'): 214, Period('2027-11', 'M'): 215, Period('2027-12', 'M'): 216, Period('2028-01', 'M'): 217, Period('2028-02', 'M'): 218,
 Period('2028-03', 'M'): 219, Period('2028-04', 'M'): 220, Period('2028-05', 'M'): 221, Period('2028-06', 'M'): 222, Period('2028-07', 'M'): 223,
 Period('2028-08', 'M'): 224, Period('2028-09', 'M'): 225, Period('2028-10', 'M'): 226, Period('2028-11', 'M'): 227, Period('2028-12', 'M'): 228,
 Period('2029-01', 'M'): 229, Period('2029-02', 'M'): 230, Period('2029-03', 'M'): 231, Period('2029-04', 'M'): 232, Period('2029-05', 'M'): 233,
 Period('2029-06', 'M'): 234, Period('2029-07', 'M'): 235, Period('2029-08', 'M'): 236, Period('2029-09', 'M'): 237, Period('2029-10', 'M'): 238,
 Period('2029-11', 'M'): 239, Period('2029-12', 'M'): 240}

def ordinal_mapping(date):
    # Convert date to Period object in 'M' frequency
    period_date = pd.Period(date, freq='M')

    # Return the ordinal value if the date is in the map, else return None
    return ordinal_map.get(period_date)

# df['ordinal_month'] = df['Month_year'].apply(ordinal_mapping)
