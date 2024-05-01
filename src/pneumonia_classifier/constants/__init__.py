import os 
import datetime

ROOT_DIR = os.getcwd()   

def get_current_time_stamp():
    return f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


SAVED_MODELS_DIR_NAME = "saved_model"
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
YOLO_MODEL = "keremberke/yolov8m-chest-xray-classification"

CONFIG_DIR = 'yaml_config' 
CONFIG_FILE_NAME = 'component_config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

#SCHEMA_FILE_NAME = 'schema.yaml'
#SCHEMA_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,SCHEMA_FILE_NAME)


CURRENT_TIME_STAMP = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWD ="nitesh8527" 

# data ingestion and validation related variables
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion' # name of the folder inside arifact 
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATASET_DOWNLOAD_URL_KEY = 'dataset_download_url'
TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
INGESTED_DIR_KEY = 'ingested_dir'


# data validation related variables
VALID_VAL_DATA_DIR_KEY = 'val'
VALID_TRAIN_DIR_KEY = 'train'
VALID_TEST_DIR_KEY = 'test'


#Training pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config" 
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


# model training related variables
MODEL_TRAINER_ARTIFACT_DIR_KEY = 'model_training'
MODEL_TRAINER_CONFIG_KEY = 'model_trainer_config'
TRAINED_MODEL_DIR_KEY = 'trained_model_dir'
TRAINED_MODEL_CONFIG_DIR = 'model_config_dir'
TRAINED_MODEL_CONFIG_FILE_NAME = 'model_config_file_name'
TRAINED_MODEL_FILE_NAME = 'model_file_name'

# trainig parameters
MODEL_PARAMS_KEY = "params"
EPOCHS_KEY = 'epochs'
LEARNING_RATE = 'learning_rate'
LOSS_KEY = 'loss'
METRICS_KEY = 'metrics'

# model pusher related variables
MODEL_PUSHER_CONFIG_KEY ='model_pusher_config'
MODEL_PUSHER_SAVED_MODEL_DIR = 'saved_model_dir'