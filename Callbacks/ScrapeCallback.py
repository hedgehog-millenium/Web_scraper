import re, lxml, lxml.html
import csv

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))

    def __call__(self, url, html):
        if re.search('/view/', url):
            row = []
            html_rows = lxml.html.fromstring(html).cssselect('tr > td.w2p_fw')
            for r in html_rows:
                row.append(r.text_content())
            self.writer.writerow(row)