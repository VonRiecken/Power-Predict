from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from power_predict.logic.registry import save_model


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

save_model(model_trained, 'test_john')
