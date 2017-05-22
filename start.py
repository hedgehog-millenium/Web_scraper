from Callbacks.ScrapeCallback import ScrapeCallback
from Callbacks.alexaCallback import AlexaCallback
from DB.MongoCache import MongoCache
from Scrapers import scraper


# url = 'https://metanit.com/python/tutorial/8.2.php'
# sitemap_url = 'https://metanit.com/sitemap.xml'

seed_url = 'http://example.webscraping.com/index'
link_regex = '/(index|view)'

if __name__ == "__main__":
    # MongoCache().clear()
    scrape_callback = AlexaCallback()
    scraper.link_crawler(seed_url=scrape_callback.seed_url,
                         cache=MongoCache(),
                         scrape_callback=ScrapeCallback() )


