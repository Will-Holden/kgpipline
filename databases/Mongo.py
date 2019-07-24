import sys
sys.path.append(".")
import pymongo
from settings import MONGO_HOST, MONGO_PORT, MONGO_DB
from core.Singleton import Singleton

class Mongo(metaclass=Singleton):
    def __init__(self, ip=MONGO_HOST, port=MONGO_PORT, db=MONGO_DB):
        self.client = pymongo.MongoClient("mongodb://{0}:{1}/".format(ip, port))
        self.db = db

    def insert(self, doc, db, table):
        self.client[db][table].insert(doc, continue_on_error=True)

    def update(self, spec, doc, db, table):
        self.client[db][table].update_one(spec, {"$set": doc})

    def delete(self, query_cond, db, table):
        self.client[db][table].delete_many(query_cond)

    def query(self, query_cond, db, table, projection=None, skip=None, limit=None):
        if query_cond is None or query_cond == {}:
            if skip is None:
                query_result = self.client[db][table].find(projection=projection)
            else:
                query_result = self.client[db][table].find(projection=projection).skip(skip).limit(limit)
        else:
            if skip is None:
                query_result = self.client[db][table].find(query_cond, projection=projection)
            else:
                query_result = self.client[db][table].find(query_cond, projection=projection).skip(skip).limit(limit)
        x = [doc for doc in query_result]
        return x

    def query_sort(self, query_cond, table, db, sort_by='', ascending=-1, page=1,
                   size=10):
        skip = (page - 1) * size
        if query_cond is None or query_cond == {}:
            query_result = self.client[db][table].find().sort(sort_by, ascending).skip(skip).limit(size)
        else:
            query_result = self.client[db][table].find(query_cond).sort(sort_by, ascending).skip(skip).limit(size)
        x = [doc for doc in query_result]
        return x

    def count_tag(self, tag_column, db, table, limit=10, cond=None):
        if cond == None:
            query_result = self.client[db][table].aggregate([{"$unwind": "${0}".format(tag_column)},
                                                             {"$group": {"_id": "${0}".format(tag_column),
                                                                         "num": {"$sum": 1}}},
                                                             {"$project": {"_id": 0, tag_column: "$_id", "num": 1}},
                                                             {"$sort": {"num": -1}}])
        else:
            query_result = self.client[db][table].aggregate([{"$match": cond},
                                                             {"$unwind": "${0}".format(tag_column)},
                                                             {"$group": {"_id": "${0}".format(tag_column),
                                                                         "num": {"$sum": 1}}},
                                                             {"$project": {"_id": 0, tag_column: "$_id", "num": 1}},
                                                             {"$sort": {"num": -1}}])
        x = [doc for doc in query_result]
        return x

    def count_column_with_cond(self, cond, column_name, db, table):
        query_result = self.client[db][table].aggregate([
            {"$match": cond},
            {"$group": {
                "_id": "${0}".format(column_name),
                "num": {"$sum": 1}}},
            {"$project": {"_id": 0, column_name: "$_id", "num": 1}},
            {"$sort": {"num": -1}}])
        x = [doc for doc in query_result]
        return x

    def remove_dul(self, dul_col, db, table):
        dul_ids = self.client[db][table].aggregate([
            {"$group": {
                "_d_id": {"$min": '$_id'},
                "_id": {"id": "${0}".format(dul_col)},
                "num": {"$sum": 1},
            }},
            {"$match": {
                "num": {"$gt": 1}
            }}
            # {"$project": {"_id": 0, dul_col: "$_id", "num": 1}}
        ])
        x = [data for data in dul_ids]
        return x


if __name__ == '__main__':
    ms = Mongo()
    import time

    a = time.time()

    data = mgService.query({"schoolName": "武汉大学"},
                           'kb_demo',
                           'kb_academy')
    print(data)

    print(time.time() - a)
