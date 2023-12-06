from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import os
from google.cloud import bigquery
from pathlib import Path
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from power_predict.logic.registry import *
from power_predict.logic.data import merging_all_datasets
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from power_predict.logic.registry import save_model, save_performance


def polynomial_regression(dataframe, target:str): ## best score = 0.8760212307541482

    # --- Data Preprocessing ---

    print(list(dataframe.columns))

    # Setting Country + Month year as Index
    dataframe['Country_Month'] = dataframe['Country'] + '_' + dataframe['Month_year'].astype(str)
    dataframe = dataframe.set_index('Country_Month')

    # Separating features and target variables (took out 'Unnamed: 0')
    X = dataframe.drop(['Month_year', 'Balance',
                'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar',
                'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind',
                'total_sol_wind_hyd', 'value_CDD_18', 'value_CDD_21',
                'value_HDD_16', 'value_HDD_18', 'value_Heat_index',], axis=1)

    # Applying logistic (log) transformation to the target variables
    if target == 'total_sol_wind_hyd':
        y = np.log1p(dataframe[['total_sol_wind_hyd']])
    elif target == 'Solar':
        y = np.log1p(dataframe[['Solar']])
    elif target == 'Wind':
        y = np.log1p(dataframe[['Wind']])
    elif target == 'Hydro':
        y = np.log1p(dataframe[['Hydro']])
    else:
        print('Target type not recognised!')

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


    ##columns_X = [col for (col in final.columns if 'value' in col)]or (col in final.columns if 'Country' in col)]
    columns_X = [col for col in dataframe.columns if 'value' in col or 'Country' in col or 'Month_year' in col]

    ##  We're selecting the columns named with 'value'
    X = dataframe[columns_X] # For the polynomial reg we use all our features, even the ones that are highly correlated

    # Drop the original Timestamp column if needed as well as the country
    X = X.drop(columns=['Month_year', 'Country'])

    # Assuming X, y are your full dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Model Training ---
    # Train the model
    preprocessing_pipeline.fit(X_train, y_train)

    ## ----- POLYNOMIAL REGRESSION ------- ##

    # We used the best polynomial degree found with a Gridsearch
    best_degree = 3

    # Fit the Polynomial Regression model with the best degree on the full training set
    poly_model_best = make_pipeline(PolynomialFeatures(degree=best_degree), LinearRegression())
    poly_model_best.fit(X_train, y_train)

    # Perform cross-validation and calculate the mean cross-validated R-squared score
    cross_val_cod = cross_val_score(poly_model_best, X, y, cv=5, scoring='r2').mean()

    # Make predictions on the test set
    y_pred_poly = poly_model_best.predict(X_test)

    # Calculate R-squared (Coefficient of Determination)
    cod_poly = r2_score(y_test, y_pred_poly)

    mae = mean_absolute_error(y_test, y_pred_poly)
    mse = mean_squared_error(y_test, y_pred_poly)

    print(f'Mean Absolute Error: {mae}')
    print(f'Mean Squared Error: {mse}')
    print(f'cross_val_cod: {cross_val_cod}')
    print(f'Coefficient of Determination (COD): {cod_poly}')

    return poly_model_best


save_model(polynomial_regression, 'polynomial-regression')

polynomial_regression(merging_all_datasets(), 'total_sol_wind_hyd')
