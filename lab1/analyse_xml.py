from lxml import etree

tree = etree.parse('pages.xml')
pages = tree.xpath("/data/page")

for page in pages:
  hyperlinks = page.xpath("fragment[@type='a']/text()")
  print "List for %s" % page.xpath("@url")
  for l in hyperlinks:
    print "\t" + l