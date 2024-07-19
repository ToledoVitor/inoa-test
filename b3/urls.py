from rest_framework.routers import DefaultRouter

from b3.views import SearchViewSet

router = DefaultRouter()
router.register(r"searchs", SearchViewSet, basename="searchs")

searchs_urlpatterns = router.urls
