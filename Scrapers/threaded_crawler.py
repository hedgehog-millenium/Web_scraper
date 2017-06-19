import time
import threading
from urllib import parse
from Scrapers.downloader import Downloader
from DB.mongo_queue import MongoQueue
from DB.mongo_cache import MongoCache

SLEEP_TIME = 1


def threaded_crawler(seed_url, delay=5, scrape_callback=None, user_agent=None, proxies=None, num_retries=1,
                     max_threads=10, timeout=60):
    """Crawl this website in multiple threads
    """

    crawl_queue = MongoQueue()
    crawl_queue.push(seed_url)
    cache = MongoCache()
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except KeyError:
                # currently no urls to process
                break
            else:
                html = D(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {}: {}'.format(url, e))
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            crawl_queue.complete(link)


    # wait for all download threads to finish
    threads = []
    while threads or crawl_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True) # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = parse.urldefrag(link) # remove hash to avoid duplicates
    return parse.urljoin(seed_url, link)