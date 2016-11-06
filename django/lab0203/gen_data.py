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
  for name in names:
    ns = name.split(' ')
    ph = {
        'name': name,
        'level': random.randint(1, 100),
        'email': ns[0][0].lower() + ns[-1].lower() + '@natgeo.org'
    }
    mongo_client.photo.photographer.insert(ph)