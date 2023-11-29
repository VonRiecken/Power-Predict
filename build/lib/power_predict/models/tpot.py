import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from tpot import TPOTRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# --- Data Collection and Preparation ---
df = pd.read_csv('our_data.csv')  ## Replace

# Separating features and target variables
features = df.drop(['target columns'], axis=1)  # Drop target columns to isolate features
targets = df[['target columns']]  # Select only the target columns

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# --- Data Preprocessing ---
# Preprocessing pipeline for missing data imputation and feature scaling
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with mean
            ('scaler', MinMaxScaler())]), features.columns)  # Scale features using MinMaxScaler
    ])

# --- Model Building with TPOT ---
# TPOT regressor for multi-target regression
tpot_regressor = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42,
                               config_dict='TPOT light', cv=5)

# Pipeline including preprocessing and TPOT regressor
pipeline = Pipeline(steps=[('preprocessor', preprocessing_pipeline),
                           ('tpot_regressor', tpot_regressor)])

# --- Model Training ---
# Train the TPOT model
pipeline.fit(X_train, y_train)

# --- Model Evaluation ---
# Evaluate the best model found by TPOT
y_pred = pipeline.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# Output performance metrics
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)

# Feature importance (TPOT might select a model where feature importance is not available)
# Here, we're assuming TPOT selected a Random Forest model. If not, this part would need to be adjusted.
if 'feature_importances_' in dir(pipeline.named_steps['tpot_regressor'].fitted_pipeline_[-1]):
    feature_importances = pipeline.named_steps['tpot_regressor'].fitted_pipeline_[-1].feature_importances_

    # Create a bar chart of feature importances
    plt.barh(range(len(feature_importances)), feature_importances, align='center')
    plt.yticks(range(len(feature_importances)), features.columns)
    plt.xlabel('Feature Importance')
    plt.ylabel('Feature')
    plt.show()
else:
    print("Selected model does not support feature importances.")
