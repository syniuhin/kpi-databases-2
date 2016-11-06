from faker import Faker
from lxml import etree
from lxml.html.clean import clean_html
import random
import urllib2

from . import mongo_client


def generate_data():
  response = urllib2.urlopen(
      'http://events.nationalgeographic.com/speakers-bureau/photographers/')
  page = clean_html(response.read())

  tree = etree.HTML(page.decode('utf-8'))
  names = tree.xpath('//a[@class="titleLink"]/text()')
  photographers = []
  for name in names:
    ns = name.split(' ')
    ph = {
        'name': name,
        'level': random.randint(1, 100),
        'email': ns[0][0].lower() + ns[-1].lower() + '@natgeo.org'
    }
    photographers.append(mongo_client.photo.photographer.insert_one(ph).inserted_id)
  locations = [
      {"name": "Mont Blanc"},
      {"name": "Sahara Desert"},
      {"name": "Kilimanjaro"},
      {"name": "Everest"},
      {"name": "Patagonia Glaciers"},
      {"name": "Elbrus"},
      {"name": "Kabul"},
      {"name": "Ohio"},
  ]
  cameras = [
      {"name": "Nikon D3300", "precision": random.randint(50, 300)/10},
      {"name": "Canon 5D Mark IV", "precision": random.randint(50, 300)/10},
      {"name": "Leica M9", "precision": random.randint(50, 300)/10},
      {"name": "Leica X", "precision": random.randint(50, 300)/10},
      {"name": "Leica T", "precision": random.randint(50, 300)/10},
      {"name": "Pentax K1000", "precision": random.randint(50, 300)/10},
      {"name": "Pentax 645Z", "precision": random.randint(50, 300)/10},
      {"name": "Pentax K1", "precision": random.randint(50, 300)/10},
      {"name": "Hasselblad X1D", "precision": random.randint(50, 300)/10},
      {"name": "Hasselblad H6D", "precision": random.randint(50, 300)/10},
      {"name": "Hasselblad H5X", "precision": random.randint(50, 300)/10},
  ]
  fake = Faker()

  photos = []
  for i in xrange(100000):
    ph = {
      'name': ' '.join(fake.words(nb=2)).capitalize(),
      'photographer': random.choice(photographers),
      'camera': random.choice(cameras),
      'location': random.choice(locations),
      'iso': random.randint(1, 16) * 100,
      'aperture': random.random(),
      'shot_time': fake.date_time().isoformat(),
    }
    photos.append(ph)
  mongo_client.photo.photo.insert_many(photos)
