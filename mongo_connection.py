from pymongo import MongoClient
import os

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")


class MongoDBClient:
    def __init__(self, db_name: str) -> None:
        client = MongoClient(MONGO_CONNECTION_STRING)
        self.db = client[db_name]

    def insert_list_to_mongo(self, collection_name: str, to_insert: list) -> None:
        collection = self.db[collection_name]
        collection.insert_many(to_insert)

    def get_objects_from_collection(self, collection_name: str) -> list:
        collection = self.db[collection_name]
        return collection.find()
