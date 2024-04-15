import streamlit as st
import numpy as np
from PIL import Image
from ultralyticsplus import YOLO, postprocess_classify_output
import tensorflow as tf
import cv2
import io
import base64
import mysql.connector as conn

mydb = conn.connect(host = "localhost", user = "root", passwd="nitesh8527")
cursor = mydb.cursor()


name = st.text_input("NAME",'enter your name')
age = st.text_input("age",'enter your age')


# Read image as bytes then convert into image
uploaded_file = st.file_uploader("Choose a X-RAY Image.")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # read bytes as image:
    img = Image.open(io.BytesIO(bytes_data))
    # convert BGR to RGB
    img = img.convert("RGB")
    # convert image to array:
    img_array = np.array(img)
    # show image
    st.image(img_array)

if st.button("YOLOv8"):
    st.model = YOLO("keremberke/yolov8m-chest-xray-classification")
    st.model.overrides['conf'] = 0.25 
    result = st.model(img_array, device="CPU")
    processed_result = postprocess_classify_output(st.model, result=result[0])
    normal = f"{processed_result['NORMAL']:.2%}"
    pneumonia = f"{processed_result['PNEUMONIA']:.2%}"

    st.write(f"normal : {normal}")
    st.write(f"pneumonia : {pneumonia}")

    args = (name, age, bytes_data, normal, pneumonia)

    query = "insert into pneumonia_data.user_data values(%s, %s, %s, %s, %s)"

    cursor.execute(query, args)
    mydb.commit()
    

if st.button("CNN"):

    st.model = tf.keras.models.load_model("CNN.h5")
    img_array = cv2.resize(img_array, (224,224), interpolation=cv2.INTER_AREA)
    img_array = np.expand_dims(img_array, axis=0)

    with tf.device("/cpu:0"):
        result = st.model.predict(img_array)
    normal = f"{1 - result[0][0]:.2%}"
    pneumonia = f"{result[0][0]:.2%}"

    st.write(f"normal : {normal}")
    st.write(f"pneumonia : {pneumonia}")

    args = (name, age, bytes_data, normal, pneumonia)

    query = "insert into pneumonia_data.user_data values(%s, %s, %s, %s, %s)"

    cursor.execute(query, args)
    mydb.commit()

