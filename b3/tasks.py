from celery import shared_task

from b3.models import Search
from b3.services.brapi import BRAPIService


@shared_task(bind=True)
def search_b3_task(self, search_id: int):
    try:
        search = Search.objects.get(id=search_id)
        BRAPIService().handle(search=search)

    except Exception as e:
        print(str(e), type(e))
