from Scrapers.scraper import link_crawler
from Callbacks.CareercenterCallback import careeercenterCalback
import re

# url = 'https://metanit.com/python/tutorial/8.2.php'
# sitemap_url = 'https://metanit.com/sitemap.xml'

# seed_url = 'http://example.webscraping.com/index'
# link_regex = '/(index|view)'

url = 'https://careercenter.am/ccidxann.php'


if __name__ == "__main__":
    regex_pat = '.*ccdspann\.php\?id=d*'
    link_crawler(seed_url=url,link_regex=regex_pat,delay=0,scrape_callback=careeercenterCalback())



