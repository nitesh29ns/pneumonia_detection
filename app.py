from src.pneumonia_classifier.pipeline.pipeline import PipeLine
from src.pneumonia_classifier.config.configuration import configration
from src.pneumonia_classifier.exception import classificationException
from src.pneumonia_classifier.constants import *
from src.pneumonia_classifier.utils.util import get_model_path, upload_data_to_db
import streamlit as st
import numpy as np
from PIL import Image
from ultralyticsplus import YOLO, postprocess_classify_output
import tensorflow as tf
import cv2
import io, sys
import base64

def start_pipeline():
    try:
        pipeline = PipeLine(config=configration(current_time_stamp=get_current_time_stamp()))
        pipeline.run()
    except Exception as e:
        raise classificationException(e, sys)

def main():
     
    st.set_page_config(layout="wide")

    with st.sidebar:
        st.header("About")
        st.write("""
            My Name is Nitesh Sharma and This is my Intership project under ineuron Intership.
            ***
            github :- https://github.com/nitesh29ns/pneumonia_detection/tree/main
                
            linkdin :- https://www.linkedin.com/in/nitesh-sharma-0a260b183/
            """)
          
    with st.container():
         
        st.title("Pneumonia Detection")
        st.write("""
        This app predict Percentage of Having Penumonia.
        ***
        """)

    with st.expander("Initiate CNN Pipeline..."):
            result = ""
            if st.button("Start Pipeline"):
                start_pipeline()
                result = "ML Pipeline Completed Successfully."
            st.success(result)


    html_temp = """
        <div style="background-color:tomato;padding:5px">
        <h2 style="color:white;text-align:center;"> Pneumonia Detection App </h2>
        </div>
        """

    st.markdown(html_temp,unsafe_allow_html=True)

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

    if st.button("YOLOv8_Model"):
        st.model = YOLO(YOLO_MODEL)
        st.model.overrides['conf'] = 0.25 
        result = st.model(img_array, device="CPU")
        processed_result = postprocess_classify_output(st.model, result=result[0])
        normal = f"{processed_result['NORMAL']:.2%}"
        pneumonia = f"{processed_result['PNEUMONIA']:.2%}"

        st.write(f"normal : {normal}")
        st.write(f"pneumonia : {pneumonia}")

        upload_data_to_db(name=name,age=age,bytes_data=bytes_data,normal=normal,pneumonia=pneumonia)

    if st.button("Custom_Train_CNN_Model"):

        model_path = get_model_path()
        st.model = tf.keras.models.load_model(model_path)
        img_array = cv2.resize(img_array, (224,224), interpolation=cv2.INTER_AREA)
        img_array = np.expand_dims(img_array, axis=0)

        with tf.device("/cpu:0"):
            result = st.model.predict(img_array)
        normal = f"{1 - result[0][0]:.2%}"
        pneumonia = f"{result[0][0]:.2%}"

        st.write(f"normal : {normal}")
        st.write(f"pneumonia : {pneumonia}")
        
        upload_data_to_db(name=name,age=age,bytes_data=bytes_data,normal=normal,pneumonia=pneumonia)


if __name__ == "__main__":
     main()




