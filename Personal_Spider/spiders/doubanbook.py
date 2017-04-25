# -*- coding: utf-8 -*-
'''DoubanbookSpider:爬取豆瓣读书某个种类的图书信息
        1、书籍列表页翻页规律：r"https://book.douban.com/tag/编程\?start=\d+&type=T"
                第一页:https://book.douban.com/tag/心理学?start=0&type=T
                第二页:https://book.douban.com/tag/心理学?start=20&type=T
                第三页:https://book.douban.com/tag/心理学?start=40&type=T
        2、书籍详情页url规律:链接都类似，r "http://book.douban.com/subject/\d+/$"
                https://book.douban.com/subject/26805083/
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Personal_Spider.items import DoubanBookItem


class DoubanbookSpider(CrawlSpider):
    name = 'doubanbook'
    allowed_domains = ['douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Personal_Spider.pipelines.DoubanbookSpiderPipeline': 1,
        },
    }

    category = '编程'
    start_urls = ['https://book.douban.com/tag/%s?start=0&type=T' % category]

    rules = (
        # 列表页url
        Rule(LinkExtractor(allow=(r"https://book.douban.com/tag/编程\?start=\d+&type=T"))),
        # 详情页url
        Rule(LinkExtractor(allow=(r"https://book.douban.com/subject/\d+/$")),
             callback="parse_item"),
    )

    def parse_item(self, response):

        item = DoubanBookItem()

        # 图书名
        item["name"] = response.xpath(
            "//div[@id='wrapper']/h1/span/text()").extract()[0].strip()
        # 读者评分
        item["score"] = response.xpath(
            "//div[@class='rating_self clearfix']/strong/text()").extract()[0].strip()
        # 详情页链接
        item["link"] = response.url
        # 内容简介
        try:
            contents = response.xpath(
                "//div[@id='link-report']//div[@class='intro']")[-1].xpath(".//p//text()").extract()
            item["content_description"] = "\n".join(content for content in contents)
        except:
            item["content_description"] = ""

        return item
