from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, QueryDict
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
import urllib

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
    querystr = request.META['QUERY_STRING']
    page_num = 0
    if len(querystr) > 0:
      self.querydict = QueryDict(querystr)
      if 'q' in self.querydict:
        self.form = self.get_form_class()(self.querydict)
      if 'page' in self.querydict:
        page_num = self.querydict['page']
    if not hasattr(self, 'form'):
      self.form = self.get_form(self.get_form_class())

    # From BaseListView
    self.object_list = self.get_queryset()
    context = self.get_context_data(
        object_list=self.object_list, form=self.form)
    if 'page_id' in kwargs:
      page_num = kwargs['page_id']
    context['page_num'] = page_num
    return self.render_to_response(context)

  def post(self, request):
    # From ProcessFormMixin
    self.form = self.get_form_class()(request.POST)
    if self.form.is_valid():
      url = reverse('photo_search') + '?' + urllib.urlencode(
          {'q': self.form.cleaned_data['search'],
           'page': 0})
      return HttpResponseRedirect(url)

    # From BaseListView
    self.object_list = self.get_queryset()
    context = self.get_context_data(
        object_list=self.object_list, form=self.form)
    return self.render_to_response(context)

  def get_queryset(self):
    if hasattr(self, 'querydict'):
      search = self.querydict.get('q') if 'q' in self.querydict else ''
      page = int(self.querydict.get('page')) if 'page' in self.querydict else 0
      return Photo.search(search, page)
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
