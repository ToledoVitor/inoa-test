import json

from django.db import transaction
from django.shortcuts import get_object_or_404
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from b3.models import Search, StockPrice
from b3.serializers import Searcherializer, StockPriceSerializer


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = Searcherializer
    queryset = Search.objects.all()

    def perform_create(self, serializer: Searcherializer):
        try:

            with transaction.atomic():
                instance: Search = serializer.save()
                schedule, _ = IntervalSchedule.objects.get_or_create(
                    every=instance.interval,
                    period=IntervalSchedule.MINUTES,
                )

                task = PeriodicTask.objects.create(
                    interval=schedule,
                    name=f"Search: {instance.id}",
                    task="b3.tasks.search_b3_task",
                    kwargs=json.dumps(
                        {
                            "search_id": instance.id,
                        }
                    ),
                )
                instance.task = task
                instance.save()

        except Exception as e:
            raise APIException(str(e))

    def perform_destroy(self, instance: Search):
        if instance.task is not None:
            instance.task.delete()
        return super().perform_destroy(instance)


class StockPriceViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = StockPrice.objects.all()
        serializer = StockPriceSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StockPrice.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StockPriceSerializer(user)
        return Response(serializer.data)
