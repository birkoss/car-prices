from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'api/makes',
        api_views.makes.as_view(),
        name='makes'
    ),
    path(
        'api/make/<str:make>/models',
        api_views.models.as_view(),
        name='models'
    ),
    path(
        'api/make/<str:make>/model/<str:model>/trims',
        api_views.trims.as_view(),
        name='trims'
    ),
]
