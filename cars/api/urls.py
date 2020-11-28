from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'makes',
        api_views.makes.as_view(),
        name='makes'
    ),
    path(
        'make/<str:make>',
        api_views.make.as_view(),
        name='make'
    ),
]
