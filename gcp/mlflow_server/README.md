# MLflow Server Deployment on Google Cloud

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
