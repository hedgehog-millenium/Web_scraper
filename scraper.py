from urllib import request, error, parse ,robotparser
import datetime , time , re, random as rnd


def download(url, user_agent=None,proxy=None , num_retries=2):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    ]

    print('Downloading ', url)
    headers = {'User-agent': user_agent if user_agent else rnd.choice(user_agents)}
    req = request.Request(url, headers=headers)
    opener = request.build_opener()
    if proxy:
        proxy_params = {parse.urlparse(url).scheme: proxy}
    opener.add_handler(request.ProxyHandler(proxy_params))
    try:
        html = request.urlopen(req).read()
    except error.HTTPError as e:
        print('Download error:', e.reason)
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries - 1)
            html = None
    return html


def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1):
    crawl_queue = [seed_url]
    seen = {seed_url: 0}
    rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()

        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url)
            links = []

            depth = seen[url]
            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in link:
                    link = normalize(seed_url, link)
                    if link not in seen:
                        if same_domain(seed_url, link):
                            seen[link] = depth+1
                            crawl_queue.append(link)


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = parse.urldefrag(link) # remove hash to avoid duplicates
    return parse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return parse.urlparse(url1).netloc == parse.urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


class Throttle:
    def __init__(self,delay):
        self.delay = delay
        self.domains = {}

    def wait(self,url):
        domain = parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay>0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now()-last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs) \
 \
        self.domains[domain] = datetime.datetime.now()

