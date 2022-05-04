import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = '127.0.0.1:8000'
timeout = 3600
accesslog = 'log/access.log'
errorlog = 'log/error.log'
capture_output = True
loglevel = "debug"
log_level = "debug"
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" '