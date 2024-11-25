import os
import pandas as pd
from google.cloud import bigquery

# Load environment variables with defaults
PROJECT_ID = os.getenv('GCP_PROJECT_ID')


DATASET_ETL_ID = os.getenv('DATASET_ETL_ID', '1_bronze')
TABLE_ETL_ID = os.getenv('TABLE_ETL_ID', 'raw_data')


def fetch_data_from_api():
    # TODO Denne vil avhenge av din datakilde
    return


def transform_data(df: pd.DataFrame):
    # TODO Hvis du trenger å gjøre transformasjon av dataen før du lagrer i skyen, feks anonymisering
    return df


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


def run_etl():
    try:
        data = fetch_data_from_api()
        df = pd.DataFrame(data)
        df = transform_data()
        save_to_bq(df, PROJECT_ID, DATASET_ETL_ID, TABLE_ETL_ID)
        logging.info("ETL process completed successfully.")
    except Exception as e:
        logging.error(f"ETL process failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_etl()
