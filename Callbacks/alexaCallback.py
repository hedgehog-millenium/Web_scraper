from zipfile import ZipFile
from io import BytesIO
import csv
import codecs


class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
        with ZipFile(BytesIO(html)) as zf:
            csv_filename = zf.namelist()[0]
            data = codecs.iterdecode(zf.open(csv_filename), 'utf-8')
            for _, website in csv.reader(data):
                urls.append('http://' + website)
                if len(urls) == self.max_urls:
                    break
        return urls
