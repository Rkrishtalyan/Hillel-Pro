import os
from celery import Celery

# ---- PostgreSQL Configuration (Commented for Reference) ----
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
# app = Celery('root')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
#
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# ---- Redis and MongoDB Configuration ----
app = Celery('root')
app.conf.broker_url = 'redis://localhost:6379/0'  # Redis broker URL
app.conf.result_backend = 'mongodb://localhost:27017/book_manager'  # MongoDB result backend
app.conf.mongodb_backend_settings = {
    'database': 'book_manager',  # MongoDB database for task metadata
    'taskmeta_collection': 'celery_taskmeta',  # Collection for storing task metadata
}
