# -*- coding: utf-8 -*-
'''meizitu_1、meizitu_2为scrapy分布式爬虫
		Meizitu1Spider:用来爬取meizitu.com的所有分类页(所有页)的链接
                            start_urls = 'http://www.meizitu.com'
		Meizitu2Spider:用来爬取分类页的图片详情页里的图片的链接
'''
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider
import redis


class Meizitu1Spider(RedisCrawlSpider):
    name = "meizitu_1"
    allowed_domains = ["meizitu.com"]

    redis_key = 'meizituspider:start_urls'

    rules = (
        # 分类页url
        Rule(LinkExtractor(allow=(r'http://www.meizitu.com/a/[a-z]+\.html')),callback="parse_item"),
    )

    def parse_item(self, response):
        '''解析分类页，获取该分类页的总页数，返回对应的url'''
        # print(self.server.get('a'))  self.server代表该spider链接的redis的实例

        # page_url 类似 'qingchun_3_8.html' 代表最后一页的地址 其中8即为总页数
        page_url_data = response.xpath(
            '//div[@id="wp_page_numbers"]/ul/li[last()-2]/a/@href').extract_first()
        # 切割page_url, 'qingchun_3_8.html' --> ['qingchun','3','8']
        temp_list = page_url_data.rstrip('.html').split('_')
        page_url = temp_list[0] + '_' + temp_list[1] + '_'

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        pipe = r.pipeline(transaction=True)
        for i in range(1, int(temp_list[2]) + 1):
        	url = 'http://www.meizitu.com/a/' + page_url + str(i) + '.html'
        	r.lpush('meizituspider:page_urls', url)
        pipe.execute()

