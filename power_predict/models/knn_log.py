import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# --- Fetching Data ---
df = pd.read_csv('/Users/FernandoSandoval/code/VonRiecken/Power-Predict/power_predict/data/merged_dataset2023-11-29 16:33:32.960189.csv')
df.head(5)

# --- Data Preprocessing ---

# Assuming 'df' is your DataFrame

# Setting Country + Month year as Index
df['Country_Month'] = df['Country'] + '_' + df['Month_year'].astype(str)
df = df.set_index('Country_Month')

# Separating features and target variables
X = df.drop(['Unnamed: 0', 'Month_year', 'Balance',
             'Combustible_Renewables', 'Hydro', 'Other_Renewables', 'Solar',
             'Total_Renewables__Hydro__Geo__Solar__Wind__Other_', 'Wind',
             'total_sol_wind_hyd'], axis=1)

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

# --- Create Model Training ---
# KNeighborsRegressor wrapped in MultiOutputRegressor
multi_knn_regressor = MultiOutputRegressor(KNeighborsRegressor(n_neighbors=20, p=2, weights='uniform'))

# Pipeline including preprocessing and multi-output KNN regressor
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessing_pipeline),
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
