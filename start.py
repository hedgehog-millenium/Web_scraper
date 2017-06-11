from Scrapers.scraper import link_crawler
from Callbacks.CareercenterCallback import careeercenterCalback
from Callbacks.policeAmCallback import policeamCallback
from DB.mongo_cache import MongoCache
from DB.mongo import MongoManager
from datetime import timedelta
from Scrapers.proxy_manager import ProxyManager



def printDb():
    # Print All Dbs and Collections
    dbMgr = MongoManager()
    dbs = dbMgr.GetAllDbs()
    for db in dbs:
        print(db)
        cols = dbMgr.GetAllCollections(db)
        for col in cols:
            print('\t',col)

    # Select All Objects
    objs = dbMgr.FindAll('cache','crawl_queue')
    for o in objs:
        print(o)

    # Select Single
    print('----------------')
    pred = {'_id':{'$regex': 'http://chat.*'} }
    curs = dbMgr.Find('cache','crawl_queue',pred)
    for doc in curs:
        print(doc)

if __name__ == "__main__":
    # url = 'https://careercenter.am/ccidxann.php'
    # regex_pat = '.*ccdspann\.php\?id=d*'

    url = 'http://www.police.am/Cucakner'
    regex_pat = '.*d{1,3}/'
    proxyCache = MongoCache(collection='proxies',client=None,expires=timedelta(minutes=10))
    prxMgr = ProxyManager(cache=proxyCache)
    proxies = prxMgr.get_checked_proxy_list(5)
    link_crawler(seed_url=url,link_regex=regex_pat,delay=0,scrape_callback=policeamCallback(),cache=MongoCache(),proxies=proxies)

    # printDb()

