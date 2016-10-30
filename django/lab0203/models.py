from __future__ import unicode_literals

from django.db import models


class Camera(models.Model):
  name = models.CharField(max_length=64)
  date_created = models.DateField()
  version = models.IntegerField()

  class Meta:
    unique_together = (('name', 'version'),)

  def __str__(self):
    return self.name.encode('utf-8')


class Location(models.Model):
  name = models.CharField(max_length=64, unique=True)
  lat = models.FloatField(max_length=10)
  lng = models.FloatField(max_length=10)
  accessible = models.BooleanField()

  def __str__(self):
    return self.name.encode('utf-8')


class Photographer(models.Model):
  name = models.CharField(max_length=64)
  level = models.IntegerField()
  email = models.EmailField(unique=True)

  cameras = models.ManyToManyField(Camera, blank=True)
  locations = models.ManyToManyField(Location, blank=True)

  def __str__(self):
    return self.name.encode('utf-8')


class Photo(models.Model):
  name = models.CharField(max_length=64)
  aperture = models.FloatField()
  iso = models.IntegerField()
  shot_time = models.DateTimeField()

  camera = models.ForeignKey(Camera)
  location = models.ForeignKey(Location)
  photographer = models.ForeignKey(Photographer, null=True,
                                   on_delete=models.SET_NULL)

  def __str__(self):
    return self.name.encode('utf-8')
