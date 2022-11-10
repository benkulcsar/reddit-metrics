variable "REDDIT_CLIENT_ID" {
  type      = string
  sensitive = true
}

variable "REDDIT_CLIENT_SECRET" {
  type      = string
  sensitive = true
}

variable "REDDIT_S3_BUCKET" {
  type = string
}

variable "GCP_ACCESS_KEY" {
  type      = string
  sensitive = true
}

variable "GCP_SECRET_ACCESS_KEY" {
  type      = string
  sensitive = true
}
