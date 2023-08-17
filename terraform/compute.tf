module "container_vm" {
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 3.1"

  container = {
    image = var.image
  }
}

module "network" {
  source       = "terraform-google-modules/network/google"
  version      = "~> 7.3"
  project_id   = var.project_id
  network_name = var.name
  subnets = [
    {
      subnet_name           = var.name
      subnet_ip             = "10.125.0.0/20"
      subnet_region         = var.region
      subnet_private_access = true
    }
  ]
  ingress_rules = [
    {
      name = "${var.name}-lb-to-instances"
      allow = [
        {
          protocol = "tcp"
          ports    = [3000]
        }
      ]
      source_ranges = [
        "130.211.0.0/22",
        "35.191.0.0/16",
      ]
      target_service_accounts = module.service_account.emails_list
    }
  ]
}

# Router and Cloud NAT are required for installing packages from repos (apache, php etc)
module "cloud_router" {
  source  = "terraform-google-modules/cloud-router/google"
  version = "~> 5.1"

  project = var.project_id
  name    = var.name
  network = module.network.network_self_link
  region  = var.region
  nats = [
    {
      name = var.name
    }
  ]
}

module "instance_template" {
  source  = "terraform-google-modules/vm/google//modules/instance_template"
  version = "~> 8.0"

  project_id           = var.project_id
  network              = module.network.network_self_link
  subnetwork           = module.network.subnets_self_links[0]
  name_prefix          = var.name
  source_image_family  = "cos-stable"
  source_image_project = "cos-cloud"
  source_image         = reverse(split("/", module.container_vm.source_image))[0]
  metadata             = { "gce-container-declaration" = module.container_vm.metadata_value }
  tags = [
    "http-server"
  ]
  labels = {
    "container-vm" = module.container_vm.vm_container_label
  }
  service_account = {
    email = module.service_account.email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

module "mig" {
  source  = "terraform-google-modules/vm/google//modules/mig"
  version = "~> 8.0"

  project_id        = var.project_id
  region            = var.region
  hostname          = var.name
  instance_template = module.instance_template.self_link
  target_size       = 0
  min_replicas      = 0
  max_replicas      = 3
  named_ports = [
    {
      name = "http",
      port = 3000
    }
  ]
  autoscaling_enabled = true
  autoscaling_metric = [
    {
      name   = "loadbalancing.googleapis.com/https/backend_request_count"
      type   = "DELTA_PER_SECOND"
      target = 65535
    }
  ]
  autoscaling_mode = "ON"
}

module "lb_http" {
  source  = "GoogleCloudPlatform/lb-http/google"
  version = "~> 6.2"

  project                 = var.project_id
  name                    = var.name
  target_service_accounts = module.service_account.emails_list
  firewall_networks = [
    module.network.network_self_link
  ]
  backends = {
    default = {
      description                     = null
      protocol                        = "HTTP"
      port                            = 3000
      port_name                       = "http"
      timeout_sec                     = 30
      connection_draining_timeout_sec = null
      enable_cdn                      = false
      security_policy                 = null
      session_affinity                = null
      affinity_cookie_ttl_sec         = null
      custom_request_headers          = null
      custom_response_headers         = null
      health_check = {
        initial_delay_sec   = 600
        check_interval_sec  = 30
        timeout_sec         = 10
        healthy_threshold   = 1
        unhealthy_threshold = 5
        port                = 3000
        request_path        = "/livez"
        host                = ""
        logging             = false
      }
      log_config = {
        enable      = false
        sample_rate = null
      }
      groups = [
        {
          group                        = module.mig.instance_group
          balancing_mode               = null
          capacity_scaler              = null
          description                  = null
          max_connections              = null
          max_connections_per_instance = null
          max_connections_per_endpoint = null
          max_rate                     = null
          max_rate_per_instance        = null
          max_rate_per_endpoint        = null
          max_utilization              = null
        }
      ]
      iap_config = {
        enable               = false
        oauth2_client_id     = ""
        oauth2_client_secret = ""
      }
    }
  }
}
