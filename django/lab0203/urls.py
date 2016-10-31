from django.conf.urls import url

from . import views
from .views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^photographer/list/filter/?$',
    #     FilterPhotographerListView.as_view(),
    #     name='photographer_list_filter'),
    url(r'^photo/clicked/?$',
        views.PhotoController.clicked,
        name='on_click_photo'),
    url(r'^photo/create/?$', views.PhotoController.create, name='new_photo'),
    url(r'^photo/(?P<photo_id>.*)/update/?$',
        views.PhotoController.update,
        name='update_photo'),
    url(r'^photo/delete/(?P<photo_id>.*)/?$',
        views.PhotoController.delete,
        name='delete_photo'),
    url(r'^photo/list/?$', PhotoListView.as_view(), name='photo_list'),
    # url(r'^photo/list/filter/?$',
    #     FilterPhotoListView.as_view(),
    #     name='photo_list_filter'),
]
