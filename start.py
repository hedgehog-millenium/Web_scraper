from Callbacks.ScrapeCallback import ScrapeCallback
from DB.MongoCache import MongoCache
from Scrapers import scraper

# url = 'https://metanit.com/python/tutorial/8.2.php'
# sitemap_url = 'https://metanit.com/sitemap.xml'

seed_url = 'http://example.webscraping.com/index'
link_regex = '/(index|view)'

if __name__ == "__main__":
    # MongoCache().clear()
    scraper.link_crawler(seed_url, link_regex, max_depth=1, scrape_callback=ScrapeCallback(), cache=MongoCache())