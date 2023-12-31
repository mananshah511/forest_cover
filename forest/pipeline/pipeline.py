import os,sys,json
from forest.loggers import logging
from forest.exception import ForestException
from forest.config.configuration import Configuration
from forest.entity.config_entity import DataIngestionConfig
from forest.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformArtifact,ModelTrainerArtifact,ModelEvulationArtifact,ModelPusherArtifact,FinalArtifact
from forest.components.data_ingestion import DataIngestion
from forest.components.data_validation import DataValidation
from forest.components.data_transform import DataTransform
from forest.components.model_trainer import ModelTrainer
from forest.components.model_evulation import ModelEvulation
from forest.components.model_pusher import ModelPusher

class Pipeline:

    def __init__(self,config:Configuration=Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.intiate_data_ingestion()
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=self.config.get_data_validation_config())

            return data_validation.intiate_data_validation()
        except Exception as e:
            raise ForestException(sys,e) from e

    def start_data_transform(self,data_ingestion_artifact:DataIngestionArtifact,
                                data_validation_artifact:DataValidationArtifact)->DataTransformArtifact:
        try:
            data_transform = DataTransform(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_artifact=data_validation_artifact,
                                           data_transform_config=self.config.get_data_transform_config())
            return data_transform.intiate_data_transform()
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def start_model_trainer(self,data_transform_artifact:DataTransformArtifact)->ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(data_transform_artifact=data_transform_artifact,
                                         model_trainer_config=self.config.get_model_trainer_config())
            return model_trainer.intiate_model_trainer()
        except Exception as e:
            raise ForestException(sys,e) from e

    def start_model_evulation(self,data_transform_artifact:DataTransformArtifact,
                              model_trainer_artifact:ModelTrainerArtifact)->ModelEvulationArtifact:
        try:
            model_evulation = ModelEvulation(data_transform_artifact=data_transform_artifact,
                                             model_trainer_artifact=model_trainer_artifact,
                                             model_evulation_config=self.config.get_model_evulation_config())
            return model_evulation.intiate_model_evulation()
        except Exception as e:
            raise ForestException(sys,e) from e

    def start_model_pusher(self,model_evulation_artifact:ModelEvulationArtifact)->ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(model_evulation_artifact=model_evulation_artifact,
                                       model_pusher_config=self.config.get_model_pusher_config())
            return model_pusher.intiate_model_pusher()
        except Exception as e:
            raise ForestException(sys,e) from e
        
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transform_artifact = self.start_data_transform(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transform_artifact=data_transform_artifact)
            model_evultion_artifact = self.start_model_evulation(data_transform_artifact=data_transform_artifact,
                                                                 model_trainer_artifact=model_trainer_artifact)
            model_pusher_artifact = self.start_model_pusher(model_evulation_artifact=model_evultion_artifact)

            final_artifact = FinalArtifact(preprocessed_model_path=data_transform_artifact.preprocessed_dir,
                                           cluster_model_path=data_transform_artifact.cluster_model_dir,
                                           export_dir_path=model_pusher_artifact.export_dir_path)

            with open('data.json', 'w') as json_obj:
                json.dump(final_artifact._asdict(), json_obj)


        except Exception as e:
            raise ForestException(sys,e) from e