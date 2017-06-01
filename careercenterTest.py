import lxml.html
from Scrapers.downloader import Downloader
import re


def work_with_jobdict(desc_dict):
    for k in desc_dict:
        print(k)

    while(True):
        inp = input('pls type the key u want to select from dic   ')
        try:
            print('-------------RESULT--------------')
            print(desc_dict[inp])
            print('---------------------------')
        except:
            break


def clear_key(key):
    return key.replace(':', '').replace(' ', '_').replace('/', '').strip()


def clear_text(text):
    clean_text = text.strip()
    # clear usicode spec chars
    return re.sub(r'[^\x00-\x7F]+', '', clean_text)


def get_job_dict_from_html(html):
    h = lxml.html.fromstring(html)
    desc_dict = {}

    print(h.cssselect('p>b'))
    # print(h.cssselect('table>tr> td:nth-child(2) > font > b')[0].text)
    desc_dict['COMPANY'] =  h.xpath('//body/p[1]/font/b/text()') or h.xpath('//body/table/tbody/tr/td[2]/font/b/text()')
    for p in h.xpath('//p'):
        try:
            key = clear_key(p.xpath('b/text()')[0])
            desc_dict[key] = clear_text(p.xpath('text()')[0])
        except:
            pass
    return desc_dict


def save_to_json(desc_dict):
    import json
    js = json.dumps(desc_dict)

    with open('parsed_jobs/jobjson.json','w') as f:
        f.write(js)

    return js



if __name__ == "__main__":
    # scrape_callback = AlexaCallback()
    # max_threads = 10
    # process_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback,  max_threads=max_threads,timeout=10)
    # url = 'https://careercenter.am/ccdspann.php?id=28188'
    url = 'https://careercenter.am/index.php?/ccdspann.php?id=28465'
    d = Downloader()
    res = d(url=url)

    desc_dict = get_job_dict_from_html(res)
    # work_with_jobdict(desc_dict)

    # js = save_to_json(desc_dict)
    # print(js)


