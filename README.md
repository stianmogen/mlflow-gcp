# MLflow on Google Cloud Platform

This repository provides an MLOps setup using MLflow, hosted on Google Cloud Platform (GCP), for model training, tracking, and deployment. The setup includes Terraform configuration for infrastructure, MLflow server setup using Cloud Run, and Google Cloud resources such as PostgreSQL for tracking, Google Cloud Storage for artifact storage.

### Repository Structure

- **`gcp/mlflow_server`**: Contains the MLflow server setup with instructions to deploy via `gcloud` CLI.
- **`gcp/etl`**: Contains ETL function setup with instructions to deploy via `gcloud` CLI.
- **`gcp/pre_process`**: Contains pre-process function setup with instructions to deploy via `gcloud` CLI.
- **`gcp/predict`**: Contains the prediction function setup with instructions to deploy via `gcloud` CLI.
- **Terraform configuration files**: Scripts to set up Google Cloud resources like Cloud Run, PostgreSQL, artifact storage, and secrets.
- **`train.py`**: Training script using MLflow for model versioning and logging.

### Prerequisites

- **Google Cloud SDK** installed and configured
- A **Google Cloud project** with appropriate permissions
- **Terraform** installed (optional)