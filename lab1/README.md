# Лабораторна робота #1

## Завдання
1. Виконати збір інформації зі сторінок Web-сайту за варіантом.
2. Виконати аналіз сторінок Web-сайту для подальшої обробки текстової та
графічної інформації, розміщеної на ньому.
3. Реалізувати функціональні можливості згідно вимог, наведених нижче.

### Варіант
14ий. Для 3ього завдання обран 16 через проблеми із аналізом сайту магазина львівських меблів.

## Фрагменти коду
Парсер сторінок для 1ого та 2ого завдання:
```{python}
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
```
Генератор дерева для 2ого завдання:
```{python}
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
```
Фрагмент дерева:
```{xml}
<data>
  <page url="http://www.stejka.com">
    <fragment type="text">Stejka - туристический портал Украины. Путешествия, достопримечательности, отели, гостиницы, рестораны, такси.</fragment>
    <!--...-->
    <fragment type="image">http://www.stejka.com/i/best.png</fragment>
  </page>
  <page url="http://www.stejka.com/rus/jitomirskaja/">
    <!--...-->
  </page>
  <!--...-->
</data>
```
