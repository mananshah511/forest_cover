import os,sys
from forest.loggers import logging
from forest.exception import ForestException
from forest.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from forest.constant import *
from forest.util.util import read_yaml


class Configuration:

    def __init__(self,config_file_path:str=CONFIG_FILE_PATH,
                 current_time_stamp:str=CURRENT_TIME_STAMP) -> None:
        try:
            self.config_info = read_yaml(file_path=config_file_path)
            self.current_time_stamp = current_time_stamp
            self.training_pipeline_config = self.get_training_pipeline_config()
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            logging.info(f"get data ingestion config function started")

            artifact_dir = self.training_pipeline_config.artifact_dir

            data_ingestion_config = self.config_info[DATA_INGESTION_CONFIG_KEY]

            data_ingestion_dir = os.path.join(artifact_dir,DATA_INGESTION_DIR,self.current_time_stamp)

            raw_data_dir = os.path.join(data_ingestion_dir,data_ingestion_config[DATA_INGESTION_RAW_DATA_DIR])

            zip_data_dir = os.path.join(data_ingestion_dir,data_ingestion_config[DATA_INGESTION_ZIP_DATA_DIR])

            ingestion_dir = os.path.join(data_ingestion_dir,data_ingestion_config[DATA_INGESTION_INGESTED_DATA_DIR])

            train_ingested_dir = os.path.join(ingestion_dir,data_ingestion_config[DATA_INGESTION_INGESTED_TRAIN_DATA_DIR])

            test_ingested_dir = os.path.join(ingestion_dir,data_ingestion_config[DATA_INGESTION_INGESTED_TEST_DATA_DIR])

            data_download_url = data_ingestion_config[DATA_INGESTION_DOWNLOAD_URL_KEY]

            data_ingestion_config = DataIngestionConfig(dataset_download_url=data_download_url,
                                                        raw_data_dir=raw_data_dir,
                                                        zip_data_dir=zip_data_dir,
                                                        ingested_train_dir=train_ingested_dir,
                                                        ingested_test_dir=test_ingested_dir)
            
            logging.info(f"data ingestion config : {data_ingestion_config}")

            return data_ingestion_config
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            logging.info(f"get training pipeline config function started")
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]

            artifact_dir = os.path.join(ROOT_DIR,training_pipeline_config[TRINING_PIPELINE_NAME_KEY],
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)

            logging.info(f"training pipeline config : {training_pipeline_config}")

            return training_pipeline_config   
        except Exception as e:
            raise ForestException(sys,e) from e