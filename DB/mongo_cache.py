from datetime import datetime, timedelta
from pymongo import MongoClient

import pickle
import zlib
from bson.binary import Binary


class MongoCache:
    def __init__(self,collection='webpage', client=None, expires=timedelta(days=5)):
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.cache
        self.collectionName = collection
        self.collection = self.db[collection]
        self.db[collection].create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    def __contains__(self, id):
        try:
            self[id]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, id):
        """Load value at this URL
       """
        record = self.collection.find_one({'_id': id})
        if record:
            return pickle.loads(zlib.decompress(record['data']))
        else:
            raise KeyError(id + ' does not exist')

    def __setitem__(self, id, data):
        """Save value for this URL
        """
        record = {
            'data': Binary(zlib.compress(pickle.dumps(data))),
            'timestamp': datetime.utcnow()
        }
        self.collection.update({'_id': id}, {'$set': record}, upsert=True)

    def clear(self):
        self.collection.drop()
