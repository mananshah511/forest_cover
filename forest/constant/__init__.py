import os,sys
from datetime import datetime

ROOT_DIR = os.getcwd()
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

DATABASE_NAME = "covtype"

COLUMN = ['elevation','aspect','slope','horizontal_distance_to_hydrology','Vertical_Distance_To_Hydrology','Horizontal_Distance_To_Roadways',
          'Horizontal_Distance_To_Fire_Points','wilderness_area1','wilderness_area2','wilderness_area3','wilderness_area4'
          ,'soil_type_1','soil_type_2','soil_type_3','soil_type_4','soil_type_5','soil_type_6','soil_type_7','soil_type_8'
          ,'soil_type_9','soil_type_10','soil_type_11','soil_type_12','soil_type_13','soil_type_14','soil_type_15','soil_type_16'
          ,'soil_type_17','soil_type_18','soil_type_19','soil_type_20','soil_type_21','soil_type_22','soil_type_23','soil_type_24'
          ,'soil_type_25','soil_type_26','soil_type_27','soil_type_28','soil_type_29','soil_type_30','soil_type_31','soil_type_32'
          ,'soil_type_33','soil_type_34','soil_type_35','soil_type_36','soil_type_37','soil_type_38','soil_type_39','soil_type_40'
]

#training pipeline related varibales

TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRINING_PIPELINE_NAME_KEY = "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"

#data ingestion related varibales

DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_DIR = "data_ingestion"
DATA_INGESTION_RAW_DATA_DIR = "raw_data_dir"
DATA_INGESTION_ZIP_DATA_DIR = "zip_data_dir"
DATA_INGESTION_INGESTED_DATA_DIR = "ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DATA_DIR = "ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DATA_DIR = "ingested_test_dir"