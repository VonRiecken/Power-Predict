from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from power_predict.logic.registry import save_model, save_performance


# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a simple Decision Tree classifier
model = DecisionTreeClassifier()

# Train the model
model_trained = model.fit(X_train, y_train)

model_name = 'test_john'
params = 'r2 score'
metrics = 'mae_score'
save_performance(model_name, params, metrics)
save_model(model_trained, model_name)


# General Structure:
    # df = cleaned_df()
    # df = targets_and_features(df)
    # X_train, X_test, y_train, y_test = train_test_split(df)
    # X_train_proc = preprocess(X_train)

    # if needed:
        # y_train_log = log_transform(y_train)
        # X_train_proc = polynomial_function(X_train_proc)

    # params
    # model.fit()
    # save_results('model_name', params, metrics)
    # save_model(model, 'model_name')
