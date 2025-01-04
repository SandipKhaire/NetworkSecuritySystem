import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


import certifi
ca = certifi.where()

import pandas as pd
from pymongo.mongo_client import MongoClient
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

class NetworkDataExtract():
    def __init__(self):
        try :
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json_converter(self,file_path:str):
        try:
            data = pd.read_csv(file_path)
            records= data.to_dict(orient="records")
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client = MongoClient(MONGO_DB_URL,tlsCAFile=ca, tlsAllowInvalidCertificates=True)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return f"{len(self.records)} Data Records Inserted Successfully"
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "Network_data/phisingData.csv"
    DATABASE = "SANDIPAI"
    Collection = "NetworkData"
    obj = NetworkDataExtract()
    logger.info("Reading CSV data...")
    records = obj.csv_to_json_converter(file_path=FILE_PATH)
    logger.info("Inserting data into MongoDB...")
    response = obj.insert_data_mongodb(records=records,database=DATABASE,collection=Collection)
    logger.info(response)
   
