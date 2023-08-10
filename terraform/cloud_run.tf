resource "google_cloud_run_v2_service" "default" {
  provider     = google-beta
  project      = var.project_id
  name         = var.name
  location     = var.location
  labels       = var.labels
  ingress      = "INGRESS_TRAFFIC_ALL"
  launch_stage = "BETA"

  template {
    timeout               = "600s"
    service_account       = module.service_account.email
    execution_environment = "EXECUTION_ENVIRONMENT_GEN2"
    scaling {
      max_instance_count = 3
    }
    containers {
      image = var.image

      env {
        name  = "DEEP_LAKE_DATASET_URI"
        value = "gcs://${module.bucket.name}/books/"
      }
      env {
        name  = "VERTEX_AI_PROJECT"
        value = var.vertex_ai_project_id
      }
      env {
        name  = "VERTEX_AI_LOCATION"
        value = var.vertex_ai_location
      }
      env {
        name  = "OPENLLM_LLAMA_FRAMEWORK"
        value = "pt"
      }
      env {
        name  = "OPENLLM_LLAMA_MODEL_ID"
        value = "NousResearch/Llama-2-7b-chat-hf"
      }
      ports {
        container_port = 3000
      }
      resources {
        limits = {
          cpu    = "6000m"
          memory = "16Gi"
        }
        cpu_idle          = true
        startup_cpu_boost = true
      }
      liveness_probe {
        http_get {
          path = "/livez"
          port = 3000
        }
      }
      startup_probe {
        http_get {
          path = "/readyz"
          port = 3000
        }
        initial_delay_seconds = 120
      }
      volume_mounts {
        name       = "torch-cache"
        mount_path = "/home/bentoml/.cache/torch"
      }
    }

    volumes {
      name = "torch-cache"
      empty_dir {
        medium     = "MEMORY"
        size_limit = "512Mi"
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service_iam_member" "default" {
  provider = google-beta
  project  = var.project_id
  location = var.location
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
