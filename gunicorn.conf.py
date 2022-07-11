import os
num_workers = int(os.environ.get('WSGI_WORKERS', 2))
workers = num_workers
timeout = 600 #seconds
