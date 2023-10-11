import os,sys
from forest.loggers import logging
from forest.exception import ForestException
from forest.entity.config_entity import DataIngestionConfig
from forest.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import numpy as np
from six.moves import urllib
from zipfile import ZipFile
from forest.constant import DATABASE_NAME,COLUMN
import gzip,shutil
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config :DataIngestionConfig) -> None:
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} \n\n")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def download_forest_data(self)->str:
        try:
            logging.info(f"download forest data function started")
            downlaod_data_url = self.data_ingestion_config.dataset_download_url
            zip_data_dir = self.data_ingestion_config.zip_data_dir
            logging.info(f"downloading data from {downlaod_data_url} in the folder {zip_data_dir}")

            file_name = os.path.basename(downlaod_data_url)
            zip_file_path = os.path.join(zip_data_dir,file_name)
            os.makedirs(zip_data_dir,exist_ok=True)

            logging.info(f"------data download started")
            urllib.request.urlretrieve(downlaod_data_url,zip_file_path)
            logging.info(f"-----data download completed")
            return zip_file_path

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_extracted_data(self,zip_path:str):
        try:
            logging.info(f"get extracted data function started")
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            logging.info(f"extracting data from {zip_path} into {raw_data_dir} folder")

            os.makedirs(raw_data_dir,exist_ok=True)
            with ZipFile(zip_path,'r') as zip:
                zip.extractall(raw_data_dir)

            logging.info(f"extraction completed")

            data_gz_file = os.path.join(raw_data_dir,DATABASE_NAME+'.data.gz')
            data_gz_file_output = os.path.join(raw_data_dir,DATABASE_NAME+'.data')
            with gzip.open(data_gz_file,'r') as gzip_in:
                with open(data_gz_file_output,'wb') as gzip_out:
                    shutil.copyfileobj(gzip_in,gzip_out)

            logging.info(f"data extraction completed")

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_train_test_split_data(self):
        try:
            logging.info(f"get train test split data function started")
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = DATABASE_NAME+'.data'

            file_path = os.path.join(raw_data_dir,file_name)
            logging.info(f"reading file from : {file_path}")

            logging.info(f"-----data reading started-----")
            forest_df = pd.read_csv(file_path,names=COLUMN,sep=',')
            logging.info(f"-----data reading completed-----")

            logging.info(f"train test split started")
            X_train,X_test,y_train,y_test = train_test_split(forest_df.iloc[:,:-1],forest_df.iloc[:,-1],test_size=0.2, random_state=42)
            logging.info(f"train test split completed")

            file_name = file_name.replace('.data','.csv')

            train_df = None
            test_df = None

            logging.info(f"combining input and target feature")
            train_df = pd.concat([X_train,y_train],axis=1)
            test_df = pd.concat([X_test,y_test],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            logging.info(f"train file path is : {train_file_path}")
            logging.info(f"test file path is : {test_file_path}")

            if train_df is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"saving train data as csv file")
                train_df.to_csv(train_file_path,index=False)

            if test_df is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"saving test data as csv file")
                test_df.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(is_ingested=True,
                                                            message="successfully",
                                                            train_file_path=train_file_path,
                                                            test_file_path=test_file_path)
            
            return data_ingestion_artifact
            
            
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def intiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info(f"intiate data ingestion function started")
            zip_path = self.download_forest_data()
            self.get_extracted_data(zip_path=zip_path)
            return self.get_train_test_split_data()

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
        
    

