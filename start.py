from Callbacks.ScrapeCallback import ScrapeCallback
from Callbacks.alexaCallback import AlexaCallback
from DB.MongoCache import MongoCache
from Scrapers import scraper,threaded_crawler


# url = 'https://metanit.com/python/tutorial/8.2.php'
# sitemap_url = 'https://metanit.com/sitemap.xml'

seed_url = 'http://example.webscraping.com/index'
link_regex = '/(index|view)'

if __name__ == "__main__":
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    max_threads = 10
    threaded_crawler.threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, max_threads=max_threads, timeout=10)

    # scraper.threaded_crawler(seed_url=scrape_callback.seed_url,
    #                      cache=cache,
    #                      scrape_callback=scrape_callback,
    #                      ignore_robots=True,
    #                      check_domain=False)




