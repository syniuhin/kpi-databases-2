from __future__ import unicode_literals

from bson.objectid import ObjectId
from django.db import models

from . import mongo_client


class Photo(object):

  @staticmethod
  def all():
    query = mongo_client.photo.photo.find()
    photos = []
    for ph in query:
      ph_id = ph['photographer']
      ph['photographer'] = Photographer.find_by_id(ph_id)
      photos.append(ph)
    return photos

  @staticmethod
  def insert(data):
    # Wrap form data
    if len(data['location']) > 0:
      data['location'] = {"name": data['location']}
    if len(data['camera']) > 0:
      data['camera'] = {"name": data['camera']}
    data = {k: v for k, v in data.items() if v}
    data['photographer'] = ObjectId(data['photographer'])
    mongo_client.photo.photo.insert_one(data)


class Photographer(object):

  @staticmethod
  def find_by_id(ph_id):
    return mongo_client.photo.photographer.find_one({'_id': ph_id})

  @staticmethod
  def choices():
    return [(ph['_id'], ph['name'])
            for ph in mongo_client.photo.photographer.find()]
