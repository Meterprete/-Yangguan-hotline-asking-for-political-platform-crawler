# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient


class YangguangPipeline(object):
    def open_spider(self, spider):
        client = MongoClient()
        self.connect = client['yangguang']['data']
        self.re_complax = re.compile(r'''\xa0|\r|\t|\n|\s''')

    def process_item(self, item, spider):
        item['detail'] = self.data_clear(item['detail'])
        self.connect.insert(dict(item))
        return item

    def data_clear(self, content):
        content = [self.re_complax.sub("", i) for i in content]
        content = [i for i in content if len(i) > 0]
        return content
