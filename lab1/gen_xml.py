from lxml import etree
from lxml.html.clean import clean_html
import urllib2

BASE_URL = 'http://www.stejka.com'


def process_text(text_lst):
  text_lst = map(lambda x: ' '.join(x.split()),
                 text_lst)  # remove two+ tabulation chars
  text_lst = filter(lambda x: len(x) > 2,
                    text_lst)  # get words with two and more chars
  return text_lst


def process_images(images):
  return map(lambda img: img if img.startswith("http") else BASE_URL + img,
             images)


def process_urls(urls):
  urls = list(set(urls))
  urls = filter(lambda x: len(x) > 3 and x[0] == "/", urls)
  urls = map(lambda x: BASE_URL + x, urls)
  return urls


def parse_html(url):
  response = urllib2.urlopen(url)
  page = response.read()
  page = clean_html(page)

  tree = etree.HTML(page.decode('utf-8'))

  text = tree.xpath('//text()')
  text = process_text(text)

  images = tree.xpath('//img/@src')
  images = process_images(images)

  urls = tree.xpath('//a/@href')
  urls = process_urls(urls)

  return urls, text, images


def generate_xml_page(page_url, urls, text, images):
  page_elem = etree.Element("page", url=page_url)

  for elem in text:
    fragment = etree.Element("fragment", type="text")
    fragment.text = elem
    page_elem.append(fragment)

  for url in urls:
    fragment = etree.Element("fragment", type="a")
    fragment.text = url
    page_elem.append(fragment)

  for img in images:
    fragment = etree.Element("fragment", type="image")
    fragment.text = img
    page_elem.append(fragment)

  return page_elem


def generate_xml(filename):
  root = etree.Element("data")

  urls, _, _ = parse_html(BASE_URL)
  urls.insert(0, BASE_URL)
  urls = urls[:20]

  for url in urls:
    urls, text, images = parse_html(url)
    page_elem = generate_xml_page(url, urls, text, images)
    root.append(page_elem)

  et = etree.ElementTree(root)
  et.write(filename, encoding="utf-8", xml_declaration=True, pretty_print=True)


generate_xml("pages.xml")