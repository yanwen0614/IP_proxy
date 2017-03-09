import bs4
import requests
import re
from lxml import etree
# 


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
        


    def getHtmlTree(self, url):
        """
        获取html树
        :param url:
        :param kwargs:
        :return:
        """
        html = requests.get(url=url, headers=self.HEADER, timeout=30).content
        return etree.HTML(html)

    def freeProxyFirst(self, page=10):
        """
        抓取快代理IP http://www.kuaidaili.com/
        :param page: 翻页数
        :return:
        """
        url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(page=page) for page in range(1, page + 1))
        # 页数不用太多， 后面的全是历史IP， 可用性不高

        for url in url_list:
            tree = self.getHtmlTree(url)
            proxy_list = tree.xpath('.//div[@id="index_free_list"]//tbody/tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])


    def VaildProxy():
        pass
    
    def DelProxyFromDB():
        pass
    
    def saveProxy():
        pass    

    def saveProxy2DB():
        pass

    def saveProxy2file():
        pass

def main():
    p = proxy()
    for pp in p.freeProxyFirst():
        print(pp)

if __name__ == '__main__':
    main()
