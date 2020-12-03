from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'api/make/<str:make_slug>/prices',
        api_views.make.as_view(),
        name='make-prices'
    ),
    path(
        'api/model/<str:model_id>/prices',
        api_views.models.as_view(),
        name='model-prices'
    ),
    path(
        'api/trim/<str:trim_id>/prices',
        api_views.prices.as_view(),
        name='trim-prices'
    ),
]
