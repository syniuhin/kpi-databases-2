<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Products</h2>
    <table border="1">
      <tr bgcolor="#666666">
        <th style="text-align:left">Имя</th>
        <th style="text-align:left">Цена</th>
        <th style="text-align:left">Описание</th>
        <th style="text-align:left">Картинка</th>
      </tr>
      <xsl:for-each select="data/product">
      <tr>
        <td><xsl:value-of select="name"/></td>
        <td><xsl:value-of select="price"/></td>
        <td><xsl:value-of select="description"/></td>
        <td><img><xsl:attribute name="src"><xsl:value-of select="image"/></xsl:attribute></img></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>