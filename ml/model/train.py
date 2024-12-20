import numpy as np
import mlflow
import mlflow.sklearn
import lightgbm as lgb
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Set tracking URI and experiment
mlflow.set_tracking_uri("file:./mlruns")
experiment_name = "lightgbm_classification_model"
mlflow.set_experiment(experiment_name)

# Load dataset
data = load_iris()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start logging
with mlflow.start_run():
    # Define LightGBM model
    model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions and calculate accuracy
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Log params, metrics, and input example
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("learning_rate", 0.1)
    mlflow.log_metric("accuracy", accuracy)

    # Log the model with input_example
    input_example = np.array([X_train[0]])
    mlflow.sklearn.log_model(model, "model", input_example=input_example)

    print(f"Model logged successfully with Accuracy: {accuracy}")
