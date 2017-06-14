import lxml
import lxml.html
from urllib import parse

class policeamCallback:
    def __int__(self):
        pass

    def __call__(self, url,html):
        doc = lxml.html.fromstring(html)
        links = doc.xpath('//a')
        for a in links:
            part = a.get('href')
            fin_url = parse.urljoin(url,part)
            print(fin_url)