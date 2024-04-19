
from src.pneumonia_classifier.logger import lg 
from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.entity.component_config_entity import *
from src.pneumonia_classifier.constants import *
from src.pneumonia_classifier.utils.util import read_yaml_file
import os, sys
from datetime import datetime



class configration:
    def __init__(self,
                config_file_path:str = CONFIG_FILE_PATH,
                current_time_stamp:str = CURRENT_TIME_STAMP)-> None :
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.trainging_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_data_ingestion_config(self)-> dataingestionconfig:
        try:
            artifact_dir = self.trainging_pipeline_config.artfact_dir

            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )

            os.makedirs(data_ingestion_artifact_dir,exist_ok=True)

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATASET_DOWNLOAD_URL_KEY]

            data_file_name = data_ingestion_info[DATASET_FILE_NAME_KEY]

            tgz_download_dir = os.path.join(data_ingestion_artifact_dir,
                                            data_ingestion_info[TGZ_DOWNLOAD_DIR_KEY])
            
            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
                                             data_ingestion_info[INGESTED_DIR_KEY])
            
            data_ingestion_config = dataingestionconfig(
                dataset_download_url=dataset_download_url,
                tgz_download_dir=tgz_download_dir,
                ingested_data_dir=ingested_data_dir
            )
            lg.info(f"data ingestion config: [{data_ingestion_config}].")
            return data_ingestion_config
        
        except Exception as e:
            raise classificationException(e, sys) from e
