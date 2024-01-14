import cv2
import streamlit as st

# File paths
yolov4_weights_path = 'yolov4.weights'
yolov4_cfg_path = 'yolov4.cfg'

# Load YOLOv4 model
net = cv2.dnn.readNet(yolov4_weights_path, yolov4_cfg_path)

# Streamlit app code
st.write(f"YOLOv4 model initialized with weights: {yolov4_weights_path}")

# Rest of your Streamlit app code...
