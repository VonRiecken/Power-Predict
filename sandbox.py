from power_predict.params import *
from power_predict.logic.registry import *
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X, y = [[1], [2], [3], [4], [5]], [2, 4, 5, 4, 5]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple linear regression model
# model = LinearRegression()
# model.fit(X_train, y_train)

model = load_model()

# Make predictions on the test set
y_pred = model.predict(X_test)

# Print the mean squared error as a quick evaluation metric
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# save_results(model.get_params, model.get_params)

# save_model(model)

# print({LOCAL_PATH_PARAMS})

# print(__file__)
