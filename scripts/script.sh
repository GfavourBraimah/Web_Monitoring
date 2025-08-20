#!/bin/bash
echo "Starting Web Monitoring Stack..."
docker-compose up -d

echo "
 Stack is running!
 Grafana: http://localhost:3000 (admin/admin)
 Prometheus: http://localhost:9090
 Web App: http://localhost:5000
"