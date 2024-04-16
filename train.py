import tensorflow as tf
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import logging as lg

log_file_path = "./model_train_history.log"

lg.basicConfig(filename=log_file_path,
               filemode="w",
               format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s ',
               level=lg.INFO)



data_dir = r"D:\ml\pneumonia_detection\flower_photos" #"D:\ml\pneumonia_detection\chest_x_ray_dataset\chest_xray\train"

training_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=(1.0/225))

training_iterator = training_data_generator.flow_from_directory(data_dir,class_mode="categorical", color_mode="rgb", target_size=(224,224), interpolation='nearest', batch_size=16)


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
    tf.keras.layers.Dense(5, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['acc'])

model.fit(training_iterator, epochs=5)

model.save("flower_CNN.h5")



"""
model =  tf.keras.applications.resnet50.ResNet50(
    input_shape=training_iterator.image_shape,
    weights=None,
    include_top = False)

model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"])

flatten_in = tf.keras.layers.Flatten()(model.output)

prediction = tf.keras.layers.Dense(
    units=2,
    activation="softmax"
)(flatten_in)

full_model = tf.keras.models.Model(
    inputs=model.input,
    outputs=prediction
)

full_model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=['accuracy']
)


model_histroy = full_model.fit(training_iterator,batch_size=128,epochs=1)

full_model.save("./new_resnet50.h5")
"""

"""
model =  tf.keras.applications.resnet.ResNet50(
    input_shape=training_iterator.image_shape,
    weights="imagenet",
    include_top = False)

model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"])

flatten_in = tf.keras.layers.Flatten()(model.output)

prediction = tf.keras.layers.Dense(
    units=2,
    activation="softmax"
)(flatten_in)

full_model = tf.keras.models.Model(
    inputs=model.input,
    outputs=prediction
)

full_model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=['accuracy']
)


model_histroy = full_model.fit(training_iterator,batch_size=128,epochs=3)

#lg.info(f"train history : {model_histroy}")

full_model.save("local_resnet50.h5")
"""