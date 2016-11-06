from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.forms import ValidationError

from .models import Photo, Photographer


class PhotoForm(forms.Form):
  name = forms.CharField(label='Name', required=True)
  aperture = forms.FloatField(label='Aperture', required=False)
  iso = forms.IntegerField(label='ISO', required=False)
  camera = forms.CharField(label='Camera', required=False)
  location = forms.CharField(label='Location', required=False)
  photographer = forms.ChoiceField(
      label='Photographer', choices=Photographer.choices)
  shot_time = forms.DateTimeField(widget=DateTimeWidget(
      attrs={'id': 'shot_time'}, usel10n=True, bootstrap_version=3))


class PhotoSearchForm(forms.Form):
  search = forms.CharField(label='Search', max_length=255, required=False)
  page = forms.IntegerField(label='Page', min_value=0, required=False)
