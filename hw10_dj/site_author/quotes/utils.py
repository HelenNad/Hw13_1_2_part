from pymongo import MongoClient


def get_mongodb():
    client = MongoClient('mongodb://localhost')

    db = client.bd_site_authors
    return db
