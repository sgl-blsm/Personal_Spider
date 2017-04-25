# -*- coding: utf-8 -*-
'''ToutiaoSpider:抓取今日头条（http://www.toutiao.com）里通过关键字搜索后出现的内容
		如，搜索孙允珠---http://www.toutiao.com/search/?keyword=孙允珠，要求获取相关页的所有图片
   分析发现，该url的响应HTML中并没有相关的内容，
		发现所需内容是通过ajax请求服务器、加载到HTML文档上的
			--http://www.toutiao.com/search_content/?offset=0&format=json&keyword=孙允珠&autoload=true&count=20&cur_tab=1
			分析发现该url是可以得到所需内容的
			    --http://www.toutiao.com/search_content/?offset=0&format=json&keyword=孙允珠
				其响应是json数据，里面含有具体详情页的地址
					article_url:"http://toutiao.com/group/6410489529144606978/"
						详情页里的图片的链接都是在HTML文档里的
				其是通过ajax加载分页数据的，第二页 offset=20

			发现article_url有的指向图片列表页，类似http://toutiao.com/group/6410489529144606978/，
					有的会跳往第三方页，其内容都是视频，可以不管它
			大概爬到offset=140就差不多了，后面就没有内容了

	http://www.toutiao.com/search_content/?offset=0&format=json&keyword=孙允珠
	http://www.toutiao.com/search_content/?offset=140&format=json&keyword=孙允珠

		---> article_url:"http://toutiao.com/group/6410489529144606978/"

			--> 爬对应的HTML，找到图片的链接，并下载图片
'''
import scrapy
from Personal_Spider.items import SunYunZhuImgItem

import re


class ToutiaoSpider(scrapy.Spider):
    name = "toutiao"
    allowed_domains = ["toutiao.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'Personal_Spider.pipelines.MyImagesPipeline2': 1,
        },
    }

    key = '孙允珠'
    offset = 140

    start_urls = ['http://www.toutiao.com/search_content/?offset=%d&format=json&keyword=孙允珠' %
                  i for i in range(0, offset, 20)]

    def parse(self, response):
    	# 解析response的响应，其是json字符串，获取其中的所有article_url
    	article_urls = re.findall(r'"article_url": "(http://toutiao\.com/group/\d+/)"',response.body)
    	for url in article_urls:
    		yield scrapy.Request(url, callback=self.parse_next)

    def parse_next(self, response):
    	# 解析article_url所代表的的详情页，获取所有相关图片链接
    	item = SunYunZhuImgItem()
    	item['image_urls'] = response.xpath('//div[@class="article-content"]//img/@src').extract()
    	item['image_name'] = response.xpath('//h1[@class="article-title"]/text()').extract_first()
    	return item

    	

