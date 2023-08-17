module "bucket" {
  source        = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/gcs"
  project_id    = var.project_id
  prefix        = var.project_id
  name          = "${var.name}-deep-lake-datasets"
  location      = var.region
  storage_class = "REGIONAL"
  labels        = var.labels
  iam = {
    "roles/storage.objectViewer" = [
      module.service_account.iam_email
    ]
    "roles/storage.insightsCollectorService" = [
      module.service_account.iam_email
    ]
  }
}
