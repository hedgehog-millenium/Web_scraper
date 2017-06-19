from urllib import request, parse
from Scrapers.downloader import Downloader
import lxml.html
import re
import time
import ssl
from datetime import datetime


class ProxyManager:
    __IpCheckApiUrl = 'https://api.ipify.org'

    def __init__(self, cache=None):
        self.cache = cache
        ssl._create_default_https_context = ssl._create_unverified_context

    def check_proxy(self, proxy, port, check_timeout_sec=10):
        proxy_str = '%s:%s' % (proxy, port)
        result = {}
        if self.cache:
            try:
                result = self.cache[proxy_str]
                print('%s was in cache' % proxy_str)
            except KeyError:
                pass
        if len(result) == 0:
            try:
                proxy_params = {parse.urlparse(self.__IpCheckApiUrl).scheme: proxy_str}
                req = request.Request(self.__IpCheckApiUrl)
                opener = request.build_opener()
                opener.add_handler(request.ProxyHandler(proxy_params))
                req_start_time = time.time()
                resp = opener.open(req, timeout=check_timeout_sec)
                duration = time.time() - req_start_time
                resp_text = resp.read()
                is_secure = proxy in resp_text.decode('utf-8')
                result = {'proxy': proxy_str, 'visible_ip': resp_text, 'alive': True, 'secure': is_secure,
                          'performance': duration,'check_time': datetime.utcnow()}
                if self.cache:
                    self.cache[proxy_str] = result
            except IOError as e:
                # print("Connection error! (Check proxy)")
                result = {'proxy': proxy_str, 'visible_ip': proxy_str, 'alive': False, 'secure': False,
                          'performance': None,
                          'error': e}

        return result

    def get_free_proxy_list_net(self, onlyAnonymous=True, httpsSupport=True):

        proxies = []
        if self.cache:
            try:
                proxies = self.cache['proxylist']
                print('Proxies are found in cache')
            except KeyError:
                pass

        if len(proxies) == 0:
            D = Downloader()
            url = 'https://free-proxy-list.net'
            html_string = D.download(url, headers=None, proxy=None, num_retries=1)
            for p in ProxyManager.extract_proxy_list_net_proxy_fromhtml(html_string):
                proxies.append(p)
            # set proxies to cash
            if self.cache:
                self.cache['proxylist'] = proxies

        if onlyAnonymous:
            proxies = [p for p in proxies if p['anonymity'] == 'anonymous']
        if httpsSupport:
            proxies = [p for p in proxies if p['https'] == 'yes']

        return proxies

    def get_checked_proxy_list(self, count=10, timeout=10):
        proxies = self.get_free_proxy_list_net()
        result = []
        while True:
            proxy = proxies.pop()
            print('checking proxy : %s:%s' % (proxy['proxy'], proxy['port']))
            res = self.check_proxy(proxy['proxy'], proxy['port'], timeout)
            if res['alive'] and res['secure']:
                result.append(res['proxy'])
            print('proxies left: %d , resut proxy amount: %d'%(len(proxies),len(result)))
            if len(result) >= count or len(proxies) == 0:
                break

        return result

    @staticmethod
    def extract_proxy_list_net_proxy_fromhtml(html_string):
        tbl = lxml.html.fromstring(html_string['html']).cssselect('#proxylisttable')
        rows = tbl[0].xpath('tbody/tr')
        for r in rows:
            proxy = {}
            cols = r.xpath('td')
            proxy['proxy'] = cols[0].xpath('string(text())')
            proxy['port'] = cols[1].xpath('string(text())')
            proxy['code'] = cols[2].xpath('string(text())')
            proxy['country'] = cols[3].xpath('string(text())')
            proxy['anonymity'] = cols[4].xpath('string(text())')
            proxy['google'] = cols[5].xpath('string(text())')
            proxy['https'] = cols[6].xpath('string(text())')
            proxy['lastchecked'] = cols[7].xpath('string(text())')

            yield proxy

    @classmethod
    # is not completed
    def get_hide_my_ass_proxy_list(cls):
        url = 'http://proxylist.hidemyass.com/'
        html = request.urlopen(url).read()
        # form = Downloader.parse_form(html)
        html = lxml.html.fromstring(html)
        rows = html.xpath('//table[@id="listable"]/tbody/tr')

        for r in rows:
            cols = r.xpath('td')
            head_span = cols[1].xpath('span')[0]
            style = head_span.xpath('string(style)')
            # nondisp_classes = re.findall('[.](\S*)\{display:none\}',style)
            nondisp_classes = re.findall('[.](\S{4})\{display:none\}', style)
            child_spans = head_span.xpath('span[not(contains(@style,"display:none"))]')
            ip_arr = [sp.xpath('string(text())').replace('.', '') for sp in child_spans if
                      sp.get('class') not in nondisp_classes]
            print(''.join(ip_arr))
