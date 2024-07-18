# inoa-test


Rodar o projeto:

Django
python manage.py runserver


Celery
celery -A core worker --loglevel=info -P gevent --concurrency 1 -E


Celery Beat
celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --max-interval 10
