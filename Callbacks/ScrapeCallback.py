import re, lxml, lxml.html
import csv


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))

    def __call__(self, url, html):
        if re.search('/view/', url):
            row = []
            html_rows = lxml.html.fromstring(html).xpa('commentViewContent > article > section.containerOuter.blogBodyContainer > section > ul:nth-child(7) > li:nth-child(1)')
            for r in html_rows:
                row.append(r.text_content())
            self.writer.writerow(row)
