import lxml.html
import re
from urllib import parse
import os
from os.path import isfile, join
from Scrapers.downloader import Downloader


class policeamCallback:
    def __init__(self,proxies=None):
        self.xls_patt = '.*\d{0,2}_\d{0,2}.xls$'
        self.path_name = 'C:\\Users\\Samvel.Kocharyan\\Desktop\\reg_files'
        self.files_in_folder = [f for f in os.listdir(self.path_name) if isfile(join(self.path_name, f))]
        self.__downloader = Downloader()
        self.__proxies = proxies if not None else []
        pass

    xls_links = []

    def __call__(self, url, html):
        if re.match(self.xls_patt, url):
            self.saveFile(url, html)
        else:
            try:
                root = lxml.html.fromstring(html)
                links = root.xpath('//a')
                new_links = []
                for l in links:
                    link = l.xpath('text()')[0]
                    if re.match(self.xls_patt , link):
                        fine_link = parse.urljoin(url, link)
                        self.xls_links.append(fine_link)
                        new_links.append(fine_link)
                return new_links
            except Exception as e:
                print('problem with url: ',url)
                print(e)

    def saveFile(self, url,html):
        if html:
            xls_name = re.findall('\d{0,2}_\d{0,2}.xls$', url)[0]
            if xls_name not in self.files_in_folder:
                fin_path = os.path.join(self.path_name,xls_name)
                with open(fin_path, 'wb') as f:
                    f.write(html)
                    print('File successfully saved . name: ', fin_path)
            else:
                print(xls_name, ' file is already in folder :', self.path_name)
        else:
            print('Empty html for url: ',url)
