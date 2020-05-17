import os
PORT = os.getenv('PORT', 5000)

pidfile = 'app.pid'
worker_tmp_dir = '/dev/shm'
worker_class = 'gthread'
workers = 2
worker_connections = 1000
timeout = 30
keepalive = 2
threads = 4
proc_name = 'app'
bind = f'0.0.0.0:{PORT}'
backlog = 2048
accesslog = '-'
errorlog = '-'
