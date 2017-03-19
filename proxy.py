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
        self.HEADER = {
                        'Connection': 'keep-alive',
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
            print(url)
            tree = self.getHtmlTree(url, driver)
            proxy_list = tree.xpath('.//div[@id="index_free_list"]//tbody/tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    def freeProxySecond(proxy_number=100):
        """
        抓取代理66 http://www.66ip.cn/
        :param proxy_number: 代理数量
        :return:
        """
        url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(proxy_number)
        html = requests.get(url, headers=HEADER).content
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    def VaildProxy(self,IP):
        proxies = {
                    "http": "http://{0}".format(IP),
                    "https": "http://{0}".format(IP),
                    }
        try:
            r = requests.get('https://www.baidu.com/', proxies=proxies, timeout=30, verify=False)
            if r.status_code == 200:
                return True
            else:
                return False
        except Exception:
            return False
    
    def DelProxyFromDB():
        pass

    def saveProxy2DB(self, IP):
        pass

    def saveProxy2file(self, IP):
        now_time = time.ctime()
        now_time = now_time.split()
        now_time = '{year}-{month}-{day}'.format(year=now_time[-1],month=now_time[1],day=now_time[2])
        with open(".\Proxy_Pool\{nowtime}.txt".format(nowtime = now_time),"a") as f:
            f.write(IP+'\n')
            #print(IP+'\n')


def main():
    p = proxy()
    for pp in p.freeProxyFirst(10):
        if p.VaildProxy(pp):
            print(pp+'  pass')
            p.saveProxy2file(pp)
        else:
            print(pp+'  refuse')

if __name__ == '__main__':
    main()
