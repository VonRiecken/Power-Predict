import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from power_predict.logic.registry import save_model, save_performance
from power_predict.logic.data import load_local_df
from power_predict.logic.preprocessor import ordinal_mapping, custom_scaler

# --- Fetching Data ---
df = load_local_df()

# --- Data Preprocessing ---

# Adding Ordinal Month Column
df['ordinal_month'] = df['Month_year'].apply(ordinal_mapping)

# Setting Country + Month year as Index
df['Country_Month'] = df['Country'] + '_' + df['Month_year'].astype(str)
df = df.set_index('Country_Month')

# Separating features and target variables
X = df.drop(['Unnamed: 0', 'Month_year', 'Balance',
             'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar',
             'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind',
             'total_sol_wind_hyd', 'value_CDD_18', 'value_CDD_21',
             'value_HDD_16', 'value_HDD_18', 'value_Heat_index',], axis=1)

# Applying logistic transformation to target variables
y = np.log1p(df[['Hydro', 'Solar', 'Wind', 'total_sol_wind_hyd']])

# Defining Scalers

    # Init list of numerical columns, excluding 'ordinal_months'
num_features = [col for col in X.select_dtypes(include=[np.number]).columns if col != 'ordinal_months']

    # Custom scaler function for 'ordinal_months'
# def custom_scaler(om):
#     om_scaled = (om - 1) / (240 - 1)  # scale from 0 to 1 with max value 240
#     return om_scaled

    # Create a transformer for the custom scaling
custom_scaler_transformer = FunctionTransformer(np.vectorize(custom_scaler), validate=False)

# Preprocessing pipeline
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[('scaler', MinMaxScaler())]), num_features),
        ('ordinal_month', Pipeline(steps=[('custom_scaler', custom_scaler_transformer)]), ['ordinal_month']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Country'])
    ])

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# --- Create Model Training ---

# KNeighborsRegressor with Polynomial Features wrapped in MultiOutputRegressor
polynomial_features = PolynomialFeatures(degree=2)
multi_knn_regressor = MultiOutputRegressor(KNeighborsRegressor(n_neighbors=20, p=2, weights='uniform'))

# Pipeline including preprocessing, polynomial feature generation, and multi-output Polynomial Regression
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessing_pipeline),
    ('poly_features', polynomial_features),
    ('multi_knn_regressor', multi_knn_regressor)
])


# --- Model Training ---
# Train the model
pipeline.fit(X_train, y_train)

# --- Model Evaluation ---
# Evaluate the model
y_pred = pipeline.predict(X_test)  # X_test will be automatically preprocessed by the pipeline

# Inverse log transformation of the predictions
y_pred = np.expm1(y_pred)

# --- Save Model ---
    # Save fitted pipeline model as 'knn_log'
save_model(pipeline, 'knn_poly_4feats_time_log')

# --- Save Params and Metrics ---
    # Save params from fitted pipeline into a dict 'params'
params = pipeline.named_steps['multi_knn_regressor'].get_params()

# Define performace metrics
    # Initialize an empty dictionary to store metrics
metrics = {}
for i, target in enumerate(['Hydro', 'Solar', 'Wind', 'total_sol_wind_hyd']):
    mse = mean_squared_error(np.expm1(y_test.iloc[:, i]), y_pred[:, i])
    mae = mean_absolute_error(np.expm1(y_test.iloc[:, i]), y_pred[:, i])
    r2 = r2_score(np.expm1(y_test.iloc[:, i]), y_pred[:, i])
    rmse = np.sqrt(mse)

    # Store metrics in the dictionary
    metrics[target] = {
        # 'Mean CV Score': mean_cv_score,
        'Mean Absolute Error': mae,
        'Mean Squared Error': mse,
        'Root Mean Squared Error': rmse,
        'R-squared': r2
    }

    # Call save_performace function in registry.py to save dicts with a time stamp in the correct file
save_performance('knn_log', params, metrics)

for target, metrics_values in metrics.items():
    print(f"Metrics for {target}:")
    for metric_name, metric_value in metrics_values.items():
        print(f"    {metric_name}: {metric_value:.4f}")
    print("\n")

### --- Learning Curves --- ###

# train_sizes, train_scores, validation_scores = learning_curve(
#     estimator = pipeline,
#     X = X_train,
#     y = y_train,
#     train_sizes = np.linspace(0.1, 1.0, 5),
#     cv = 3,
#     scoring = 'r2'
# )


# # Calculate mean and standard deviation for training set scores
# train_mean = np.mean(train_scores, axis=1)
# train_std = np.std(train_scores, axis=1)

# # Calculate mean and standard deviation for validation set scores
# validation_mean = np.mean(validation_scores, axis=1)
# validation_std = np.std(validation_scores, axis=1)

# # Plot the learning curves
# plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color="r")
# plt.fill_between(train_sizes, validation_mean - validation_std, validation_mean + validation_std, alpha=0.1, color="g")
# plt.plot(train_sizes, train_mean, 'o-', color="r", label="Training score")
# plt.plot(train_sizes, validation_mean, 'o-', color="g", label="Cross-validation score")

# plt.title("Learning Curves")
# plt.xlabel("Training Set Size")
# plt.ylabel("r2")
# plt.legend(loc="best")
# plt.show()
