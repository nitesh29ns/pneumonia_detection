from src.pneumonia_classifier.logger import lg 
from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.config.configuration import configration
from src.pneumonia_classifier.constants import *
from src.pneumonia_classifier.entity.artifact_entity import ModelTrainerArtifact, DataIngestArtifact
from src.pneumonia_classifier.entity.component_config_entity import modeltrainerconfig
from src.pneumonia_classifier.utils.util import read_yaml_file
import os, sys
import tensorflow as tf


class Model_Trainer:
    def __init__(self,model_trainer_config, data_ingestion_artifact):
        try:
            lg.info(f"{'>>' * 30} model trainer log started {'<<' * 30}")
            self.model_trainer_config = model_trainer_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise classificationException(e, sys) from e
        
    def get_data(self):
        try:
            lg.info(f"{'>>' * 30}getting data ready for training {'<<' * 30}")
            data_path = self.data_ingestion_artifact.ingested_dir_path
            training_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=(1.0/225))
            training_iterator = training_data_generator.flow_from_directory(data_path,class_mode="categorical",color_mode="rgb", target_size=(224,224),interpolation='nearest',batch_size=16)
            return training_iterator
        except Exception as e:
            raise classificationException(e, sys) from e
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            lg.info(f"{'>>' * 30}loading data {'<<' *30}")
            data = self.get_data()

            lg.info(f"{'>>' * 30} create convolution model {'<<' * 30}")
            model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(32, (3,3), input_shape=(224,224,3), activation='relu'),
                    tf.keras.layers.MaxPooling2D(2,2),
                    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
                    tf.keras.layers.MaxPooling2D(2,2),
                    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
                    tf.keras.layers.MaxPooling2D(2,2),
                    tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
                    tf.keras.layers.MaxPooling2D(2,2),
                    tf.keras.layers.Conv2D(512, (3,3), activation='relu'),
                    tf.keras.layers.MaxPooling2D(2,2),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(256, activation='relu'),
                    tf.keras.layers.Dense(1, activation='sigmoid')
                    ])
            
            params = read_yaml_file(file_path=self.model_trainer_config.model_config_file_path)
            params = params[MODEL_PARAMS_KEY]
            model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=params[LEARNING_RATE]), loss=params[LOSS_KEY], metrics=[params[METRICS_KEY]])

            lg.info(f"{'>>' * 30}model summary: {model.summary()}")

            lg.info(f"{'>>' * 30}start training model on our data{'<<' * 30}")
            model.fit(data, epochs=params[EPOCHS_KEY])

            trained_model_file_path = self.model_trainer_config.trained_model_file_path
            model.save(trained_model_file_path)
            lg.info(f"{'>>' * 30}model is saved -- {trained_model_file_path}.")
            
            model_trainer_artifact = ModelTrainerArtifact(
                message="model training successfully.",
                trained_model_file_path=trained_model_file_path
            )
            return model_trainer_artifact

        except Exception as e:
            raise classificationException(e, sys) from e

    def __del__(self):
        lg.info(f"{'>>' * 30}Model trainer log completed.{'<<' * 30} ")
