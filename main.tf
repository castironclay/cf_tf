data "external" "tunnel1" {
  program = ["python3", "${path.module}/cloudflare.py", var.tunnel, "${var.tunnel_name}1"]
}

data "external" "tunnel2" {
  program = ["python3", "${path.module}/cloudflare.py", var.tunnel, "${var.tunnel_name}2"]
}

variable "tunnel" {
  type = string
  validation {
    condition     = contains(["create", "delete"], var.tunnel)
    error_message = "valid values for var: tunnel are (create or delete)."
  }
}

variable "tunnel_name" {
  type = string
}

variable "zone_id" {
  type = string
}

resource "cloudflare_access_service_token" "my_token" {
  name    = var.tunnel_name
  zone_id = var.zone_id
}

data "template_file" "mdm_config1" {
  template = file("${path.module}/mdm.xml.tmpl")

  vars = {
    ACCESS_KEY = cloudflare_access_service_token.my_token.client_id
    SECRET_KEY = cloudflare_access_service_token.my_token.client_secret
    TUNNEL_KEY = data.external.tunnel1.result["TunnelSecret"]
    ORG_NAME   = "castironclay"
  }
}

data "template_file" "mdm_config2" {
  template = file("${path.module}/mdm.xml.tmpl")

  vars = {
    ACCESS_KEY = cloudflare_access_service_token.my_token.client_id
    SECRET_KEY = cloudflare_access_service_token.my_token.client_secret
    TUNNEL_KEY = data.external.tunnel2.result["TunnelSecret"]
    ORG_NAME   = "castironclay"
  }
}
output "mdm_config1" {
  value = data.template_file.mdm_config1.rendered
}

output "mdm_config2" {
  value = data.template_file.mdm_config2.rendered
}
resource "local_file" "mdm1" {
  content  = data.template_file.mdm_config1.rendered
  filename = "${path.module}/mdm1.xml"
}

resource "local_file" "mdm2" {
  content  = data.template_file.mdm_config2.rendered
  filename = "${path.module}/mdm2.xml"
}
