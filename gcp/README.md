# MLflow Server and Prediction Pipeline Deployment on Google Cloud

This guide covers deploying an MLflow server on Google Cloud Platform (GCP) using `gcloud` CLI commands.

## Steps

### 1. Set up a PostgreSQL Instance

Set up a PostgreSQL database to store MLflow tracking data.

```bash
gcloud sql instances create INSTANCE-NAME \
  --database-version=POSTGRES_15 \
  --region=eu-west1 \
  --tier=db-f1-micro \
  --storage-type=HDD \
  --storage-size=10GB \
  --authorized-networks=0.0.0.0/0
```
```bash
gcloud sql users create USERNAME --instance=INSTANCE-NAME --password=PASSWORD
```
```bash
gcloud sql databases create DATABASE-NAME --instance=INSTANCE-NAME
```

### 2. Create a Google Cloud Storage Bucket
This bucket will store your model artifacts and other large files.
```bash
gcloud storage buckets create gs://BUCKET-NAME

```

### 3. Create an Artifact Registry
The Artifact Registry will host Docker images used in Cloud Run deployments.
```bash
gcloud artifacts repositories create ARTIFACT-REPO-NAME \
  --location=eu-west1 \
  --repository-format=docker
```

### 4. Build and Deploy MLflow Docker Image
Build the Docker image:
```bash
docker buildx build --platform linux/amd64 -t europe-west1-docker.pkg.dev/PROJECT-NAME/REPO-NAME/mlflow-server:latest .
```
Push the Docker image to Artifact Registry:
```bash
docker push europe-west1-docker.pkg.dev/PROJECT-NAME/REPO-NAME/mlflow-server:latest
```
### 5. Deploy to Cloud Run

```bash
gcloud run deploy mlflow-server \
  --image=europe-west1-docker.pkg.dev/PROJECT-NAME/REPO-NAME/mlflow-server:latest \
  --region=eu-west1 \
  --platform=managed \
  --service-account=SERVICE-ACCOUNT \
  --memory=1Gi \
  --port=8080
```

### 6. Service Account Permission

Depending on the service account you use, you may want to add additional permissions to read and write to the database, cloud storage and artifact registry.

To allow the MLflow server access to necessary Google Cloud resources, grant the service account specific roles. 

```bash
# Artifact Registry Administrator
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/artifactregistry.admin'

# Cloud SQL Editor
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/cloudsql.editor'

# Storage Object Admin
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/storage.objectAdmin'

# Secret Manager Secret Accessor
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/secretmanager.secretAccessor'

# Cloud Functions Admin
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/cloudfunctions.admin'

# Cloud Deploy Service Agent
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/clouddeploy.serviceAgent'

# Container Analysis Occurrences Viewer
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/containeranalysis.occurrences.viewer'

# BigQuery Data Viewer
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member='serviceAccount:SERVICE-ACCOUNT-NAME@PROJECT-ID.iam.gserviceaccount.com' \
  --role='roles/bigquery.dataViewer'
```

# Prediction pipeline

This guide covers deploying the prediction pipeline on Google Cloud Platform (GCP) using `gcloud` CLI commands.

1. ETL Function
```
gcloud functions deploy etl_function \
  --runtime python312 \
  --trigger-http \
  --timeout 900s \
  --memory 512MB \
  --source=gcp/etl \
  --region=europe-west1 \
  --set-env-vars 
```

2. Pre Process Function

```
gcloud functions deploy pre_process_function \
  --runtime python312 \
  --trigger-http \
  --timeout 120s \
  --memory 1024MB \
  --source=cloud_functions/pre_process \
  --region=europe-west1 \
  --set-env-vars 
```

3. Prediction Function

```
gcloud functions deploy predict_function \
  --runtime python312 \
  --trigger-http \
  --timeout 120s \
  --memory 1024MB \
  --source=cloud_functions/predict \
  --region=europe-west1 \
  --set-env-vars 
```
