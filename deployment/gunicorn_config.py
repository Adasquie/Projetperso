import os
import multiprocessing

# Bind
port = int(os.environ.get('PORT', 8000))
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = 1  # Start with just one worker
worker_class = 'sync'
timeout = 300
keepalive = 5

# Startup configuration
preload_app = True
max_requests = 100
max_requests_jitter = 10

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'critical'  # Set to debug for more information

# SSL Configuration (if needed)
keyfile = None
certfile = None 