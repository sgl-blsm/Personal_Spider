# -*- coding: utf-8 -*-
import scrapy
from Personal_Spider.items import SunYunZhuImgItem
from Personal_Spider.settings import DOWNLOADER_MIDDLEWARES


import re


class Taotiao2Spider(scrapy.Spider):
    name = "taotiao2"
    # allowed_domains = ["taotiao.com"] 不要，因其url会跳转到别的域名去

    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES': {
   			'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   			'Personal_Spider.middleware_random_useragent.RandomUserAgentMiddleware': 1000,
        	'Personal_Spider.middleware_taotiao2.Taotiao2AjaxDownloadMiddleware': 1000
        },
        'ITEM_PIPELINES': {
            'Personal_Spider.pipelines.MyImagesPipeline2': 1,
        },      
    }

    def start_requests(self):
    	return [scrapy.Request("http://www.toutiao.com/search/?keyword=孙允珠",
                               meta={'ajax': True},callback=self.parse)]

    def parse(self, response):
    	# 解析response的响应，获取其中的所有article_url
    	article_urls = re.findall(r'<a class="link title" target="_blank" href="(/group/\d+/)">',response.body)
    	print(article_urls)
    	for url in article_urls:
    		url = 'http://www.toutiao.com' + url
    		yield scrapy.Request(url, callback=self.parse_next)

    def parse_next(self, response):
    	# 解析article_url所代表的的详情页，获取所有相关图片链接
    	item = SunYunZhuImgItem()
    	item['image_urls'] = response.xpath('//div[@class="article-content"]//img/@src').extract()
    	item['image_name'] = response.xpath('//h1[@class="article-title"]/text()').extract_first()
    	return item
