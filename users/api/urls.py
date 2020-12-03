from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/login', api_views.loginUser.as_view(), name='login'),
]
