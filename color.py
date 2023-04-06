import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Define color and brand maps
COLOR_MAP = {0: 'black', 1: 'blue', 2: 'brown', 3: 'gray', 4: 'green', 5: 'orange', 6: 'red', 7: 'silver', 8: 'white', 9: 'yellow'}
BRAND_MAP = {0: 'Audi', 1: 'BMW', 2: 'Chevrolet', 3: 'Dodge', 4: 'Ford', 5: 'Honda', 6: 'Mercedes-Benz', 7: 'Nissan', 8: 'Toyota', 9: 'Volkswagen'}

# Load object detection model
MODEL_PATH = "models/MobileNetSSD_deploy"
model = cv2.dnn.readNetFromCaffe(f"{MODEL_PATH}.prototxt", f"{MODEL_PATH}.caffemodel")

# Load color classification model
COLOR_MODEL_PATH = "models/color_classification.h5"
color_model = tf.keras.models.load_model(COLOR_MODEL_PATH)

# Load brand recognition model
BRAND_MODEL_PATH = "models/brand_recognition.h5"
brand_model = tf.keras.models.load_model(BRAND_MODEL_PATH)


def detect_car(frame):
    # Preprocess the frame
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # Pass the blob through the object detection model
    model.setInput(blob)
    detections = model.forward()

    # Loop over the detections
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # Filter out weak detections
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            # Check if the detection is a car
            if idx == 7 or idx == 2:  # 7 for cars in real team videos and 2 for cars in uploaded videos
                # Get the bounding box for the detection
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Extract the car from the frame
                car = frame[startY:endY, startX:endX]

                # Estimate the speed of the car
                # (assuming the speed limit is 60 km/h and the car takes 1/30 of a second to pass through the frame)
                speed = 60 * (endX - startX) / (30 * car.shape[1])

                # Preprocess the car for color classification
                car_color = cv2.resize(car, (224,224))
                car_color = tf.keras.applications.mobilenet.preprocess_input(car_color)
                car_color = np.expand_dims(car_color, axis=0)

                # Predict the color of the car
                color_predictions = color_model.predict(car_color)
                color = np.argmax(color_predictions)

                # Preprocess the car for brand recognition
                car_brand = cv2.resize(car, (224,224))
                car_brand = tf.keras.applications.mobilenet.preprocess_input(car_brand)
                car_brand = np.expand_dims(car_brand, axis=0)

                # Predict the brand of the car
                brand_predictions = brand_model.predict(car_brand)
                brand = np.argmax(brand_predictions)

                # Draw the bounding box and put the results on the frame
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, f"Speed: {speed:.2f} km/h", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Map color label to color name
                color_name = COLOR_MAP[color]

                # Map brand label to brand name
                brand_name = BRAND_MAP[brand]

    return frame

# Test the function on a sample video
cap = cv2.VideoCapture("sample_video.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = detect_car(frame)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
