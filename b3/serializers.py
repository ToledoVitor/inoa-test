from rest_framework import serializers

from b3.models import Search, StockPrice


class Searcherializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = (
            "id",
            "price_tunnel",
            "interval",
            "stocks",
            "created_at",
        )


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = (
            "stock",
            "search",
            "price",
            "created_at",
        )
