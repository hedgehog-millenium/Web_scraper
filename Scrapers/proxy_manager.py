from urllib import request, parse
import lxml.html
import re
import time

class ProxyManager:
    __IpApiUrl = 'https://api.ipify.org'

    @classmethod
    def check_proxy(cls, proxy, port, check_timeout_sec=10):
        proxy_str = '%s:%s' % (proxy, port)
        # print(proxy_str)
        proxy_params = {parse.urlparse(cls.__IpApiUrl).scheme: proxy_str}

        try:
            req = request.Request(cls.__IpApiUrl)
            opener = request.build_opener()
            opener.add_handler(request.ProxyHandler(proxy_params))
            req_start_time = time.time()
            resp = opener.open(req, timeout=check_timeout_sec)
            duration = time.time()-req_start_time
            resp_text = resp.read()
            is_secure = proxy in resp_text.decode('utf-8')
            return {'proxy':proxy_str,'visible_ip':resp_text,'alive': True, 'secure': is_secure,'performance':duration}
        except IOError as e:
            # print("Connection error! (Check proxy)")
            return {'proxy':proxy_str,'visible_ip':proxy_str,'alive': False, 'secure': False,'performance':None,'error':e}

    @classmethod
    def check_proxies(cls,proxy_list):
        result = []
        for proxy in proxy_list:
            result.append(ProxyManager.check_proxies(proxy['proxy'],proxy['port']))

        return result
        
    @classmethod
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

    @classmethod
    def get_free_proxy_list_net(cls):
        from Scrapers.downloader import Downloader
        D = Downloader()
        url = 'https://free-proxy-list.net'
        html_string = D.download(url, headers=None, proxy=None, num_retries=1)
        tbl = lxml.html.fromstring(html_string['html']).cssselect('#proxylisttable')
        rows = tbl[0].xpath('tbody/tr')
        proxies = []
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

            proxies.append(proxy)
        filtered_proxies = [p for p in proxies if p['anonymity'] == 'anonymous' and p['https'] == 'yes']
        return filtered_proxies