from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.logger import lg 
from src.pneumonia_classifier.pipeline.pipeline import PipeLine
from src.pneumonia_classifier.config.configuration import configration
from src.pneumonia_classifier.components.data_ingestion import DataIngestion
from src.pneumonia_classifier.constants import *
import os, sys


def main():
    try:
        pipeline = PipeLine(config=configration(current_time_stamp=get_current_time_stamp()))
        pipeline.run()
        lg.info("main funcation execution completed.")
    except Exception as e:
        lg.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()