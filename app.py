import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Load YOLOv4 model
yolov4_weights_path = 'yolov4.weights'
yolov4_cfg_path = 'yolov4.cfg'

net = cv2.dnn.readNet(yolov4_weights_path, yolov4_cfg_path)
st.write(f"YOLOv4 model initialized with weights: {yolov4_weights_path}")
classes = []

with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f]

# Function to perform object detection with Non-Maximum Suppression (NMS)
def detect_objects(image, confidence_threshold=0.5, nms_threshold=0.4):
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_names = net.getUnconnectedOutLayersNames()
    detections = net.forward(layer_names)

    height, width, _ = image.shape

    boxes = []
    confidences = []
    class_ids = []

    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > confidence_threshold:
                box = obj[0:4] * np.array([width, height, width, height])
                (x, y, w, h) = box.astype("int")

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply NMS
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

    return boxes, confidences, class_ids, indices

# Function to draw bounding boxes on the image
def draw_boxes(image, boxes, confidences, class_ids, indices):
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    for i in indices:
        i = i[0] if isinstance(i, (list, tuple)) and len(i) > 0 else i  # Unpack the index from the iterable

        box = boxes[i]
        confidence = confidences[i]
        class_id = class_ids[i]

        label = classes[class_id]
        color = colors[class_id]

        (x, y, w, h) = box
        x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)

        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, f"{label}: {confidence:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)



# Streamlit app
def main():
    st.title("YOLOv4 Object Detection App")

    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)

        st.image(image, caption="Uploaded Image.", use_column_width=True)

        if st.button("Detect Objects"):
            # Perform object detection with NMS
            boxes, confidences, class_ids, indices = detect_objects(image)

            # Draw bounding boxes on the image
            draw_boxes(image, boxes, confidences, class_ids, indices)

            # Display results
            st.image(image, caption="Detected Objects.", use_column_width=True)

if __name__ == '__main__':
    main()
