import yaml
import os,sys
from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.logger import lg 
from src.pneumonia_classifier.constants import *
import mysql.connector as conn



def read_yaml_file(file_path:str) ->dict :
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise classificationException(e, sys) from e
    
    
def upload_data_to_db(name, age, bytes_data, normal, pneumonia):
    mydb = conn.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD)
    cursor = mydb.cursor()
    query = "insert into pneumonia_data.user_data values(%s, %s, %s, %s, %s)"
    args = (name, age, bytes_data, normal, pneumonia)
    cursor.execute(query, args)
    mydb.commit()


def get_model_path():
    try:
        folder_name = MODEL_DIR
        file_name = os.listdir(folder_name)[0]
        latest_model_path = os.path.join(folder_name, file_name)
        
        return latest_model_path
    except Exception as e:
        raise classificationException(e,sys) from e