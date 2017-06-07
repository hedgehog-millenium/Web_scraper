from urllib import request, parse
import lxml.html
from lxml.etree import XPath

class ProxyManager:
    __IpApiUrl = 'https://api.ipify.org'

    @classmethod
    def check_proxy(cls):
        proxy = '63.150.152.151:8080'
        proxy_params = {parse.urlparse(cls.__IpApiUrl).scheme: proxy}

        try:
            req = request.Request(cls.__IpApiUrl)
            opener = request.build_opener()
            opener.add_handler(request.ProxyHandler(proxy_params))
            resp = opener.open(req, timeout=10)
            print(resp.read())
        except IOError:
            print("Connection error! (Check proxy)")
        else:
            print("All was fine")

    @classmethod
    def get_proxy_list(cls):
        import re
        url = 'http://proxylist.hidemyass.com/'
        html = request.urlopen(url).read()
        # form = Downloader.parse_form(html)
        html = lxml.html.fromstring(html)
        tbl = html.xpath('//table[@id="listable"]')[0]
        rows = tbl.xpath('//tr[@class="altshade"]')
        for r in rows:
            cols = r.xpath('td')
            spans = cols[1].xpath('span')
            ip = [s for s in spans]
            print(ip)
            # port = re.findall(r'\d+',lxml.etree.tostring(cols[2]).decode('utf-8'))[0]
            # print(proxy)
            # print(lxml.etree.tostring(cols[1]))

