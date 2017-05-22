from pymongo import MongoClient
from bs4 import BeautifulSoup

import pickle
import  zlib



url = 'http://testurl.test'
client = MongoClient('localhost',27017)
db = client.cache
# db.webpage.insert({'url':url , 'html': 'html'})
collections = db.webpage.find({})

for record in collections:
    decomp_record = pickle.loads(zlib.decompress(record['result']))
    print(decomp_record)

print("there are %d documents in database"%collections.count())

client.close()