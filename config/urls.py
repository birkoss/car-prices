from django.contrib import admin
from django.urls import path

from cars.api.urls import urlpatterns as cars_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
] + cars_urlpatterns
