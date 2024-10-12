from multiprocessing import cpu_count

from app.config.utils import get_settings


settings = get_settings()
bind = f'{settings.APP_HOST}:{settings.APP_PORT}'
workers = cpu_count() * 2 + 1
logconfig_json = 'log_conf.json'
worker_class = 'uvicorn.workers.UvicornWorker'
timeout = 300
