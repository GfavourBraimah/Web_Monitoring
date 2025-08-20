# Generate some traffic to see metrics
for i in {1..30}; do
  curl http://localhost:5000
  curl http://localhost:5000/api/health
  sleep 0.5
done