from rest_framework.routers import DefaultRouter

from b3.views import SearchViewSet, StockPriceViewset

router = DefaultRouter()
router.register(r"buscas", SearchViewSet, basename="buscas")
router.register(r"precos", StockPriceViewset, basename="precos")

searchs_urlpatterns = router.urls
