# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PersonalSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MeizituItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class SunYunZhuImgItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()


class DoubanBookItem(scrapy.Item):
    name = scrapy.Field()                       # 书名   
    score = scrapy.Field()                      # 读者评分  
    content_description = scrapy.Field()        # 内容简介  
    link = scrapy.Field()                       # 详情页链接  