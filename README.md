# Cloudflare Tunnel
Manage Cloudflare Zero-Trust tunnels from the CLI
## Requirement
- Cloudfare account
- Python3.12

## Setup
```bash
python3.12 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Required Files
cf_config.yaml
```yaml
---
account_id:
api_key:
api_email:
organization:
zone_id:
r2_bucket:
r2_token:
r2_access_key:
r2_secret_key:
r2_endpoint:
```

terraform.tfvars
```bash
email   = 
zone_id = 
api_key =
```
