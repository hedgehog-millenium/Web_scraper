from datetime import datetime, timedelta
from pymongo import MongoClient

import pickle
import zlib
from bson.binary import Binary

from DB.mongo import MongoManager


class MongoCache:
    def __init__(self, collection='webpage', client=None, expires=timedelta(days=30), useCompression=True):
        self.useCompression = useCompression
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.cache
        self.collectionName = collection
        self.collection = self.db[collection]
        self.collection.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

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
            return MongoCache.decompress(record['data']) if self.useCompression else record['data']
        else:
            raise KeyError(id + ' does not exist')

    def __setitem__(self, id, data):
        """Save value for this URL
        """
        record = {
            'data': MongoCache.compress(data) if self.useCompression else data,
            'timestamp': datetime.utcnow()
        }
        self.collection.update({'_id': id}, {'$set': record}, upsert=True)

    def getAll(self):
        records = []
        all_caches = self.collection.find({})
        for c in all_caches:
            rec = MongoCache.decompress(c['data']) if self.useCompression else c['data']
            records.append(rec)
        return records

    def clear(self):
        self.collection.drop()

    @staticmethod
    def compress(data):
        return Binary(zlib.compress(pickle.dumps(data)))

    @staticmethod
    def decompress(data):
        return pickle.loads(zlib.decompress(data))
