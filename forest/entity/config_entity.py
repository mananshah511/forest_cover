from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",
                                 ["dataset_download_url","raw_data_dir","zip_data_dir","ingested_train_dir","ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig",
                                  ["schema_file_dir","report_page_file_dir","report_name"])

DataTransformConfig = namedtuple("DataTransformConfig",
                                 ["graph_save_dir","transform_train_dir","transform_test_dir","preprocessed_file_path","cluster_model_file_path"])

ModelTrainerConfig = namedtuple("ModelTrainerConfig",["trained_model_file_path","base_accuracy",
                                                      "model_config_file_path"])

ModelEvulationConfig = namedtuple("ModelEvulationConfig",["evulation_file_path","time_stamp"])

ModelPusherConfig = namedtuple("ModelPusherConfig",
                               ["export_dir_path"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["artifact_dir"])


