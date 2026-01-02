#!/bin/bash
# Check health of all services

set -euo pipefail

check_service() {
    local service=$1
    local url=$2
    
    if curl -sf "$url" > /dev/null; then
        echo "[OK] $service is healthy"
        return 0
    else
        echo "[FAIL] $service is unhealthy"
        return 1
    fi
}

echo "Checking service health..."
echo "======================================"

check_service "nginx" "http://localhost/health"
check_service "Flask API" "http://localhost/api/health"

echo "======================================"
echo "Docker container status:"
docker-compose ps
