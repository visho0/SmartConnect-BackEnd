# Configuración de Gunicorn para producción
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
user = None  # Se configurará según el usuario del sistema
group = None
pidfile = "/var/run/gunicorn/smartconnect.pid"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

