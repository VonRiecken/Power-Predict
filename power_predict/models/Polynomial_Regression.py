from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from google.cloud import bigquery
import pandas_gbq
from pathlib import Path
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score




def polynomial_regression(dataframe):

    ##columns_X = [col for (col in final.columns if 'value' in col)]or (col in final.columns if 'Country' in col)]
    columns_X = [col for col in dataframe.columns if 'value' in col or 'Country' in col or 'Month_year' in col]

    ##  We're selecting the columns named with 'value'
    X = dataframe[columns_X] # For the Lasso we use all our features, even the ones that are highly correlated

    # Drop the original Timestamp column if needed
    X = X.drop(columns=['Month_year', 'Country'])
    y = dataframe['total target (wind, solar, hydro)']

    # Assuming X, y are your full dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define a range of values for polynomial degree and number of folds
    degree_values = [1, 2, 3, 4, 5]

    # Create a parameter grid for GridSearchCV
    param_grid = {'polynomialfeatures__degree': degree_values}

    # Create a Polynomial Regression model using a pipeline
    poly_model = make_pipeline(PolynomialFeatures(), LinearRegression())

    # Use GridSearchCV to find the best polynomial degree
    grid_search = GridSearchCV(poly_model, param_grid, scoring='neg_mean_squared_error', cv=5)
    grid_search.fit(X_train, y_train)

    # Get the best polynomial degree
    best_degree = grid_search.best_params_['polynomialfeatures__degree']
    print(f'✅ The best polynomial degree is: {best_degree}')

    # Fit the Polynomial Regression model with the best degree on the full training set
    poly_model_best = make_pipeline(PolynomialFeatures(degree=best_degree), LinearRegression())
    poly_model_best.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred_poly = poly_model_best.predict(X_test)

    # Calculate R-squared (Coefficient of Determination)
    cod_poly = r2_score(y_test, y_pred_poly)
    print(f'✅ Coefficient of Determination (COD) for Polynomial Regression: {cod_poly}')
    print(f'✅ Mean Squared Error on Validation Set: {grid_search.best_score_}')  # Negative of Mean Squared Error
