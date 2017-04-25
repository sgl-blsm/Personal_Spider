#-*-coding:utf-8-*-
 
import random
 
class ProxyIPMiddleware(object):
    
    def process_request(self, request, spider):
        pro_adr = random.choice(self.proxyList)
        print "USE PROXY ---------------------------> "+pro_adr
        request.meta['proxy'] = "http://"+ pro_adr
        print request.meta['proxy']


    proxyList = ['36.250.69.4:80', '58.18.52.168:3128', '58.253.238.243:80', 
                 '60.191.164.22:3128', '60.191.167.93:3128']
        
'''
这里用的免费代理,不用用户名密码的.如果有用户名和密码,还要加入以下代码
    proxy_user_pass = "USERNAME:PASSWORD"
    encoded_user_pass = base64.encodestring(proxy_user_pass)
    request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
'''
