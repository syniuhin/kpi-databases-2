from lxml import etree

xslt_root = etree.parse('pattern.xsl')
transorm = etree.XSLT(xslt_root)
xml_root = etree.parse('products.xml')
result_tree = transorm(xml_root)
result = str(result_tree)
with open("products.xhtml", "w") as out:
  out.write(result)
