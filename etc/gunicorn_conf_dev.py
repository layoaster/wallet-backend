# gunicorn's configuration for development.
# For configuration details go to: http://docs.gunicorn.org/en/stable/configure.html

# Server Socket
backlog = 2048  # default
bind = "0.0.0.0:5000"

# Worker Processes
graceful_timeout = 90
keepalive = 2  # default
max_requests = 0  # default
timeout = 2000
worker_class = "sync"
worker_connections = 1000  # default
workers = 2

# Security
limit_request_fields = 100  # default
limit_request_field_size = 8190  # default
limit_request_line = 4094  # default


# Server Mechanics
chdir = "/code/wallet_api"
daemon = False  # default
group = 0  # default
pidfile = "/var/run/gunicorn.pid"
umask = 0  # default
user = 0  # default
worker_tmp_dir = "/dev/shm"   # http://docs.gunicorn.org/en/stable/faq.html#blocking-os-fchmod

# Debug
reload = True

# Logging
accesslog = "-"
errorlog = "-"  # default
loglevel = "debug"
