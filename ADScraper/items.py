# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ADItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    zh_data_manual = scrapy.Field()
    en_data_manual = scrapy.Field()
    user_manual = scrapy.Field()
