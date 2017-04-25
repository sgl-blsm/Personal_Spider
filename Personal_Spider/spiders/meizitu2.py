# -*- coding: utf-8 -*-
'''MeizituSpider:爬取妹子图网站整站的图片
网站结构分析：
        首页---http://www.meizitu.com/，里面含有图片的所有分类信息
        某一分类---http://www.meizitu.com/a/xinggan.html，里面多页的数据
                第三页---http://www.meizitu.com/a/xinggan_2_3.html
                第一页---http://www.meizitu.com/a/xinggan_2_1.html
        每一页都有很多图片，这些图片是一个系列图片的第一个图片，点击会进入到该系列页面
                某一个系列---http://www.meizitu.com/a/5516.html
                （分类列表页有很多子元素，每个元素都是一个系列相关的图片）
        该系列页面有很多该系列的图片  
爬取策略：

    首页（起始页）--- http://www.meizitu.com/

    分类页----------- http://www.meizitu.com/a/xinggan.html 
           --> r'http://www.meizitu.com/a/[a-z]+\.html'
            
    分类页的所有页---- http://www.meizitu.com/a/xinggan_2_3.html
                       http://www.meizitu.com/a/xinggan_2_1.html
                --> r'http://www.meizitu.com/a/[a-z]+_\d+_\d+\.html'

    分类页的详情页---- http://www.meizitu.com/a/5516.html 
              --> r'http://www.meizitu.com/a/\d+.html'
              
     图片的url---http://mm.howkuai.com/wp-content/uploads/2015a/04/27/01.jpg              
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Personal_Spider.items import MeizituItem


class Meizitu2Spider(CrawlSpider):
    name = 'meizitu2'
    allowed_domains = ['meizitu.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Personal_Spider.pipelines.MyImagesPipeline': 1,
        },
    }
    start_urls = ['http://www.meizitu.com/']

    rules = (
        # 分类页url
        Rule(LinkExtractor(allow=(r'http://www.meizitu.com/a/[a-z]+\.html'))),
        # 分类页的所有页url
        Rule(LinkExtractor(allow=(r'http://www.meizitu.com/a/[a-z]+_\d+_\d+\.html'))),
        # 分类页上的详情页url
        Rule(LinkExtractor(allow=(r'http://www.meizitu.com/a/\d+\.html')),callback="parse_item"),
    )

    def parse_item(self, response):
        '''解析图片系列页，返回每一个图片的url'''
        item = MeizituItem()
        item['image_urls'] = response.xpath('//div[@id="picture"]//img/@src').extract()
        return item
