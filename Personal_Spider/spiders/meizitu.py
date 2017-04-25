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
    1、从首页开始爬取，获取分类信息的url，并返回scrapy.Request()
    2、爬取分类url,获取该分类页的总页数,并返回scrapy.Request()
    3、爬取每一页数据


    http://www.meizitu.com/

    http://www.meizitu.com/a/xinggan.html
            http://www.meizitu.com/a/xinggan_2_3.html
            http://www.meizitu.com/a/xinggan_2_1.html

    http://www.meizitu.com/a/5516.html

    http://mm.howkuai.com/wp-content/uploads/2015a/04/27/01.jpg
    http://mm.howkuai.com/wp-content/uploads/2015a/04/27/05.jpg

'''
import scrapy
from Personal_Spider.items import MeizituItem


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'Personal_Spider.pipelines.MyImagesPipeline': 1,
        },
    }

    start_urls = ['http://www.meizitu.com/']

    def parse(self, response):
        '''解析首页，获取分类的url'''
        img_urls = response.xpath('//div[@class="tags"]//a/@href').extract()
        for url in img_urls:
            yield scrapy.Request(url, callback=self.parse_2)

    def parse_2(self, response):
        '''解析分类页，获取该分类页的总页数，返回对应的url'''
        # page_url 类似 'qingchun_3_8.html' 代表最后一页的地址 其中8即为总页数
        page_url_data = response.xpath(
            '//div[@id="wp_page_numbers"]/ul/li[last()-2]/a/@href').extract_first()
        # 切割page_url 类 'qingchun_3_8.html' --> ['qingchun','3','8']
        temp_list = page_url_data.rstrip('.html').split('_')
        page_url = temp_list[0] + '_' + temp_list[1] + '_'

        for i in range(1, int(temp_list[2]) + 1):
            yield scrapy.Request('http://www.meizitu.com/a/' + page_url + str(i) + '.html', callback=self.parse_3)

    def parse_3(self, response):
        '''解析每一个分类页，返回每一个图片系列页的url'''
        urls = response.xpath(
            '//ul[@class="wp-list clearfix"]//a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_4)

    def parse_4(self, response):
        '''解析图片系列页，返回每一个图片的url'''
        item = MeizituItem()
        item['image_urls'] = response.xpath('//div[@id="picture"]//img/@src').extract()
        return item
