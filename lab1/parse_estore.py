import urllib2

from lxml import etree

from gen_xml import process_text

BASE_URL = 'http://mebli-lviv.com.ua'
HEADERS = {'User-Agent': 'Chrome 54.0.2840.71'}


class Product:

  def __init__(self, name, price, description, image):
    self.name = name
    self.price = price
    self.description = description
    self.image = image

  def __str__(self):
    return self.name.encode('utf-8')

  def __repr__(self):
    return self.name.encode('utf-8')


def parse_table(url):
  request = urllib2.Request(url, headers=HEADERS)
  page = urllib2.urlopen(request).read()

  tree = etree.HTML(page.decode("cp1251").encode('utf-8'))

  products = []
  tds = tree.xpath("//td")
  duvans = filter(
      lambda duvan: len(duvan.xpath("h3/a/@href")) > 0 and duvan.xpath("h3/a/@href")[0].startswith('duvan_'),
      tds)
  for duvan in duvans:
    name = duvan.xpath("h3/a/text()")
    price = duvan.xpath("//div[@class='image_title']/text()")
    desc = '-'  #TODO: Parse it from the subpage.
    image = duvan.xpath("//img/@src")
    products.append(Product(name, price, desc, image))
  return products


def parse_product(url):
  print "Parsing product for %s" % url
  request = urllib2.Request(url, headers=HEADERS)
  page = urllib2.urlopen(request).read()

  tree = etree.HTML(page.decode("cp1251").encode('utf-8'))
  name = tree.xpath("//h1/text()")
  price = tree.xpath("//span[@class='price_main']/big/b/text()")
  image_sources = tree.xpath("//img[@id='image_src']/@src")
  print image_sources
  image = filter(
      lambda src: src.startswith('http://mebli-lviv.com.ua/makethumb.php?pic'),
      image_sources)[0]
  desc = 'BULLSHIT'  #tree.xpath(
  #"//div[@style='overflow-x: auto']/span[@itemprop='description']//text()")

  #process_text(desc)
  #desc = reduce(lambda a, x: a + x, desc)
  return Product(name, price, desc, image)


def generate_xml(filename):
  products = parse_table(BASE_URL + '/dyvanu_pryami')

  root = etree.Element("data")

  for product in products:
    product_el = etree.Element("product")

    name_el = etree.Element("name")
    name_el.text = product.name

    price_el = etree.Element("price")
    price_el.text = product.price

    desc_el = etree.Element("description")
    desc_el.text = product.description

    image_el = etree.Element("image")
    image_el.text = product.image

    product_el.append(name_el)
    product_el.append(price_el)
    product_el.append(desc_el)
    product_el.append(image_el)

    root.append(product_el)

  et = etree.ElementTree(root)
  et.write(filename, encoding="utf-8", xml_declaration=True, pretty_print=True)


generate_xml("products.xml")
