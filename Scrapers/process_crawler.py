import time
import threading
import multiprocessing
from DB.mongo_queue import MongoQueue
from DB.mongo_cache import MongoCache
from Scrapers.downloader import Downloader
from urllib import parse
import re

SLEEP_TIME = 1


def threaded_crawler(seed_url, delay=5, link_regex=None, scrape_callback=None, user_agent=None, proxies=None,
                     num_retries=1, max_threads=10, timeout=60):
    """Crawl using multiple threads
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = MongoQueue()
    crawl_queue.push(seed_url)
    crawl_queue.clear()
    cache = MongoCache()
    print(seed_url)
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries,
                   timeout=timeout)

    def process_queue():
        while True:
            # keep track that are processing url
            try:
                url = crawl_queue.pop()
                print('Module:process_queue , URL:', url)
            except KeyError:
                # currently no urls to process
                break
            else:
                html = D(url)
                links = []
                if link_regex:
                    # filter for links matching our regular expression
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))
                if scrape_callback:
                    try:
                        links.extend(scrape_callback(url, html) or [])
                    except Exception as e:
                        print('Error in callback for: {}: {}'.format(url, e))
                    else:
                        for link in links:
                            # add this new link to queue
                            crawl_queue.push(normalize(seed_url, link))

                crawl_queue.complete(url)

    # wait for all download threads to finish
    threads = []
    while threads or crawl_queue:
        print('treads count: ',len(threads))
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)


def process_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print('Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = parse.urldefrag(link)  # remove hash to avoid duplicates
    return parse.urljoin(seed_url, link)


def get_links(html):
    """Return a list of links from html 
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    st = str(html)

    return webpage_regex.findall(st)
