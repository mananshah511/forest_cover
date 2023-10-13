import os,sys,shutil
from forest.loggers import logging
from forest.exception import ForestException
from forest.entity.config_entity import ModelPusherConfig
from forest.entity.artifact_entity import ModelPusherArtifact,ModelEvulationArtifact


class ModelPusher:

    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_evulation_artifact:ModelEvulationArtifact) -> None:
        try:
            logging.info(f"{'>>'*20}Model Pusher log completed.{'<<'*20} \n\n")
            self.model_pusher_config = model_pusher_config
            self.model_evulation_artifact = model_evulation_artifact
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def export_model_dir(self)->ModelPusherArtifact:
        try:
            logging.info(f"export model dir function started")
            trained_model_path = self.model_evulation_artifact.evulation_model_file_path
            export_model_dir = self.model_pusher_config.export_dir_path
            export_dir_list = []

            for cluster_number in range(len(trained_model_path)):
                trained_model_name = os.path.basename(trained_model_path[cluster_number])
                export_dir_path = os.path.join(export_model_dir,'cluster'+str(cluster_number))
                os.makedirs(export_dir_path,exist_ok=True)
                shutil.copy(trained_model_path[cluster_number],dst=export_dir_path)
                export_dir_list.append(os.path.join(export_dir_path,trained_model_name))
            
            logging.info(f"all models are copied to : {export_dir_path}")
            model_pusher_artifact = ModelPusherArtifact(export_dir_path=export_dir_list)
            return model_pusher_artifact
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def intiate_model_pusher(self)->ModelPusherArtifact:
        try:
            logging.info(f"intiate model pusher function started")
            return self.export_model_dir()
        except Exception as e:
            raise ForestException(sys,e) from e
        
    def __del__(self):
        logging.info(f"{'>>'*20}Model Pusher log completed.{'<<'*20} \n\n")
