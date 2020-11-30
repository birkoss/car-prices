from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'api/make/<str:make>/prices',
        api_views.make.as_view(),
        name='make-prices'
    ),
    path(
        'api/make/<str:make>/model/<str:model>/trim/<str:trim>/prices',
        api_views.trim.as_view(),
        name='trim-prices'
    ),
    path(
        'api/make/<str:make>/model/<str:model>/trim/<str:trim>/price/<str:price_type>',  # nopep8
        api_views.trim_type.as_view(),
        name='trim-price-type'
    ),
]