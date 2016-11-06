from __future__ import unicode_literals

from bson import json_util
from bson.code import Code
from bson.objectid import ObjectId
from bson.son import SON
from django.db import models
import redis

from . import mongo_client


redis_instance = redis.StrictRedis()
page_size = 30

class Photo(object):

  @staticmethod
  def all():
    query = mongo_client.photo.photo.find()
    photos = []
    for ph in query:
      photos.append(Photo._prepare_for_view(ph))
    return photos

  @staticmethod
  def page(i):
    redis_key = 'page: %d' % i
    paged_data = redis_instance.get(redis_key)
    if paged_data:
      return json_util.loads(paged_data)
    query = mongo_client.photo.photo.aggregate([
        {"$sort": SON([("_id", 1)])},
        {"$skip": i * page_size},
        {"$limit": page_size},
    ])
    photos = []
    for ph in query:
      photos.append(Photo._prepare_for_view(ph))
    redis_instance.set(redis_key, json_util.dumps(photos))
    return photos

  @staticmethod
  def search(search_query, page=0):
    redis_key = 'search: %s page: %d' % (search_query, page)
    cached_res = redis_instance.get(redis_key)
    if cached_res:
      return json_util.loads(cached_res)
    # TODO: Page search results
    query = mongo_client.photo.photo.aggregate([
        {"$match": {"$text": {"$search": search_query}}},
        {"$sort": SON([("_id", 1)])},
        {"$skip": page * page_size},
        {"$limit": page_size},
    ])
    photos = []
    for ph in query:
      photos.append(Photo._prepare_for_view(ph))
    redis_instance.set(redis_key, json_util.dumps(photos))
    return photos

  @staticmethod
  def form_instance(str_id):
    instance = mongo_client.photo.photo.find_one({'_id': ObjectId(str_id)})
    if instance:
      instance = Photo._prepare_for_form(instance)
    return instance

  @staticmethod
  def insert(data):
    data = Photo._prepare_for_insert(data)
    mongo_client.photo.photo.insert_one(data)
    # TODO: Think about smarter way to invalidate appropriate cache
    for k in redis_instance.keys('search:*'):
      redis_instance.delete(k)

  @staticmethod
  def update(str_id, data):
    data = Photo._prepare_for_update(data)
    mongo_client.photo.photo.update_one({'_id': ObjectId(str_id)},
                                        {"$set": data})
    # TODO: Think about smarter way to invalidate appropriate cache
    redis_instance.flushall()

  @staticmethod
  def delete(str_id):
    mongo_client.photo.photo.delete_one({'_id': ObjectId(str_id)})
    # TODO: Think about deleting by pattern in keys
    redis_instance.flushall()

  @staticmethod
  def _prepare_for_view(ph):
    ph['id'] = ph['_id']
    ph_id = ph['photographer']
    ph['photographer'] = Photographer.find_by_id(ph_id)
    return ph

  @staticmethod
  def _prepare_for_form(instance):
    ph = Photographer.find_by_id(instance['photographer'])
    instance['photographer'] = ph['_id']
    if 'camera' in instance and instance['camera']:
      instance['camera'] = instance['camera']['name']
    if 'location' in instance and instance['location']:
      instance['location'] = instance['location']['name']
    return instance

  @staticmethod
  def _prepare_for_insert(data):
    # Wrap form data
    if len(data['location']) > 0:
      data['location'] = {"name": data['location']}
    if len(data['camera']) > 0:
      data['camera'] = {"name": data['camera']}
    data = {k: v for k, v in data.items() if v}
    data['photographer'] = ObjectId(data['photographer'])
    return data

  @staticmethod
  def _prepare_for_update(data):
    if len(data['location']) > 0:
      data['location.name'] = data['location']
    del data['location']
    if len(data['camera']) > 0:
      data['camera.name'] = data['camera']
    del data['camera']
    data = {k: v for k, v in data.items() if v}
    data['photographer'] = ObjectId(data['photographer'])
    return data


class Photographer(object):

  @staticmethod
  def find_by_id(ph_id):
    return mongo_client.photo.photographer.find_one({'_id': ph_id})

  @staticmethod
  def choices():
    return [(ph['_id'], ph['name'])
            for ph in mongo_client.photo.photographer.find()]


class Aggregator(object):

  @staticmethod
  def photographer_mean_aperture():
    mapper = Code("""
      function() {
        if ("aperture" in this) {
          emit(this.photographer, this.aperture);
        }
      }
    """)
    reducer = Code("""
      function(k, vs) {
        return Array.sum(vs) / vs.length;
      }
    """)
    raw = mongo_client.photo.photo.map_reduce(mapper, reducer,
                                              "photographer_aps").find()
    res = []
    for kv in raw:
      res.append({'name': Photographer.find_by_id(kv['_id'])['name'],
                  'mean': kv['value']})
    return res

  @staticmethod
  def photographer_shots_count():
    mapper = Code("""
      function() {
        emit(this.photographer, 1);
      }
    """)
    reducer = Code("""
      function(k, vs) {
        return Array.sum(vs);
      }
    """)
    raw = mongo_client.photo.photo.map_reduce(mapper, reducer,
                                              "photographer_phs").find()
    res = []
    for kv in raw:
      res.append({'name': Photographer.find_by_id(kv['_id'])['name'],
                  'count': kv['value']})
    return res

  @staticmethod
  def popular_trusted_cameras():
    pipeline = [
      { "$group": { "_id" : "$photographer", "cameras": {"$addToSet": "$camera"} } },
      { "$project": { "_id": 1, "cameras": 1, "ccount": { "$gt" : [ { "$size" : "$cameras" }, 1 ] } } },
      { "$match": { "ccount" : True } },
      { "$unwind": "$cameras" },
      { "$group": { "_id": "$cameras", "phs": {"$addToSet": "$_id"} } },
      { "$project": { "_id": 1, "phs": 1, "phcount": {"$size": "$phs"} } },
      { "$sort": SON([("phcount", -1), ("_id.name", 1)]) }
    ]
    agg = list(mongo_client.photo.photo.aggregate(pipeline))
    for obj in agg:
      obj['name'] = obj['_id']['name']
      obj['count'] = obj['phcount']
    return agg
