
# --------- Variables for the project --------- 
variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  default     = "europe-west1"
}

# --------- Service accounts and secrets --------- 
variable "service_account_name" {
  description = "The name of the service account"
}

variable "postgres_password_secret_id" {
  description = "Id for accessing postgres password secret"
}


variable "postgres_url_secret_id" {
  description = "Id for accessing postgres url secret"
}

variable "bucket_secret_id" {
  description = "Id for accessing bucket secret"
}


variable "access_keys_secret_id" {
  description = "Id for accessing access keys secret"
}


# --------- Storage (buckets, database, registry, datasets and tables) --------- 
variable "mlflow_bucket_name" {
  description = "Name of bucket storing mlflow artifacts"
}

variable "mlflow_db_name" {
  description = "Name of mlflow database"
}

variable "mlflow_db_instance_name" {
  description = "Name of mlflow database instance"
}

variable "mlflow_db_user_name" {
  description = "Name of mlflow database user"
}

variable "artifact_repo_name" {
  description = "Name of repository in artifact registry"
}

variable "tf_bucket_name" {
  description = "Name of bucket storing Terraform state"
}
