from Callbacks.ScrapeCallback import ScrapeCallback
from Callbacks.alexaCallback import AlexaCallback
from Scrapers.process_crawler import process_crawler


# url = 'https://metanit.com/python/tutorial/8.2.php'
# sitemap_url = 'https://metanit.com/sitemap.xml'

seed_url = 'http://example.webscraping.com/index'
link_regex = '/(index|view)'

if __name__ == "__main__":
    scrape_callback = AlexaCallback()
    max_threads = 10
    process_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback,  max_threads=max_threads,
                    timeout=10)






