from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from .forms import *
from .models import *


def index(request):
  return HttpResponseRedirect('/photo/list')


class PhotoController:

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

# class FormListView(FormMixin, ListView):
#   def get(self, request, *args, **kwargs):
#     # From ProcessFormMixin
#     form_class = self.get_form_class()
#     self.form = self.get_form(form_class)

#     # From BaseListView
#     self.object_list = self.get_queryset()
#     allow_empty = self.get_allow_empty()
#     if not allow_empty and len(self.object_list) == 0:
#       raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
#                     % {'class_name': self.__class__.__name__})

#     context = self.get_context_data(object_list=self.object_list,
#                                     form=self.form)
#     return self.render_to_response(context)

#   def post(self, request):
#     # From ProcessFormMixin
#     self.form = self.get_form_class()(request.POST)
#     if self.form.is_valid():
#       self.cleaned_data = self.form.cleaned_data

#     # From BaseListView
#     self.object_list = self.get_queryset()
#     allow_empty = self.get_allow_empty()
#     if not allow_empty and len(self.object_list) == 0:
#       raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
#                     % {'class_name': self.__class__.__name__})

#     context = self.get_context_data(object_list=self.object_list,
#                                     form=self.form)
#     return self.render_to_response(context)

# class FilterCameraListView(FormListView):
#   form_class = CameraAttributesForm
#   template_name = 'camera/list_filtered.html'

#   def get_queryset(self):
#     if hasattr(self, 'cleaned_data'):
#       date_created_from = self.cleaned_data.get('date_created_from')
#       date_created_to = self.cleaned_data.get('date_created_to')
#       version = self.cleaned_data.get('version')
#       q = Q()
#       if date_created_from is not None:
#         q = q & Q(date_created__gte=date_created_from.date())
#       if date_created_to is not None:
#         q = q & Q(date_created__lte=date_created_to.date())
#       if version is not None:
#         q = q & Q(version=version)
#       queryset = Camera.objects.filter(q)
#     else:
#       queryset = Camera.objects.all()
#     return zip(queryset, [db.camera_usage(q.id) for q in queryset])

# class FilterLocationListView(FormListView):
#   form_class = LocationAttributesForm
#   template_name = 'location/list_filtered.html'

#   def get_queryset(self):
#     if hasattr(self, 'cleaned_data'):
#       lat_from = self.cleaned_data.get('lat_from')
#       lng_from = self.cleaned_data.get('lng_from')

#       lat_to = self.cleaned_data.get('lat_to')
#       lng_to = self.cleaned_data.get('lng_to')

#       accessible = self.cleaned_data.get('accessible')
#       q = Q()
#       if lat_from is not None:
#         q = q & Q(lat__gte=lat_from)
#       if lng_from is not None:
#         q = q & Q(lng__gte=lng_from)
#       if lat_to is not None:
#         q = q & Q(lat__lte=lat_to)
#       if lng_to is not None:
#         q = q & Q(lng__lte=lng_to)
#       q = q & Q(accessible=accessible)
#       return Location.objects.filter(q)
#     return Location.objects.all()

# class FilterPhotographerListView(FormListView):
#   form_class = PhotographerAttributesForm
#   template_name = 'photographer/list_filtered.html'

#   def get_queryset(self):
#     if hasattr(self, 'cleaned_data'):
#       level_from = self.cleaned_data.get('level_from')
#       level_to = self.cleaned_data.get('level_to')
#       email_contains = self.cleaned_data.get('email_contains')
#       have_cameras = self.cleaned_data.get('have_cameras')
#       have_been_to = self.cleaned_data.get('have_been_to')

#       q = Q()
#       if level_from is not None:
#         q &= Q(level__gte=level_from)
#       if level_to is not None:
#         q &= Q(level__lte=level_to)
#       if email_contains is not None:
#         q &= Q(email__contains=email_contains)
#       if len(have_cameras) > 0:
#         q &= Q(cameras__in=have_cameras)
#       if len(have_been_to) > 0:
#         q &= Q(locations__in=have_been_to)
#       return Photographer.objects.filter(q)
#     return Photographer.objects.all()

# class FilterPhotoListView(FormListView):
#   form_class = PhotoSearchForm
#   template_name = 'photo/list_filtered.html'

#   def get_queryset(self):
#     if hasattr(self, 'cleaned_data'):
#       search = self.cleaned_data.get('search')
#       return Photo.objects.filter(Q(name__contains=search) |
#                                   Q(aperture__contains=search) |
#                                   Q(iso__contains=search) |
#                                   Q(shot_time__contains=search) |
#                                   Q(photographer__name__contains=search) |
#                                   Q(location__name__contains=search) |
#                                   Q(camera__name__contains=search))
#     return Photo.objects.all()
