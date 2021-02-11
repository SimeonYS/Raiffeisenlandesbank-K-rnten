# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RfkarntenItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()