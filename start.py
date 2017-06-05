from Scrapers.scraper import link_crawler
from Callbacks.CareercenterCallback import careeercenterCalback
from DB.mongo_cache import MongoCache
from DB.mongo import MongoManager

url = 'https://careercenter.am/ccidxann.php'


if __name__ == "__main__":
    regex_pat = '.*ccdspann\.php\?id=d*'
    link_crawler(seed_url=url,link_regex=regex_pat,delay=0,scrape_callback=careeercenterCalback(),cache=MongoCache())

    # Print All Dbs and Collections
    # dbs = dbMgr.GetAllDbs()
    # for db in dbs:
    #     print(db)
    #     cols = dbMgr.GetAllCollections(db)
    #     for col in cols:
    #         print('\t',col)
    #
    # # Select All Objects
    # objs = dbMgr.FindAll('cache','crawl_queue')
    # for o in objs:
    #     print(o)
    #
    # # Select Single
    # print('----------------')
    # pred = {'_id':{'$regex': 'http://chat.*'} }
    # curs = dbMgr.Find('cache','crawl_queue',pred)
    # for doc in curs:
    #     print(doc)
    #
