# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


class IsbnItem(scrapy.Item):
    # define the fields for your item here like:
    isbn = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    publish = scrapy.Field()


class IsbnLoader(ItemLoader):
    ItemLoader.default_item_class = IsbnItem
    default_output_processor = TakeFirst()
