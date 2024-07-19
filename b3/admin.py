from django.contrib import admin

from b3.models import Search, Stock, StockPrice


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    readonly_fields = ["code"]


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    pass


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    pass
