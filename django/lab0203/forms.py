from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.forms import ValidationError

from .models import *


class PhotoForm(forms.ModelForm):

  class Meta:
    model = Photo
    exclude = []
    widgets = {
        'shot_time': DateTimeWidget(
            attrs={'id': 'shot_time'}, usel10n=True, bootstrap_version=3)
    }


class PhotoSearchForm(forms.Form):
  search = forms.CharField(label='Search', max_length=255, required=False)


class CameraAttributesForm(forms.Form):
  date_created_from = forms.DateTimeField(
      label='From',
      required=False,
      widget=DateTimeWidget(
          attrs={'id': 'date_created_from'},
          usel10n=True,
          bootstrap_version=3,
          options={'startView': 2,
                   'minView': 2,
                   'maxView': 4}))
  date_created_to = forms.DateTimeField(
      label='To',
      required=False,
      widget=DateTimeWidget(
          attrs={'id': 'date_created_to'},
          usel10n=True,
          bootstrap_version=3,
          options={'startView': 2,
                   'minView': 2,
                   'maxView': 4}))
  version = forms.IntegerField(label='Version', required=False)


class LocationAttributesForm(forms.Form):
  lat_from = forms.FloatField(label='Latitude from', required=False)
  lng_from = forms.FloatField(label='Longitude from', required=False)
  lat_to = forms.FloatField(label='Latitude to', required=False)
  lng_to = forms.FloatField(label='Longitude to', required=False)
  accessible = forms.BooleanField(label='Accessible', required=False)


class PhotographerAttributesForm(forms.Form):
  level_from = forms.IntegerField(label='Level from', required=False)
  level_to = forms.IntegerField(label='Level to', required=False)
  email_contains = forms.CharField(label='Email contains', required=False)
  have_cameras = forms.ModelMultipleChoiceField(
      label='Have cameras', required=False, queryset=Camera.objects.all())
  have_been_to = forms.ModelMultipleChoiceField(
      label='Have been to', required=False, queryset=Location.objects.all())


class EventIntervalForm(forms.Form):
  interval = forms.CharField(label='Schedule interval', max_length=32)

  def clean(self):
    super(EventIntervalForm, self).clean()
    if 'interval' not in self.cleaned_data:
      raise ValidationError('Please specify an interval!')
    self.cleaned_data['interval'] = self.cleaned_data['interval'].upper()
