import os
import pandas as pd
from google.cloud import bigquery
import logging

# Load environment variables with defaults
PROJECT_ID = os.getenv('GCP_PROJECT_ID')

DATASET_ETL_ID = os.getenv('DATASET_ETL_ID', '1_bronze')
TABLE_ETL_ID = os.getenv('TABLE_ETL_ID', 'raw_data')

DATASET_ID = os.getenv('DATASET_PRE_PROCESS_ID', '2_silver')
TABLE_ID = os.getenv('TABLE_PRE_PROCESS_ID', 'pre_processed')


def load_data_from_bq(project_id, dataset_id, table_id, columns):
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    query = f"SELECT `{column}` FROM `{full_table_id}`"

    try:
        df = client.query(query).to_dataframe()
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


def process_data(df: pd.DataFrame):
    # TODO Legg til pre-processering slik at dataen er klar for analyse i maskinlæringsmodellen din
    return df


def run_pre_process():
    """
     Main function to process the raw data and save it to the pre processed table.
     """
       try:
            logging.info("Loading data from BigQuery...")
            df = load_data_from_bq(
                PROJECT_ID, DATASET_ETL_ID, TABLE_ETL_ID, columns="*")

            # Process the data using some processing logic (assuming process_met_data exists)
            logging.info("Processing data...")
            df_processed = process_data(df)

            logging.info("Saving reduced data to BigQuery...")
            save_to_bq(df_processed, PROJECT_ID,
                       DATASET_ID, TABLE_ID)

        except Exception as e:
            logging.error(f"Pre-process failed: {str(e)}")
            raise


if __name__ == "__main__":
    run_pre_process()
