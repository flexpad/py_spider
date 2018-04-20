# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re

from jzb.items import JZBTopicItem, JZBPostItem
class JZBPipeline(object):
    collection_topic = 'jzb_topic'
    collection_post = 'jzb_post'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 写入json文件
        if isinstance(item, JZBTopicItem):
            self.db[self.collection_topic].insert_one(dict(item))
            pass
        elif isinstance(item, JZBPostItem):
            print("yield: ", item, "\n")
            base_url = './public/'
            for image in item['images']:
                pattern = re.compile('/\w+/\w/\d+_\d+(?=_\d+.png)')
                urls = re.findall (pattern, image['url'])
                item['post'] = re.sub(urls[0] + "_\d+.\w+", base_url + image['path'], item['post'])
                # item['post'] = item['post'].replace(urls[0] + '_\d+.png', base_url + image['path'] )
            self.db[self.collection_post].insert_one(dict(item))
            pass
        return item
