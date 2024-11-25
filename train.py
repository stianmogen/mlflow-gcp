import kagglehub
import mlflow
import mlflow.keras
from mlflow.models import infer_signature
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense

SERVER_ID = ""  # use your server id
REGION = "europe-west1"
MLFLOW_TRACKING_URI = f"https://mlflow-server-${SERVER_ID}.${REGION}.run.app"
EXPERIMENT_NAME = "lstm_experiment"
MODEL_REGISTRY_NAME = "lstm_model"


def load_data():
    path = kagglehub.dataset_download(
        "rashikrahmanpritom/heart-attack-analysis-prediction-dataset")
    data = pd.read_csv(f"{path}/heart.csv")

    X = data.drop("output", axis=1).values
    y = data["output"].values
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    return x_train, y_train, x_test, y_test


def get_best_model_version(model_registry_name, key="status", value="best"):
    client = mlflow.tracking.MlflowClient()
    model_versions = client.search_model_versions(
        filter_string=f"name='{model_registry_name}'")
    for version in model_versions:
        if version.tags.get(key) == value:
            run = mlflow.get_run(version.run_id)
            accuracy = run.data.metrics.get("accuracy")
            return version, accuracy
    return None, None


def compare_and_update_models(accuracy, model_registry_name):
    client = mlflow.tracking.MlflowClient()
    best_model_version, best_model_accuracy = get_best_model_version(
        model_registry_name, key="status", value="best")

    # Register the latest model
    latest_version = mlflow.register_model(
        f"runs:/{mlflow.active_run().info.run_id}/model", model_registry_name)

    # Compare accuracies
    if best_model_accuracy is None or accuracy > best_model_accuracy:
        if best_model_version is not None:
            client.set_model_version_tag(
                model_registry_name, best_model_version.version, "status", "previous_best")
        client.set_model_version_tag(
            model_registry_name, latest_version.version, "status", "best")
        print(f"New model with accuracy {accuracy:.2f} is now the best model.")
    else:
        print(f"New model with accuracy {
              accuracy:.2f} did not outperform the current best model with accuracy {best_model_accuracy:.2f}.")


def calculate_accuracy(y_true, y_pred):
    return accuracy_score(y_true, (y_pred > 0.5).astype(int))


def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=input_shape))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


x_train, y_train, x_test, y_test = load_data()

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)
signature = infer_signature(x_train, y_train)

with mlflow.start_run() as run:
    input_shape = (x_train.shape[1], 1)
    x_train = np.expand_dims(x_train, axis=2)
    x_test = np.expand_dims(x_test, axis=2)

    model = build_lstm_model(input_shape)

    # Train the model
    model.fit(x_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

    # Log the model
    mlflow.keras.log_model(model, "lstm_model")

    # Make predictions
    predictions = model.predict(x_test)
    accuracy = calculate_accuracy(y_test, predictions)

    # Log accuracy as a metric
    mlflow.log_metric("accuracy", accuracy)

    # Register and compare models
    compare_and_update_models(accuracy, MODEL_REGISTRY_NAME)
