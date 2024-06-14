data "external" "tunnel" {
  program = ["python3", "${path.module}/cloudflare.py", var.tunnel]
}

variable "tunnel" {
  type = string
  validation {
    condition     = contains(["create", "delete"], var.tunnel)
    error_message = "valid values for var: tunnel are (create or destroy)."
  }
}

variable "zone_id" {
  type = string
}

resource "cloudflare_access_service_token" "my_app" {
  name    = "CI/CD app"
  zone_id = var.zone_id
}

output "tunnel_name" {
  value = data.external.tunnel.result["TunnelName"]
}

data "template_file" "mdm_config" {
  template = file("${path.module}/mdm.xml.tmpl")

  vars = {
    ACCESS_KEY = cloudflare_access_service_token.my_app.client_id
    SECRET_KEY = cloudflare_access_service_token.my_app.client_secret
    TUNNEL_KEY = data.external.tunnel.result["TunnelSecret"]
    ORG_NAME   = "castironclay"
  }
}
output "mdm_config" {
  value = data.template_file.mdm_config.rendered
}
