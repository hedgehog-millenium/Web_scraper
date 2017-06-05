from pymongo import MongoClient


class MongoManager:
    def __init__(self, host_name='localhost', port=27017):
        self.__dbClient = MongoClient(host_name, port)

    def GetAllDbs(self):
        return self.__dbClient.database_names()

    def GetAllCollections(self, db_name):
        return self.__dbClient[db_name].collection_names()

    def FindAll(self, db_name,collection_name):
        db = self.__dbClient[db_name]
        return db[collection_name].find({})

    def Find(self, db_name,collection_name,predicate):
        db = self.__dbClient[db_name]
        return db[collection_name].find(predicate)

    def Insert(self, db_name, collection_name,obj):
        db = self.__dbClient[db_name]
        return db[collection_name].insert(obj)

    def Update_one(self, db_name, collection_name,predicatie,obj):
        db = self.__dbClient[db_name]
        return db[collection_name].update_one(predicatie,obj)

    def __del__(self):
        self.__dbClient.close()
