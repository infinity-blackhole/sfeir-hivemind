module "service_account" {
  source       = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/iam-service-account"
  project_id   = var.project_id
  name         = var.name
  display_name = "${var.display_name} service account"
  iam_project_roles = {
    "${var.project_id}" = [
      "roles/aiplatform.user"
    ]
  }
}