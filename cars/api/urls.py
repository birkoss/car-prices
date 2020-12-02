from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'api/makes',
        api_views.makes.as_view(),
        name='makes'
    ),
    path(
        'api/make/<str:make_slug>',
        api_views.make.as_view(),
        name='make'
    ),
    path(
        'api/make/<str:make_slug>/models',
        api_views.models.as_view(),
        name='models'
    ),
    path(
        'api/make/<str:make_slug>/trims',
        api_views.trims.as_view(),
        name='models'
    ),

    path(
        'api/model/<str:model_id>',
        api_views.model.as_view(),
        name='model'
    ),
    path(
        'api/model/<str:model_id>/trims',
        api_views.trims.as_view(),
        name='trims'
    ),

    path(
        'api/trim/<str:trim_id>',
        api_views.trim.as_view(),
        name='trim'
    ),


]
