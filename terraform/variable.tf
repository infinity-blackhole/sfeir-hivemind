variable "project_id" {
  description = "The project id"
  type        = string
  default     = "shikanime-studio"
}

variable "name" {
  description = "The name of the hivemind"
  type        = string
  default     = "sfeir-hivemind"
}

variable "display_name" {
  description = "The display name of the hivemind"
  type        = string
  default     = "Sfeir Hivemind"
}

variable "region" {
  description = "The location of the hivemind"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "The zone of the hivemind"
  type        = string
  default     = "europe-west1-b"
}

variable "labels" {
  description = "The labels of the hivemind"
  type        = map(string)
  default     = {}
}

variable "image" {
  description = "The image of the hivemind"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}

variable "vertex_ai_project_id" {
  description = "The Vertex AI project id"
  type        = string
  default     = "shikanime-studio"
}

variable "vertex_ai_location" {
  description = "The Vertex AI location"
  type        = string
  default     = "us-central1"
}