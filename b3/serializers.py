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
    stock_code = serializers.SerializerMethodField()
    search_str = serializers.SerializerMethodField()

    class Meta:
        model = StockPrice
        fields = (
            "stock_code",
            "search_str",
            "price",
            "created_at",
        )

    def get_stock_code(self, obj: StockPrice):
        return obj.stock.code
    
    def get_search_str(self, obj: StockPrice):
        return obj.search.__str__()
