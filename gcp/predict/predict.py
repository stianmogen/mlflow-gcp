import logging
import os
from datetime import datetime
import mlflow
import mlflow.keras
import pandas as pd
from google.cloud import bigquery

# Set up MLflow tracking URI
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

MODEL_REGISTRY_NAME = os.getenv('MODEL_REGISTRY_NAME', 'lstm_model')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize BigQuery client
client = bigquery.Client()

PROJECT_ID = os.getenv('PROJECT_ID')

DATASET_PRE_PROCESSED_ID = os.getenv('DATASET_PRE_PROCESSED_ID', '2_silver')
TABLE_PRE_PROCESSED_ID = os.getenv('TABLE_PRE_PROCESSED_ID', 'pre_processed')

DATASET_PREDICTIONS_ID = os.getenv('DATASET_PREDICTIONS_ID', '3_gold')
TABLE_PREDICTIONS_ID = os.getenv('TABLE_PREDICTIONS_ID', 'predictions')


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


def make_predictions(model, data):
    """
    Makes predictions using the trained model.
    """
    predictions = model.predict(data)
    return predictions


def load_model(model_uri):
    """
    Loads the MLflow model from the specified URI with custom objects using mlflow.keras.
    """
    try:
        logging.info(f"Loading model from {model_uri}")
        loaded_model = mlflow.keras.load_model(model_uri)
        logging.info("Model loaded successfully.")
        return loaded_model
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        raise


def load_data_from_bq(project_id, dataset_id, table_id):
    """
    Loads data from the specified BigQuery table.
    """
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    query = f"SELECT * FROM `{full_table_id}`"

    try:
        logging.info(f"Querying BigQuery table: {full_table_id}")
        df = client.query(query).to_dataframe()
        df['time'] = pd.to_datetime(df['time'])
        df = df.sort_values(by='time', ascending=True)
        return df
    except Exception as e:
        logging.error(f"Error loading data from BigQuery: {str(e)}")
        raise


def save_to_bq(df, project_id, dataset_id, table_id):
    try:
        client = bigquery.Client(project=project_id)
        table_ref = client.dataset(dataset_id).table(table_id)

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            autodetect=True
        )

        # Last opp data til BigQuery
        job = client.load_table_from_dataframe(
            df, table_ref, job_config=job_config)
        job.result()

        logging.info(
            f"Data successfully loaded into BigQuery table: {table_id}")
    except Exception as e:
        logging.error(f"Error saving data to BigQuery: {str(e)}")
        raise


def clear_table_in_bq(project_id, dataset_id, table_id):
    """
    Clears all rows from the specified BigQuery table.
    """
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    query = f"DELETE FROM `{full_table_id}` WHERE TRUE"
    try:
        logging.info(f"Clearing table: {table_id}")
        client.query(query).result()  # Execute the delete query
        logging.info(f"Table {table_id} cleared successfully.")
    except Exception as e:
        logging.error(f"Error clearing table {table_id}: {str(e)}")
        raise


def fetch_mlflow_params(run_id):
    """
    Fetches the parameters stored in the MLflow run.
    """
    client = mlflow.tracking.MlflowClient()
    run = client.get_run(run_id)

    # Fetch parameters
    params = run.data.params
    print(params)
    aggregation_size = params.get('aggregation_size')
    features = eval(params.get('features'))  # Evaluate list string to list
    # Evaluate dictionary string to dict
    pass_id_mapping = eval(params.get('pass_ids'))

    return aggregation_size, features, pass_id_mapping


def run_predict():
    """
    Main function to run the prediction process.
    """
    try:
        # Set MLflow tracking URI
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

        # Fetch the best model version
        model_version, _ = get_best_model_version(
            MODEL_REGISTRY_NAME, "status", "best")
        model = mlflow.keras.load_model(model_version.source)

        # Load data from BigQuery
        data = load_data_from_bq(
            PROJECT_ID, DATASET_PRE_PROCESSED_ID, TABLE_PRE_PROCESSED_ID)

        # Make predictions
        predictions = model.predict(data)

        # Append predictions and current timestamp to the DataFrame
        data['predictions'] = predictions
        data['prediction_time'] = datetime.now()

        # Save updated DataFrame to BigQuery
        save_to_bq(
            data, PROJECT_ID, DATASET_PREDICTIONS_ID, TABLE_PREDICTIONS_ID)

        logging.info("Prediction process completed successfully.")

    except Exception as e:
        logging.error(f"Prediction process failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_predict()
