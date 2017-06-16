import lxml.html


class policeamCallback:
    def __int__(self):
        pass

    def __call__(self, url,html):
        # print('Url in callback %s' % url)
        print(html)
        # root = lxml.html.fromstring(html)
        # links = root.xpath('//a')
        # for l in links:
        #     print(l.xpath('text()'))