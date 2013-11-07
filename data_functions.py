import pymongo
from pymongo import MongoClient

def initialize_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bluecoat-stats-db']
    coll = db.userstats
    return coll

def get_stats(coll=initialize_connection(), filter=dict(), limit=None):
    if limit != None:
        cur = coll.find().sort('data-usage', -1).limit(limit)
    else:
        cur = coll.find().sort('data-usage', -1)
    result = []
    for i in cur:
        result.append(i)
    return result