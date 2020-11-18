from datetime import datetime
import pymongo
import logging

# TODO: put it on another file (settings.py)

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "reddit_worldnews"

SETTINGS = {
    "MONGODB_SERVER": MONGODB_SERVER,
    "MONGODB_PORT": MONGODB_PORT,
    "MONGODB_DB": MONGODB_DB,
}

DATE_FORMAT = DATE = datetime.now().date().isoformat().replace('-', '')


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            SETTINGS['MONGODB_SERVER'],
            SETTINGS['MONGODB_PORT'],
        )
        db = connection[SETTINGS['MONGODB_DB']]
        self.collection = db[SETTINGS['MONGODB_DB']+DATE]

    def process_item(self, docs):
        valid = True
        for data in docs:
            if not data:
                valid = False
                raise ValueError("Missing {0}!".format(data))

        if valid:
            self.collection.insert_many(docs)
            logging.debug("Posts added to MongoDB database!")
        return docs
