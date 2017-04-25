# -*- coding: utf-8 -*-
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



class Taotiao2AjaxDownloadMiddleware(object):
    """对taotiao2这个爬虫，进行selenium操作"""
    def __init__(self):
        super(Taotiao2AjaxDownloadMiddleware, self).__init__()
        self.browser = webdriver.PhantomJS()

    def __del__(self):
        super(Taotiao2AjaxDownloadMiddleware, self).__init__()
        self.browser.quit()

    def process_request(self, request, spider):
        # 只有当目标request中有ajax这个标志时，才使用该中间件
        if request.meta.has_key('ajax'):
            # 1.通过browser来访问url
            self.browser.get(request.url)
            try:
                # 2.点击 图集 这个元素
                element = WebDriverWait(self.browser, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//ul[@class="y-box tab-list"]/li[3]'))
                    )
                element.click()
                # 3.等待元素加载出来
                WebDriverWait(self.browser, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//span[@class="J_title"]'))
                    )
                content = self.browser.page_source.encode('utf-8', 'ignore')

                # 返回响应response后，应该就不会再进行处理吧！应该会直接返回给spider
                return HtmlResponse(request.url, status = 200, body = content)

            except TimeoutException:
                print('还没有加载出来！！')
        else:
            return None
        