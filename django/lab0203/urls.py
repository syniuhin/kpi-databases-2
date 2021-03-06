from django.conf.urls import url

from . import views
from .views import AggregateListView, PhotoController, PhotoListView, PAListView, PPListView

urlpatterns = [
    url(r'^$', views.index, name='index'),
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
    url(r'^photo/list/(?P<page_id>\d*)/?$', PhotoListView.as_view(), name='photo_list'),
    url(r'^photo/list/search/?$', PhotoListView.as_view(), name='photo_search'),
    url(r'^camera/trusted/?$', AggregateListView.as_view(), name='tc_list'),
    url(r'^photographer/apertures/?$', PAListView.as_view(), name='pa_list'),
    url(r'^photographer/shots/?$', PPListView.as_view(), name='pp_list'),
]
