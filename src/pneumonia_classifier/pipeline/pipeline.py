from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.logger import lg 
from src.pneumonia_classifier.entity.artifact_entity import *
import os, sys
from src.pneumonia_classifier.components.data_ingestion import DataIngestion
from src.pneumonia_classifier.components.model_trainer import Model_Trainer
from src.pneumonia_classifier.components.model_pusher import Model_Pusher
from src.pneumonia_classifier.config.configuration import configration

class PipeLine():

    def __init__(self,config:configration)->None:
        try:
            # make artifact folder
            os.makedirs(config.trainging_pipeline_config.artifact_dir, exist_ok=True)
            self.config = config
        except Exception as e:
            raise classificationException(e, sys) from e
        
    def start_data_ingestion(self)->DataIngestArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())

            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise classificationException(e, sys) from e
            

    def start_model_trainer(self,data_ingestion_artifact=DataIngestArtifact)->ModelTrainerArtifact:
        try:
            model_trainer = Model_Trainer(model_trainer_config=self.config.get_model_trainer_config(),
                                          data_ingestion_artifact=data_ingestion_artifact)
            
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise classificationException(e,sys) from e
        
    def start_model_pusher(self,model_trainer_artifact = ModelTrainerArtifact)-> ModelPusherArtifact:
        try:
            model_pusher = Model_Pusher(model_pusher_config= self.config.get_model_pusher_config(),
                                        model_trainer_artfact=model_trainer_artifact)

            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise classificationException(e, sys) from e
        
    def run_pipeline(self):
        try:
            lg.info("pipeline stating.")
            data_ingestion_artifact = self.start_data_ingestion()
            model_trainer_artifact = self.start_model_trainer(data_ingestion_artifact=data_ingestion_artifact)
            model_pusher_artifact = self.start_model_pusher(model_trainer_artifact=model_trainer_artifact)
            
            return model_pusher_artifact
        
        except Exception as e:
            raise classificationException(e, sys) from e
        

    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise e