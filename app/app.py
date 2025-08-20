from flask import Flask, request
import time
import random
import requests
from prometheus_client import generate_latest, Counter, Histogram, REGISTRY

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency in seconds', ['endpoint'])

@app.route('/')
def home():
    start_time = time.time()
    # Simulate some work
    time.sleep(random.uniform(0.1, 0.5))
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)
    REQUEST_COUNT.labels(method='GET', endpoint='/', status_code=200).inc()
    return "Welcome to Monitoring Demo App!"

@app.route('/api/health')
def health():
    # Simulate health check with occasional failures
    if random.random() > 0.8:
        return "ERROR", 500
    return "OK", 200

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain'}

@app.route('/check-website')
def check_website():
    """Endpoint to check external websites"""
    url = request.args.get('url', 'https://httpbin.org/status/200')
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        request_time = time.time() - start_time
        
        REQUEST_COUNT.labels(
            method='GET', 
            endpoint='/check-website', 
            status_code=response.status_code
        ).inc()
        
        return {
            'url': url,
            'status_code': response.status_code,
            'response_time': round(request_time, 3),
            'up': response.status_code == 200
        }
    except Exception as e:
        return {'error': str(e), 'up': False}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)