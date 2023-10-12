import os,sys
from datetime import datetime

ROOT_DIR = os.getcwd()
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

DATABASE_NAME = "covtype"

NO_CLUSTER = 3

DROP_COLUMN_LIST = ['wilderness_area1','soil_type_1']

COLUMN = ['elevation','aspect','slope','horizontal_distance_to_hydrology','Vertical_Distance_To_Hydrology','Horizontal_Distance_To_Roadways',
          'Horizontal_Distance_To_Fire_Points','wilderness_area1','wilderness_area2','wilderness_area3','wilderness_area4'
          ,'soil_type_1','soil_type_2','soil_type_3','soil_type_4','soil_type_5','soil_type_6','soil_type_7','soil_type_8'
          ,'soil_type_9','soil_type_10','soil_type_11','soil_type_12','soil_type_13','soil_type_14','soil_type_15','soil_type_16'
          ,'soil_type_17','soil_type_18','soil_type_19','soil_type_20','soil_type_21','soil_type_22','soil_type_23','soil_type_24'
          ,'soil_type_25','soil_type_26','soil_type_27','soil_type_28','soil_type_29','soil_type_30','soil_type_31','soil_type_32'
          ,'soil_type_33','soil_type_34','soil_type_35','soil_type_36','soil_type_37','soil_type_38','soil_type_39','soil_type_40','class'
]


COLUMN_KEY = "columns"
NUMERIC_COULMN_KEY = "numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"
TARGET_COLUMN_KEY = "target_column"


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

#data validation related varibales

DATA_VALIDTION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_DIR = "data_validation"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_KEY = "schema_file"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME = "report_page_file_name"

#data transform related varibales

DATA_TRANSFORM_CONFIG_KEY = "data_transform_config"
DATA_TRANSFORM_DIR = "data_transform"
DATA_TRANSFORM_GRAPH_DIR_KEY = "graph_save_dir"
DATA_TRANSFORM_TRAIN_DIR_KEY = "train_dir"
DATA_TRANSFORM_TEST_DIR_KEY = "test_dir"
DATA_TRANSFORM_PREPROCESSED_OBJECT_DIR_KEY = "preprocessed_object_dir"
DATA_TRANSFORM_PREPROCESSED_OBJECT_FILE_NAME_KEY = "preprocessed_object_file_name"
DATA_TRANSFORM_CLUSTER_MODEL_DIR_KEY = "cluster_model_dir"
DATA_TRANSFORM_CLUSTER_MODEL_NAME_KEY = "cluster_model_name"

