from datetime import datetime, timedelta
from decimal import Decimal

import requests
from celery import shared_task

from b3.models import Search, SearchRequest


@shared_task(bind=True)
def search_b3_task(search_id: int):
    try:
        search = Search.objects.get(id=search_id)

        # FAZER REQUEST AQUI
        # ENTENDER OS TUNEIS DE PRECO
        response = requests.get(search.endpoint, timeout=60)

        SearchRequest.objects.create(
            response_time=int(response.elapsed.total_seconds() * 1000),
            response_status=response.status_code,
            search=search,
        )

    except Exception as e:
        print(str(e), type(e))
