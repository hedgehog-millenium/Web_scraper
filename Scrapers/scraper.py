import re
import queue
from urllib import parse, robotparser
from Scrapers.throttle import Throttle
from Scrapers.downloader import Downloader


def link_crawler(seed_url, link_regex=None, delay=1, max_depth=-1, max_urls=-1, user_agent=None,
                 proxies=None, num_retries=1, scrape_callback=None, cache=None, ignore_robots=True, check_domain=True):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = queue.deque([seed_url])
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    if not ignore_robots:
        rp = get_robots(seed_url)
    throttle = Throttle(delay)

    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)
    user_agent = D.user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        # check url passes robots.txt restrictions
        if not ignore_robots and not rp.can_fetch(user_agent, url):
            print('Blocked by robots.txt:', url)
            continue

        throttle.wait(url)
        html = D(url)
        links = []

        if scrape_callback:
            links.extend(scrape_callback(url, html) or [])

        if depth != max_depth:
            # can still crawl further
            if link_regex:
                # filter for links matching our regular expression
                links.extend(link for link in get_links(html) if re.match(link_regex, link))

            for link in links:
                link = normalize(seed_url, link)
                # check whether already crawled this link
                if link not in seen:
                    seen[link] = depth + 1
                    # check link is within same domain
                    if check_domain and not same_domain(seed_url, link):
                        continue

                    crawl_queue.append(link)

        # check whether have reached downloaded maximum
        num_urls += 1
        if num_urls == max_urls:
            break


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = parse.urldefrag(link)  # remove hash to avoid duplicates
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
    """Return a list of links from html 
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    st = str(html)

    return webpage_regex.findall(st)

