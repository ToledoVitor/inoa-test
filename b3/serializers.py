from rest_framework import serializers

from b3.models import Search, SearchRequest


class Searcherializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = (
            "id",
            "stocks",
            "all_stocks",
            "interval",
            "created_at",
        )


class SearchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchRequest
        fields = (
            "id",
            "response_time",
            "response_status",
        )
