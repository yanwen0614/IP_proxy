# import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
# import re
from lxml import etree

class proxy(object):
    '''
    proxy
    '''
    def __init__(self):
        self.HEADER = {'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    }

    def getHtmlTree(self, url,  driver=None):
        """
        获取html树
        :param url:
        :param kwargs:
        :return:
        """
        if driver:
            driver.get(url)
            time.sleep(1)
            html = driver.page_source
            return etree.HTML(html)
        else:
            r = requests.get(url, headers=self.HEADER)
            html = r.content
            return etree.HTML(html)
# //*[@id="index_free_list"]/table/tbody
    def freeProxyFirst(self, page=10):
        """
        抓取快代理IP http://www.kuaidaili.com/
        :param page: 翻页数
        :return:
        """
        url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(page=page) for page in range(1, page + 1))
        # 页数不用太多， 后面的全是历史IP， 可用性不高
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = self.HEADER
        driver = webdriver.PhantomJS( desired_capabilities=dcap)
        #driver = webdriver.Chrome() # desired_capabilities=dcap
        for url in url_list:
            tree = self.getHtmlTree(url, driver)
            proxy_list = tree.xpath('.//div[@id="index_free_list"]//tbody/tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])


    def VaildProxy():
        pass
    
    def DelProxyFromDB():
        pass
    
    def saveProxy(IP):

        pass    

    def saveProxy2DB():
        pass

    def saveProxy2file(self, IP):
        now_time = time.ctime()
        now_time = now_time.split()
        now_time = '{year}-{month}-{day}'.format(year=now_time[-1],month=now_time[1],day=now_time[2])
        with open(".\Proxy_Pool\{nowtime}.txt".format(nowtime = now_time),"a") as f:
            f.write(IP+'\n')
        

def main():
    p = proxy()
    for pp in p.freeProxyFirst():
        p.saveProxy2file(pp)

if __name__ == '__main__':
    main()
