import scraper
import re, lxml, lxml.html
import csv


# url = 'https://metanit.com/python/tutorial/8.2.php'
# sitemap_url = 'https://metanit.com/sitemap.xml'

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))

    def __call__(self, url, html):
        if re.search('/view/', url):
            row = []
            html_rows = lxml.html.fromstring(html).cssselect('tr > td.w2p_fw')
            for r in html_rows :
                row.append(r.text_content())
            self.writer.writerow(row)


seed_url = 'http://example.webscraping.com/index'
link_regex = '/(index|view)'
links = scraper.link_crawler(seed_url, link_regex, max_depth=1, scrape_callback=ScrapeCallback())

print(links)


