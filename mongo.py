from pymongo import MongoClient


url = 'http://testurl.test'
client = MongoClient('localhost',27017)
db = client.cache
# db.webpage.insert({'url':url , 'html': 'html'})
collections = db.webpage.find({})

for col in collections:
    print(col)

print("there are %d documents in database"%collections.count())

client.close()