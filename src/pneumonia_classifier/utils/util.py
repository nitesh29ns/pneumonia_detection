import yaml
import os,sys
from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.logger import lg 




def read_yaml_file(file_path:str) ->dict :
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise classificationException(e, sys) from e
    
    
    