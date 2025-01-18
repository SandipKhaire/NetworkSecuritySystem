import sys
import os
import certifi

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from pydantic import BaseModel

class ModelInput(BaseModel):
    having_IP_Address: int
    URL_Length: int
    Shortining_Service: int
    having_At_Symbol: int
    double_slash_redirecting: int
    Prefix_Suffix: int
    having_Sub_Domain: int
    SSLfinal_State: int
    Domain_registeration_length: int
    Favicon: int
    port: int
    HTTPS_token: int
    Request_URL: int
    URL_of_Anchor: int
    Links_in_tags: int
    SFH: int
    Submitting_to_email: int
    Abnormal_URL: int
    Redirect: int
    on_mouseover: int
    RightClick: int
    popUpWidnow: int
    Iframe: int
    age_of_domain: int
    DNSRecord: int
    web_traffic: int
    Page_Rank: int
    Google_Index: int
    Links_pointing_to_page: int
    Statistical_report: int



from networksecurity.utils.main_utils.utils import load_object
clinet = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = clinet[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags= ["autentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response(content="Training pipeline completed successfully",status_code=200)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict(input_data: ModelInput):
    try:
        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocesor,final_model)
        input_dict = input_data.dict()
        data = pd.DataFrame([input_dict])
        prediction = network_model.predict(data)
        return Response(content=f"prediction: {prediction.tolist()}",status_code=200)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)