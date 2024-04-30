from src.pneumonia_classifier.logger import lg 
from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.entity.component_config_entity import *
from src.pneumonia_classifier.entity.artifact_entity import DataIngestArtifact
from src.pneumonia_classifier.constants import *
from src.pneumonia_classifier.utils.util import read_yaml_file
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import os, sys, shutil
from tqdm import tqdm


class DataIngestion:
    def __init__(self, data_ingestion_config:dataingestionconfig):
        try:
            lg.info(f"{'='*20}Data ingestion log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise classificationException(e,sys) from e 
        
    def download_dataset(self)->str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            # to remove the tgz folder if exists
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            # to make tgz folder 
            os.makedirs(tgz_download_dir, exist_ok=True)

            lg.info("download file from [{download_url}] into [{tgz_download_dir}].")

            # extract tgz file using kaggel api
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_files(download_url,
                                       path=tgz_download_dir) # unzip=True -- for download unziped data directly.
            lg.info(f"[{tgz_download_dir}] is download successfully using kaggle api.")
            return tgz_download_dir
        
        except Exception as e:
            raise classificationException(e,sys) from e 
        
    def extract_tgz_file(self,tgz_dir:str)->DataIngestArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.ingested_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            zip_file = os.path.join(tgz_dir,
                                    os.listdir(tgz_dir)[0])
            
            lg.info(f"extract tgz_file[{zip_file}] into [{raw_data_dir}].")
            with zipfile.ZipFile(zip_file) as obj:
                tqdm(obj.extractall(path=raw_data_dir))

            lg.info(f"extraction completed.")

            data_ingestion_artifact = DataIngestArtifact(
                ingested_dir_path = raw_data_dir,
                message=f"data ingestion completed successfully."
            )
            return data_ingestion_artifact
        
        except Exception as e:
            raise classificationException(e,sys) from e
        
    def data_validation(self)->None:
        try:
            ingested_data = self.data_ingestion_config.ingested_dir

            dir = os.listdir(f"{ingested_data}\{os.listdir(ingested_data)[0]}")

            if VALID_VAL_DATA_DIR_KEY and VALID_TRAIN_DIR_KEY and VALID_TEST_DIR_KEY in dir:
                dir.remove(VALID_VAL_DATA_DIR_KEY)
                dir.remove(VALID_TRAIN_DIR_KEY)
                dir.remove(VALID_TEST_DIR_KEY)

            for i in dir:
                shutil.rmtree(f"{ingested_data}\{os.listdir(ingested_data)[0]}\{i}")

            lg.info(f"Remove unnecessary directory : {dir}")
        except Exception as e:
            raise classificationException(e,sys) from e
        
    
    def initiate_data_ingestion(self)-> DataIngestArtifact:
        try:
            tgz_file_path = self.download_dataset()
            ingested_artifact = self.extract_tgz_file(tgz_dir=tgz_file_path)
            self.data_validation()
            return ingested_artifact
        except Exception as e:
            raise classificationException(e, sys) from e