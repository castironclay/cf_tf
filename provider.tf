terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "4.34.0"
    }
    external = {
      source  = "hashicorp/external"
      version = "2.3.3"
    }
    template = {
      source  = "hashicorp/template"
      version = "2.2.0"
    }
  }
}
provider "cloudflare" {
  api_key = var.api_key
  email   = var.email
}

variable "api_key" {
  type = string
}
variable "email" {
  type = string
}
