from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'api/make/<str:make_slug>/prices',
        api_views.make.as_view(),
        name='make-prices'
    ),
    path(
        'api/trim/<str:trim_id>/prices',
        api_views.prices.as_view(),
        name='trim-prices'
    ),
    path(
        'api/trim/<str:trim_id>/prices/pending',
        api_views.prices_pending.as_view(),
        name='trim-prices-pending'
    ),
    path(
        'api/trim/<str:trim_id>/price/<str:price_type>',  # nopep8
        api_views.trim_type.as_view(),
        name='trim-price-type'
    ),
]
