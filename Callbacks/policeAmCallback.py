<<<<<<< HEAD
import lxml.html

=======
import lxml
import lxml.html
from urllib import parse
>>>>>>> d54afd3186cf17aa9113fc09b623aa9238a64566

class policeamCallback:
    def __int__(self):
        pass

    def __call__(self, url,html):
<<<<<<< HEAD
        # print('Url in callback %s' % url)
        print(html)
        # root = lxml.html.fromstring(html)
        # links = root.xpath('//a')
        # for l in links:
        #     print(l.xpath('text()'))
=======
        doc = lxml.html.fromstring(html)
        links = doc.xpath('//a')
        for a in links:
            part = a.get('href')
            fin_url = parse.urljoin(url,part)
            print(fin_url)
>>>>>>> d54afd3186cf17aa9113fc09b623aa9238a64566
