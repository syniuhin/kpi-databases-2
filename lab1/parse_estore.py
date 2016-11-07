import urllib2

from lxml import etree

from gen_xml import process_text

BASE_URL = 'http://www.odissey.kiev.ua/'


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


def parse_html(url):
  response = urllib2.urlopen(BASE_URL + url)
  page = response.read()

  tree = etree.HTML(page.decode("cp1251").encode('utf-8'))

  # Set of hardcode hacks
  name = tree.xpath("string(//div[@itemprop='name']/h1/text())")
  price = tree.xpath("string(//div[@id='optionPrice']/text())")
  image = tree.xpath("string(//img[@class='thumbnail']/@src)")
  desc = tree.xpath(
      "//div[@style='overflow-x: auto']/span[@itemprop='description']//text()")

  process_text(desc)
  desc = reduce(lambda a, x: a + x, desc)

  return Product(name, price, desc, BASE_URL + image)


def generate_xml(filename):
  page = urllib2.urlopen(BASE_URL).read()
  tree = etree.HTML(page)
  # Remove duplicates
  urls = set(tree.xpath('//a/@href'))
  urls = filter(lambda x: x.startswith('product'), urls)[:20]
  products = []
  for url in urls:
    products.append(parse_html(url))
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
  et.write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)


generate_xml('products.xml')
