import os
from pymongo import MongoClient


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')


def get_db(name, mongo_url=MONGODB_URI, retry_writes='true'):
    client = MongoClient(f'{mongo_url}?retryWrites={retry_writes}')
    db = client[name]
    return db
