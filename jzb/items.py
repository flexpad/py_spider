# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JZBTopicItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    tid = scrapy.Field()
    uid = scrapy.Field()
    reply = scrapy.Field()
    pass
class JZBPostItem(scrapy.Item):
    userinfo = scrapy.Field()
    userurl = scrapy.Field()
    posttime = scrapy.Field()
    lou = scrapy.Field()
    post = scrapy.Field()
    title = scrapy.Field()
    louzhu = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
