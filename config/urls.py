from django.contrib import admin
from django.urls import path

from cars.api.urls import urlpatterns as cars_urlpatterns
from prices.api.urls import urlpatterns as prices_urlpatterns
from users.api.urls import urlpatterns as users_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
] + cars_urlpatterns + prices_urlpatterns + users_urlpatterns
