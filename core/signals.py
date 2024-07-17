# from django.db import transaction
# from django.db.models import signals
# from django.dispatch import receiver

# from b3.models import SearchConfig
# from core.tasks import B3StockCrawler


# @receiver(signal=signals.post_save, sender=SearchConfig)
# def run_stock_search(sender, instance, created, **kwargs):
#     if created:
#         transaction.on_commit(
#             lambda: B3StockCrawler.handle(instance)
#         )

# def call_crawler_task(config: SearchConfig):
#     B3StockCrawler.handle(config)

