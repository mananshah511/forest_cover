import os,sys
import pandas as pd
from forest.loggers import logging
from forest.exception import ForestException
from forest.util.util import read_yaml
from forest.entity.config_entity import DataValidationConfig
from forest.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from forest.constant import COLUMN_KEY,NUMERIC_COULMN_KEY,CATEGORICAL_COLUMN_KEY
from evidently.dashboard.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            logging.info(f"{'>>'*20}Data Validation log started.{'<<'*20} \n\n")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_train_test_df(self):
        try:
            logging.info(f"get train test dataframe function started")

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            logging.info(f"data load successfull")

            return train_df,test_df
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def check_train_test_dir_exists(self):
        try:
            logging.info(f"check train test dir exists function started")

            train_dir = self.data_ingestion_artifact.train_file_path
            test_dir = self.data_ingestion_artifact.test_file_path

            train_flag = False
            test_flag = False

            if os.path.exists(train_dir):
                logging.info(f"-----train file dir is okky-----")
                train_flag = True

            if os.path.exists(test_dir):
                logging.info(f"-----test file dir is okky-----")
                test_flag = True

            if train_flag == False:
                logging.info(f"train dir is not avialabel please check")

            if test_flag == False:
                logging.info(f"test dir is not avialabel please check")

            return train_flag and test_flag
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def check_column_count_validation(self):
        try:
            logging.info(f"check column count validation function started")
            schema_file_path = self.data_validation_config.schema_file_dir
            schema_file_data = read_yaml(file_path=schema_file_path)

            train_df,test_df = self.get_train_test_df()

            train_count = len(train_df.columns)
            test_count = len(test_df.columns)
            schema_count = len(schema_file_data[COLUMN_KEY])

            logging.info(f"column count in train data is : {train_count}")
            logging.info(f"column count in test data is : {test_count}")

            logging.info(f"column count in schema file is : {schema_count}")

            train_flag = False
            test_flag = False

            if schema_count == train_count:
                logging.info(f"column count in train file is correct")
                train_flag = True

            if schema_count == test_count:
                logging.info(f"column count in test file is correct")
                test_flag = True

            if train_flag == False:
                logging.info(f"column count in train file is not correct, please check")

            if test_flag == False:
                logging.info(f"column count in test file is not correct, please check")

            return train_flag and test_flag
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def check_column_name_validation(self):
        try:
            logging.info(f"check column name validation function started")
            schema_file_path = self.data_validation_config.schema_file_dir
            schema_file_data = read_yaml(file_path=schema_file_path)

            train_df,test_df = self.get_train_test_df()

            train_column = list(train_df.columns)
            test_column = list(test_df.columns)

            schema_column = list(schema_file_data[NUMERIC_COULMN_KEY])+list(schema_file_data[CATEGORICAL_COLUMN_KEY])

            train_column.sort()
            test_column.sort()
            schema_column.sort()

            train_flag = False
            test_flag = False

            if train_column == schema_column:
                logging.info(f"column name in train file is correct")
                train_flag = True

            if test_column == schema_column:
                logging.info(f"column name in test file is correct")
                test_flag = True

            if train_flag == False:
                logging.info(f"column name in train file is not correct, please check")

            if test_flag == False:
                logging.info(f"column name in test file is not correct, please check")

            return train_flag and test_flag

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def check_column_datatype_validation(self):
        try:
            logging.info(f"check column datatype validation function started")
            schema_file_path = self.data_validation_config.schema_file_dir
            schema_file_data = read_yaml(file_path=schema_file_path)

            train_df,test_df = self.get_train_test_df()

            train_datatype = dict(train_df.dtypes)
            test_datatype = dict(test_df.dtypes)

            schema_datatype = schema_file_data[COLUMN_KEY]

            logging.info(f"data type in train file is : {train_datatype}")
            logging.info(f"data type in test file is : {test_datatype}")

            logging.info(f"data type in schema datatype is : {schema_datatype}")

            train_flag = False
            test_flag = False

            for column_name in schema_datatype.keys():
                if train_datatype[column_name]!=schema_datatype[column_name]:
                    logging.info(f"datatype of {column_name} in train data is not correct")
                    return train_flag
                
                if test_datatype[column_name]!=schema_datatype[column_name]:
                    logging.info(f"datatype of {column_name} in test data is not correct")
                    return test_flag

            train_flag = True
            test_flag = True

            logging.info(f"datatype in train file is okky")
            logging.info(f"datatype in test file is okky")

            return train_flag and test_flag

        except Exception as e:
            raise ForestException(sys,e) from e
    
    def check_null_value_validation(self):
        try:
            logging.info(f"check null value validation function started")

            train_df,test_df = self.get_train_test_df()

            train_count = dict(train_df.isnull().sum())
            test_count = dict(test_df.isnull().sum())

            train_flag = False
            test_flag = False
            for column_name,null_count in train_count.items():
                if null_count>0:
                    logging.info(f"null count in train file's {column_name} is {null_count}")
                    return train_flag
                
            for column_name,null_count in test_count.items():
                if null_count>0:
                    logging.info(f"null count in test file's {column_name} is {null_count}")
                    return test_flag
                
            train_flag = True
            test_flag = True

            logging.info(f"no null value found in train data")
            logging.info(f"no null value found in test data")

            return train_flag and test_flag
        
        except Exception as e:
            raise ForestException(sys,e) from e

    def get_and_save_data_drift_report(self):
        try:
            logging.info("get and save data drift report function started")

            report_file_path = self.data_validation_config.report_page_file_dir
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            train_df,test_df = self.get_train_test_df()
            dashboard = Dashboard(tabs=[DataDriftTab()])
            dashboard.calculate(train_df,test_df)
            dashboard.save(report_file_path)

            logging.info(f"report saved successfully")

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def intiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info(f"intitate data validation function started")
            validation5 = False

            validation1 = self.check_train_test_dir_exists()
            if validation1:
                validation2 = self.check_column_count_validation()
            if validation2:
                validation3 = self.check_column_name_validation()
            if validation3:
                validation4 = self.check_column_datatype_validation()
            if validation4:
                validation5 = self.check_null_value_validation()

            #self.get_and_save_data_drift_report()

            data_validation_artifact = DataValidationArtifact(is_validated=validation5,
            message="succesfully",schema_file_path=self.data_validation_config.schema_file_dir,
            reprot_file_path=self.data_validation_config.report_page_file_dir)

            return data_validation_artifact            

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def __del__(self):
        logging.info(f"{'>>'*20}Data Validation log completed.{'<<'*20} \n\n")