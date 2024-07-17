from rest_framework.routers import DefaultRouter

from b3.views import SearchRequestViewSet, SearchViewSet


router = DefaultRouter()
router.register(r"searchs", SearchViewSet, basename="searchs")
router.register(r"requests", SearchRequestViewSet, basename="requests")

searchs_urlpatterns = router.urls
