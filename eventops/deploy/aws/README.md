# AWS EC2 / Lightsail deployment via Docker Compose
# Usage:
#   1. Launch Ubuntu 22.04 instance (t3.medium+)
#   2. Install Docker + Docker Compose
#   3. Clone repo
#   4. Copy .env.prod -> .env
#   5. Run: docker compose -f deploy/docker-compose.prod.yml up -d
#
# ALB / SSL:
#   - Terminate SSL at ALB (port 443 -> instance port 80)
#   - Or use nginx + certbot for self-managed SSL
#
# EC2 User Data:
#   #!/bin/bash
#   apt update && apt install -y docker.io docker-compose-v2
#   git clone https://github.com/BarahWare/TTLCONFE.git /opt/eventops
#   cd /opt/eventops
#   cp deploy/.env.prod .env
#   docker compose -f deploy/docker-compose.prod.yml up -d
