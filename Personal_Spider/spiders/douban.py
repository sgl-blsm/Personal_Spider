# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    custom_settings = {
    	'COOKIES_ENABLED': True
    }

    def start_requests(self):
    	return [scrapy.Request('https://accounts.douban.com/login',callback = self.login,
    							meta = {'cookiejar':1})]

    def login(self, response):
    	# 命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        
        captcha_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        # captcha_id = response.xpath('//div[@class="captcha_block"]/input[2]/@value').extract_first()
        # 该字段会由 FormRequest.from_response() 自动处理

        if captcha_url:
        	print('需要输入验证码！！')
        	print(captcha_url)
        	# print(captcha_id)
        	captcha_value = raw_input()
        	formdata = {
        	    # 'redir':'https://www.douban.com/',  可以设置登录后跳转的url 默认跳转到https://www.douban.com
				'form_email':'651069858@qq.com',
				'form_password':'2shang5guan',
				'captcha-solution': captcha_value,
				'redir':'https://www.douban.com/people/160588178/', # 跳转到个人主页
        	}
        else:
        	print('不需要输入验证码！！')

        	formdata = {
				'redir':'https://www.douban.com/people/160588178/', # 跳转到个人主页
				'form_email':'651069858@qq.com',
				'form_password':'2shang5guan',
        	}

        temp = scrapy.FormRequest.from_response(response,formdata = formdata,
        							meta = {'cookiejar':response.meta['cookiejar']},
        							callback = self.login_after)
        # print(temp.body)
        return temp

    def login_after(self, response):

    	site_title = response.xpath('/html/head/title/text()').extract_first()
    	print(site_title)
