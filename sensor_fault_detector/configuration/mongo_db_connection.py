import pymongo
from sensor_fault_detector.constant.database import DATABASE_NAME
import certifi

ca = certifi.where()

class MongoDBClient(object):
    client = None
    def __init__(self, database_name=DATABASE_NAME) ->  None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = "mongodb+srv://sensor_fault_db:keshav10807%40B@cluster0.ozs3za5.mongodb.net/?retryWrites=true&w=majority"
                self.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e

