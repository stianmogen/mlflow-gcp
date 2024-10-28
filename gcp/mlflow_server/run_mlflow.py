import subprocess
from google.cloud import secretmanager

# Initialize the Secret Manager client
secret_client = secretmanager.SecretManagerServiceClient()

def access_secret_version(secret_id, project_id):
    """
    Access a secret from Secret Manager.
    :param secret_id: ID of the secret to access.
    :param project_id: GCP Project ID where the secret is stored.
    :return: The secret payload.
    """
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Fetch secrets
POSTGRESQL_URL = access_secret_version("mlflow-db-url")  # Fetch PostgreSQL URL
STORAGE_URL = access_secret_version("mlflow-bucket-url")  # Fetch the GCS bucket URL for artifacts

# Upgrade the MLflow database schema
print(f"Upgrading MLflow database schema at {POSTGRESQL_URL}")
subprocess.run(["mlflow", "db", "upgrade", POSTGRESQL_URL])

# Start the MLflow server
print(f"Starting MLflow server on port 8080 with backend store {POSTGRESQL_URL} and artifact destination {STORAGE_URL}")
subprocess.run([
    "mlflow", "server",
    "--host", "0.0.0.0",
    "--port", "8080",
    "--backend-store-uri", POSTGRESQL_URL,
    "--artifacts-destination", STORAGE_URL
])
