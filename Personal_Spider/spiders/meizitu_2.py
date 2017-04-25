# -*- coding: utf-8 -*-
'''meizitu_1、meizitu_2为scrapy分布式爬虫
		Meizitu1Spider:用来爬取meizitu.com的所有分类页(所有页)的链接
		Meizitu2Spider:用来爬取分类页的图片详情页里的图片的链接
'''
import scrapy
from scrapy_redis.spiders import RedisSpider

from Personal_Spider.items import MeizituItem


class Meizitu2Spider(RedisSpider):
    name = "meizitu_2"
    allowed_domains = ["meizitu.com"]

    redis_key = 'meizituspider:page_urls'

    custom_settings = {
        'ITEM_PIPELINES': {
            'Personal_Spider.pipelines.MyImagesPipeline': 1,
        },
    }

    def parse(self, response):
        '''解析每一个分类页，返回每一个图片系列页的url'''
        urls = response.xpath(
            '//ul[@class="wp-list clearfix"]//a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_2)

    def parse_2(self, response):
        '''解析图片系列页，返回每一个图片的url'''
        item = MeizituItem()
        item['image_urls'] = response.xpath('//div[@id="picture"]//img/@src').extract()
        return item
