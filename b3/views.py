import json

from django.db import transaction
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from b3.models import Search
from b3.serializers import Searcherializer


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = Searcherializer
    queryset = Search.objects.all()

    def perform_create(self, serializer):
        from b3.tasks import search_b3_task

        instance: Search = serializer.save()
        search_b3_task(instance.id)
        # try:

        #     with transaction.atomic():
        #         instance: Search = serializer.save()
        #         schedule, _ = IntervalSchedule.objects.get_or_create(
        #             every=instance.interval,
        #             period=IntervalSchedule.MINUTES,
        #         )

        #         task = PeriodicTask.objects.create(
        #             interval=schedule,
        #             name=f"Search: {instance.id}",
        #             task="b3.tasks.search_b3_task",
        #             kwargs=json.dumps(
        #                 {
        #                     "search_id": instance.id,
        #                 }
        #             ),
        #         )
        #         instance.task = task
        #         instance.save()

        # except Exception as e:
        #     raise APIException(str(e))

    def perform_destroy(self, instance):
        if instance.task is not None:
            instance.task.delete()
        return super().perform_destroy(instance)
