import os,sys,dill,csv
from forest.loggers import logging
from forest.exception import ForestException
from forest.entity.config_entity import DataTransformConfig
from forest.entity.artifact_entity import DataTransformArtifact,DataIngestionArtifact,DataValidationArtifact
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from yellowbrick.cluster import SilhouetteVisualizer
import pandas as pd
import numpy as np
from forest.constant import TARGET_COLUMN_KEY,DROP_COLUMN_LIST,NO_CLUSTER,COLUMN
from forest.util.util import read_yaml
import matplotlib.pyplot as plt
from pathlib import Path


class DataTransform:

    def __init__(self,data_transform_config:DataTransformConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact) -> None:
        try:
            self.data_transform_config = data_transform_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.target_column = read_yaml(self.data_validation_artifact.schema_file_path)[TARGET_COLUMN_KEY]
            logging.info(f"{'>>'*20}Data Transformation log started.{'<<'*20} \n\n")
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_preprocessing_object(self):
        try:
            logging.info(f"get preprocessing object function started")

            logging.info(f"pipeline ensamble started")
            pipeline = Pipeline(steps=[
                                       ('scaler',StandardScaler())])
            logging.info(f"pipelien ensamble completed")

            return pipeline
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def perform_preprocessing(self,preprocessing_object:Pipeline,is_test_data:bool=False):
        try:
            logging.info(f"perform preprocessig function started")

            if is_test_data == False:

                logging.info(f"-----reading train data started-----")
                train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
                logging.info(f"-----reading train data completed-----")

                target_df = train_df.iloc[:,-1]
                logging.info(f"dropping target column from train data")
                train_df.drop(self.target_column,axis=1,inplace=True)
                train_df.drop(DROP_COLUMN_LIST,inplace=True,axis=1)

                train_columns = train_df.columns

                train_df = preprocessing_object.fit_transform(train_df)

                train_df = pd.DataFrame(train_df,columns=train_columns)
                train_df = pd.concat([train_df,target_df],axis=1)
                logging.info(f"combining train and target dataframe")
                

                return train_df,preprocessing_object
            else:
                logging.info(f"-----reading test data started-----")
                test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
                logging.info(f"-----reading test data completed-----")

                target_df = test_df.iloc[:,-1]
                logging.info(f"dropping target column from test data")
                test_df.drop(self.target_column,axis=1,inplace=True)
                test_df = test_df.drop(DROP_COLUMN_LIST, axis=1)
                test_column = test_df.columns

                test_df = preprocessing_object.transform(test_df)

                test_df = pd.DataFrame(test_df,columns=test_column)
                test_df = pd.concat([test_df,target_df],axis=1)
                
                logging.info(f"combining test and target dataframe")
                return test_df
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_save_graph_cluster(self,train_df:pd.DataFrame):
        try:
            logging.info(f"get and save graph cluster function started")

            logging.info(f"making k-means object")
            kmeans = KMeans(init='k-means++',random_state=42)

            logging.info(f"making visulizer object and fitting data")
            visulizer = KElbowVisualizer(kmeans,k=(2,11))
            visulizer.fit((train_df.drop(self.target_column,axis=1)))

            graph_dir = self.data_transform_config.graph_save_dir
            os.makedirs(graph_dir,exist_ok=True)
            graph_file_path = os.path.join(graph_dir,'graph_cluster.png')

            visulizer.show(graph_file_path)
            logging.info(f"graph saved successfully")
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def get_and_save_silhouette_score_graph(self,train_df:pd.DataFrame):
        try:
            logging.info(f"get and save silhouetter score graph function started")
            fig, ax = plt.subplots(2, 2, figsize=(15,8))

            for no_cluster in [2,3,4,5]:
                logging.info(f"finding silhouette_score for {no_cluster} cluster")
                kmeans = KMeans(n_clusters=no_cluster,init='k-means++',random_state=42)
                q, mod = divmod(no_cluster, 2)
                visulizer = SilhouetteVisualizer(kmeans,colors='yellowbrick',ax=ax[q-1][mod])

                visulizer.fit((train_df.drop(self.target_column,axis=1)))

                graph_dir = self.data_transform_config.graph_save_dir
                os.makedirs(graph_dir,exist_ok=True)
                graph_file_path = os.path.join(graph_dir,'cluster_'+str(no_cluster)+'_silhouette_score.png')
                visulizer.show(graph_file_path)
                logging.info(f"graph saved successfully")
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def save_data_based_on_cluster(self,train_df:pd.DataFrame,test_df:pd.DataFrame,n_cluster):
        try:
            logging.info(f"save data based on cluster function started")

            logging.info(f"making k-means object and fitting data")
            k_means = KMeans(n_clusters=n_cluster,init='k-means++',random_state=42)
            k_means.fit((train_df.drop(self.target_column,axis=1)))

            train_predict = k_means.predict((train_df.drop(self.target_column,axis=1)))

            transform_train_folder = self.data_transform_config.transform_train_dir
            os.makedirs(transform_train_folder,exist_ok=True)

            column_name = list(train_df.columns)
            logging.info(f"train column names are : {column_name}")

            cluster_numbers = list(np.unique(np.array(train_predict)))
            logging.info(f"unique cluster numbers are : {cluster_numbers}")

            logging.info(f"making csv files for train data based on cluster")

            for cluster_number in cluster_numbers:
                train_files_path = os.path.join(transform_train_folder,'train_cluster'+str(cluster_number)+'.csv')
                with Path(train_files_path).open('w',newline='') as csvfiles:
                    csvwriter = csv.writer(csvfiles)

                    csvwriter.writerow(column_name)

                    for index in range(len(train_predict)):
                        if train_predict[index] == cluster_number:
                            csvwriter.writerow(train_df.iloc[index])
            logging.info(f"csv files write for train data is completed")

            test_predict = k_means.predict((test_df.drop(self.target_column,axis=1)))

            transform_test_folder = self.data_transform_config.transform_test_dir
            os.makedirs(transform_test_folder,exist_ok=True)

            column_name = list(test_df.columns)
            logging.info(f"test column names are : {column_name}")

            cluster_numbers = list(np.unique(np.array(test_predict)))
            logging.info(f"unique cluster numbers are : {cluster_numbers}")

            logging.info(f"making csv files for test data based on cluster")

            for cluster_number in cluster_numbers:
                test_files_path = os.path.join(transform_test_folder,'test_cluster'+str(cluster_number)+'.csv')
                with Path(test_files_path).open('w',newline='') as csvfiles:
                    csvwriter = csv.writer(csvfiles)

                    csvwriter.writerow(column_name)

                    for index in range(len(test_predict)):
                        if test_predict[index] == cluster_number:
                            csvwriter.writerow(test_df.iloc[index])
            logging.info(f"csv files write for test data is completed")
            return k_means

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def intiate_data_transform(self):
        try:
            logging.info(f"intiate data transform function started")
            preprocessed_obj = self.get_preprocessing_object()
            train_df,preprocessed_obj = self.perform_preprocessing(preprocessing_object=preprocessed_obj)

            logging.info(f"saving preprocessing object")
            preproceesed_file_path = os.path.dirname(self.data_transform_config.preprocessed_file_path)
            os.makedirs(preproceesed_file_path,exist_ok=True)
            with open(self.data_transform_config.preprocessed_file_path,'wb') as objfile:
                dill.dump(preprocessed_obj,objfile)
            logging.info(f"preporcessing object saved")

            test_df = self.perform_preprocessing(preprocessing_object=preprocessed_obj,is_test_data=True)

            self.get_save_graph_cluster(train_df=train_df)
            #self.get_and_save_silhouette_score_graph(train_df=train_df)

            kmeans = self.save_data_based_on_cluster(train_df=train_df,test_df=test_df,n_cluster=NO_CLUSTER)

            logging.info(f"saving cluster object")
            cluster_dir = os.path.dirname(self.data_transform_config.cluster_model_file_path)
            os.makedirs(cluster_dir,exist_ok=True)
            with open(self.data_transform_config.cluster_model_file_path,'wb') as clusterobj:
                dill.dump(kmeans,clusterobj)
            logging.info(f"cluster object saved")

            data_transform_artifact = DataTransformArtifact(is_transform=True,
                                                            message="successfull",
                                                            transform_train_dir=self.data_transform_config.transform_train_dir,
                                                            transform_test_dir=self.data_transform_config.transform_test_dir,
                                                            preprocessed_dir=self.data_transform_config.preprocessed_file_path,
                                                            cluster_model_dir=cluster_dir)
            return data_transform_artifact
            

        except Exception as e:
            raise ForestException(sys,e) from e
        
    def __del__(self):
        logging.info(f"{'>>'*20}Data Transformation log completed.{'<<'*20} \n\n")