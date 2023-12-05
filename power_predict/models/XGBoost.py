import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
from power_predict.logic.data import load_local_df
#from sklearn.externals import joblib


# --- Fetching Data ---
df = df = load_local_df()
#df = pd.read_csv('/Users/bryan/code/VonRiecken/Power-Predict/power_predict/data/merged_dataset2023-12-01 18:08:35.062618.csv')

df.head(5)

# --- Data Preprocessing ---
# Setting Country + Month year as Index
df['Country_Month'] = df['Country'] + '_' + df['Month_year'].astype(str)
df = df.set_index('Country_Month')
# Separating features and target variables
X = df.drop(['Unnamed: 0', 'Month_year', 'Balance',
             'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar',
             'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind',
             'total_sol_wind_hyd', 'value_CDD_18', 'value_CDD_21',
             'value_HDD_16', 'value_HDD_18', 'value_Heat_index',], axis=1)
# Applying logistic (log) transformation to the target variables
y = np.log1p(df[['Hydro', 'Solar', 'Wind', 'total_sol_wind_hyd']])
# Init list of numerical columns
num_features = X.select_dtypes(include=[np.number]).columns.tolist()
# Preprocessing pipeline
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('scaler', MinMaxScaler())
        ]), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Country'])
    ])
# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# --- Create Model ----
def run_xgboost_model():
    df = load_local_df()

    # Preprocessing
    final = df
    columns_X = [col for col in final.columns if 'value' in col]

    if not columns_X:
        raise ValueError("No columns with 'value' in their names.")

    X = final[columns_X]
    columns_to_drop = ['value_CDD_18',
                       'value_CDD_21',
                       'value_HDD_16',
                       'value_HDD_18',
                       'value_Heat_index'
                       ]
    X = X.drop(columns=columns_to_drop)

    # Feature scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Here you can choose which technology output to predict
    y = final['total_sol_wind_hyd']
    #y = final['Solar']
    #y = final['Wind']
    #y = final['Hydro']

    # Split training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # XGBoost model
    model = XGBRegressor()

    # Cross-validation
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='neg_mean_squared_error')
    mse_cv_mean = -cv_scores.mean()

    print(f'Mean Cross-validated Mean Squared Error: {mse_cv_mean}')

    # Fit the model on the training set
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    cod = r2_score(y_test, y_pred)

    print(f'Mean Absolute Error: {mae}')
    print(f'Mean Squared Error: {mse}')
    print(f'Coefficient of Determination (COD): {cod}')
    print(f'R-squared: {r2}')

    return model

run_xgboost_model()
