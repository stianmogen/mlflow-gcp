resource "google_workflows_workflow" "etl_process_predict_pipeline" {
  name = "etl_process_predict_pipeline"

  description = "Prediction pipeline with ETL, Pre-process, and Predict steps"

  source_contents = <<-EOT
    main:
      steps:
        - run_etl:
            call: http.post
            args:
              url: https://${var.region}-${var.project_id}.cloudfunctions.net/${google_cloudfunctions2_function.etl.name}
              auth:
                type: OIDC
        - run_pre_process:
            call: http.post
            args:
              url: https://${var.region}-${var.project_id}.cloudfunctions.net/${google_cloudfunctions2_function.pre_process.name}
              auth:
                type: OIDC
        - run_predict:
            call: http.post
            args:
              url: https://${var.region}-${var.project_id}.cloudfunctions.net/${google_cloudfunctions2_function.predict.name}
              auth:
                type: OIDC
        - return_value:
            return: "Prediction Workflow Completed"
    EOT
}

resource "google_cloud_scheduler_job" "etl_process_predict_job" {
  name   = "etl_process_predict_job"
  region = var.region

  schedule  = "0 0 * * *" # Hver natt ved midnatt
  time_zone = "Etc/UTC"

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/projects/${var.project_id}/locations/${var.region}/workflows/${google_workflows_workflow.etl_process_predict_pipeline.name}/executions"

    oauth_token {
      service_account_email = var.service_account_name
    }
  }
}
