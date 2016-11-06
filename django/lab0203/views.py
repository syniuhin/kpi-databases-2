from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from .forms import PhotoForm, PhotoSearchForm
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


class PhotoListView(FormMixin, ListView):
  template_name = 'photo/list.html'
  form_class = PhotoSearchForm

  def get(self, request, *args, **kwargs):
    # From ProcessFormMixin
    form_class = self.get_form_class()
    self.form = self.get_form(form_class)

    # From BaseListView
    self.object_list = self.get_queryset()
    allow_empty = self.get_allow_empty()
    if not allow_empty and len(self.object_list) == 0:
      raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False." %
                    {'class_name': self.__class__.__name__})

    context = self.get_context_data(
        object_list=self.object_list, form=self.form)
    context['page_num'] = kwargs['page_id']
    return self.render_to_response(context)

  def post(self, request):
    # From ProcessFormMixin
    self.form = self.get_form_class()(request.POST)
    if self.form.is_valid():
      self.cleaned_data = self.form.cleaned_data

    # From BaseListView
    self.object_list = self.get_queryset()
    allow_empty = self.get_allow_empty()
    if not allow_empty and len(self.object_list) == 0:
      raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False." %
                    {'class_name': self.__class__.__name__})

    context = self.get_context_data(
        object_list=self.object_list, form=self.form)
    return self.render_to_response(context)

  def get_queryset(self):
    if hasattr(self, 'cleaned_data'):
      search = self.cleaned_data.get('search')
      return Photo.search(search)
    return Photo.page(
        int(self.kwargs['page_id']) if len(self.kwargs['page_id']) > 0 else 0)


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
