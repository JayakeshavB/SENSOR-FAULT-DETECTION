import pymongo
from sensor_fault_detector.constant.database import DATABASE_NAME
from sensor_fault_detector.constant.env_variable import MONOGODB_URL_KEY
import certifi
import os

ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) ->  None:
        try:
            if MongoDBClient.client is None:
                MongoDBClient.client = pymongo.MongoClient(os.getenv(MONOGODB_URL_KEY), tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e