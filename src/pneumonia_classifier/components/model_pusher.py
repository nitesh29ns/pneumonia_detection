from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.logger import lg
from src.pneumonia_classifier.entity.artifact_entity import *
from src.pneumonia_classifier.entity.component_config_entity import modelPusherconfig
from src.pneumonia_classifier.constants import *
import os, sys
import shutil


class Model_Pusher:
    def __init__(self,model_pusher_config : modelPusherconfig, 
                model_trainer_artfact: ModelTrainerArtifact):
        try:
            lg.info(f"{'>>' * 30} model pusher log stared. {'<<' * 30}")
            self.model_pusher_config = model_pusher_config
            self.model_trainer_artfact = model_trainer_artfact
        except Exception as e:
            raise classificationException(e,sys) from e


    def import_current_model(self):
        try:
            model_path = self.model_trainer_artfact.trained_model_file_path

            model_name = os.path.basename(model_path)

            os.makedirs(self.model_pusher_config.saved_model_path, exist_ok=True)

            saved_model_path = os.path.join(self.model_pusher_config.saved_model_path,model_name)

            shutil.copy(model_path, saved_model_path)

            return saved_model_path
        except Exception as e:
            raise classificationException(e,sys) from e
        
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            export_model_file_path = self.import_current_model()
            Model_Pusher_artifact = ModelPusherArtifact(
                is_model_pusher=True,
                export_model_file_path=export_model_file_path
            )

            return Model_Pusher_artifact
        except Exception as e:
            raise classificationException(e, sys) from e
       
    def __del__(self):
        lg.info(f"{'>>' * 30} model pusher log completed. {'<<' * 30}")