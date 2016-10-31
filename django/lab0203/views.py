from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from .forms import PhotoForm
from .models import Aggregator, Photo, Photographer


def index(request):
  return HttpResponseRedirect('/photo/list')


class PhotoController(object):

  @staticmethod
  def create(request):
    if request.method == 'GET':
      form = PhotoForm()
    elif request.method == 'POST':
      form = PhotoForm(request.POST)
      if form.is_valid():
        Photo.insert(form.cleaned_data)
        return HttpResponseRedirect('/photo/list/')
    return render(request, 'photo/form.html', {'form': form,
                                               'action_url': '/photo/create'})

  @staticmethod
  def update(request, photo_id):
    photo = Photo.form_instance(photo_id)
    if request.method == 'GET':
      form = PhotoForm(photo)
    elif request.method == 'POST':
      form = PhotoForm(request.POST)
      if form.is_valid():
        Photo.update(photo_id, form.cleaned_data)
        return HttpResponseRedirect('/photo/list/')
    return render(request, 'photo/form.html',
                  {'form': form,
                   'action_url': '/photo/' + photo_id + '/update'})

  @staticmethod
  def clicked(request):
    if request.method == 'POST':
      print request.POST
      if 'editbtn' in request.POST:
        url = reverse(
            'update_photo', kwargs={'photo_id': request.POST['tableradio']})
        return HttpResponseRedirect(url)
      if 'deletebtn' in request.POST:
        url = reverse(
            'delete_photo', kwargs={'photo_id': request.POST['tableradio']})
        return HttpResponseRedirect(url)
    return HttpResponseBadRequest()

  @staticmethod
  def delete(request, photo_id):
    Photo.delete(photo_id)
    return HttpResponseRedirect('/photo/list/')


class PhotoListView(ListView):
  template_name = 'photo/list.html'

  def get_queryset(self):
    return Photo.all()


class PAListView(ListView):
  template_name = 'photo/pa.html'

  def get_queryset(self):
    return Aggregator.photographer_mean_aperture()


class PPListView(ListView):
  template_name = 'photo/pp.html'

  def get_queryset(self):
    return Aggregator.photographer_shots_count()


class AggregateListView(ListView):
  template_name = 'photo/trusted_cameras.html'

  def get_queryset(self):
    return Aggregator.popular_trusted_cameras()
