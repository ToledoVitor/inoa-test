from django.contrib import admin
from django.urls import path

from b3.urls import searchs_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += searchs_urlpatterns
