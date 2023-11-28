from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error

# --- Data Collection and Preparation ---

df = pd.read_csv('our_data.csv')  ## Replace with data source

# Separating features and target variables
features = df.drop(['target columns'], axis=1) # axis 1 to drop columns
targets = df[['target columns'']]

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# --- Data Preprocessing ---
# Preprocessing pipeline for missing data imputation and feature scaling
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),  ## Imputing missing values with mean -- use something else?
            ('scaler', MinMaxScaler())]), features.columns)  # Scaling features using MinMaxScaler
    ])

# --- Model Building with Grid Search ---
# Random Forest regressor
rf = RandomForestRegressor(random_state=42) ## another random state?

# Pipeline including preprocessing and the regressor
pipeline = Pipeline(steps=[('preprocessor', preprocessing_pipeline),
                           ('regressor', rf)])

# Parameters for GridSearchCV
param_grid = {           ## try different ones given initial results and iterate
    'regressor__n_estimators': [100, 200, 300],
    'regressor__max_depth': [10, 20, 30, None],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4]
}

# Grid search with 5-fold cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)

# --- Model Training and Validation ---
# Training the model using Grid Search
grid_search.fit(X_train, y_train)

# --- Model Evaluation ---
# Evaluate the best model found by Grid Search
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# Outputting performance metrics and best model parameters
print("Best Model Parameters:", grid_search.best_params_)
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)

# Feature importance from the best model's Random Forest regressor
feature_importances = best_model.named_steps['regressor'].feature_importances_

# Create a bar chart of feature importances
plt.barh(range(len(feature_importances)), feature_importances, align='center')
plt.yticks(range(len(feature_importances)), features.columns)
plt.xlabel('Feature Importance')
plt.ylabel('Feature')
plt.show()
