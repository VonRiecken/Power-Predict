import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from power_predict.logic.registry import save_model, save_performance

# --- Fetching Data ---
df = pd.read_csv('/Users/FernandoSandoval/code/VonRiecken/Power-Predict/power_predict/data/merged_dataset2023-12-01 18:08:35.062618.csv')
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
y = df[['Hydro', 'Solar', 'Wind', 'total_sol_wind_hyd']]

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

# --- Create Model Training ---
# KNeighborsRegressor wrapped in MultiOutputRegressor
multi_knn_regressor = MultiOutputRegressor(KNeighborsRegressor(n_neighbors=20, p=2, weights='uniform'))

# Pipeline including preprocessing and multi-output KNN regressor
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessing_pipeline),
    ('multi_knn_regressor', multi_knn_regressor)
])


# --- 5-Fold Cross-Validation ---
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
mean_cv_score = np.mean(cv_scores)
print(f"Cross-validated scores for 5 folds on the training data: {cv_scores}")
print(f"Mean CV Score: {mean_cv_score}")

# --- Model Training ---
# Train the model
pipeline.fit(X_train, y_train)

# --- Model Evaluation ---
# Evaluate the model
y_pred = pipeline.predict(X_test)  # X_test will be automatically preprocessed by the pipeline

# --- Save Model ---
    # Save fitted pipeline model as 'knn_4feats'
save_model(pipeline, 'knn_4feats')

# --- Save Params and Metrics ---
    # Save params from fitted pipeline into a dict 'params'
params = pipeline.named_steps['multi_knn_regressor'].get_params()

# Define performace metrics
    # Initialize an empty dictionary to store metrics
metrics = {}
for i, target in enumerate(['Hydro', 'Solar', 'Wind', 'total_sol_wind_hyd']):
    mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
    mae = mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
    r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
    rmse = np.sqrt(mse)

    # Store metrics in the dictionary
    metrics[target] = {
        'Mean CV Score': mean_cv_score,
        'Mean Absolute Error': mae,
        'Mean Squared Error': mse,
        'Root Mean Squared Error': rmse,
        'R-squared': r2
    }

    # Call save_performace function in registry.py to save dicts with a time stamp in the correct file
save_performance('knn_4feats', params, metrics)

for target, metrics_values in metrics.items():
    print(f"Metrics for {target}:")
    for metric_name, metric_value in metrics_values.items():
        print(f"    {metric_name}: {metric_value:.4f}")
    print("\n")
