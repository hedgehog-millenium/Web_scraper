import scraper
import re, lxml, lxml.html
import csv


# url = 'https://metanit.com/python/tutorial/8.2.php'
# sitemap_url = 'https://metanit.com/sitemap.xml'

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country',
                       'capital', 'continent', 'tld', 'currency_code',
                       'currency_name', 'phone', 'postal_code_format',
                       'postal_code_regex', 'languages',
                       'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
                self.writer.writerow(row)


seed_url = 'http://example.webscraping.com/index'
link_regex = '/(index|view)'
links = scraper.link_crawler(seed_url, link_regex, max_depth=1, scrape_callback=ScrapeCallback())

print(links)


