import random
import socket
from urllib import request, parse ,error
from Scrapers.throttle import Throttle


class Downloader:
    __user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    ]

    __DEFAULT_AGENT = random.choice(__user_agents)
    __DEFAULT_DELAY = 5
    __DEFAULT_RETRIES = 1
    __DEFAULT_TIMEOUT = 60

    def __init__(self, delay=__DEFAULT_DELAY, user_agent=None, proxies=None, num_retries=__DEFAULT_RETRIES,
                 timeout=__DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent if not'None' else self.__DEFAULT_AGENT
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
                print('Url: %s found in cache' % url)
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignore result from cache and re-download
                    result = None
        if result is None:
            # result was not loaded from cache so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        print('Downloading:', url)
        if 'User-agent' not in headers.keys():
            headers['User-agent'] = random.choice(self.__user_agents)

        req = request.Request(url, data, headers or {})
        opener = self.opener or request.build_opener()
        if proxy:
            proxy_params = {parse.urlparse(url).scheme: proxy}
            opener.add_handler(request.ProxyHandler(proxy_params))
        try:
            response = opener.open(req)
            html = response.read()
            code = response.code
        except Exception as e:
            print('Download error:', str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # retry 5XX HTTP errors
                    return self.download(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {'html': html, 'code': code}
