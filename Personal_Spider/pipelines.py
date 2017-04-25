# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

import pymysql
import random


class PersonalSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # url格式为 http://mm.howkuai.com/wp-content/uploads/2017a/01/08/02.jpg
        # 将图片的名字变为2017a010802.jpg
        temp = request.url.split('/')[-1:-5:-1]
        temp.reverse()
        image_guid = ''.join(temp)
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class MyImagesPipeline2(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        temp = ''.join(random.sample('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789', random.randrange(4,8)))
        return 'full/%s' % (request.meta['image_name'] + '_' + temp + '.jpg')

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url,meta = {'image_name': item['image_name']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class DoubanbookSpiderPipeline(object):

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='localhost', port=3306, user='root', passwd='root', db='douban', charset='utf8')

    def process_item(self, item, spider):
        # 由于scrapy在spider中抓取的所有字段都会转换成unicode码
        # 所以我们在存入json文件之前先将每一项都转换成utf8
        # 不转的话，我们存入json文件中的数据也是unicode码，中文显示方式不是我们想要的
        # for k in item:
        #     item[k] = item[k].encode("utf8")
        #     print(item[k])
        # return item
        cursor = self.conn.cursor()

        cursor.execute('insert into book(name,score,content_description,link) values(%s,%s,%s,%s)', (item[
                       'name'], item['score'], item['content_description'], item['link']))

        self.conn.commit()
        cursor.close()

    def close_spider(self, spider):
        self.conn.close()
