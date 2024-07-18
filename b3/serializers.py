from rest_framework import serializers

from b3.models import Search


class Searcherializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = (
            "id",
            "stocks",
            "price_tunnel",
            "interval",
            "created_at",
        )
