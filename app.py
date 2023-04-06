import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

#model = keras.models.load_model('C:/FYP Emotion/Car-Speed-Detector')

# Load the vehicle detection classifier
car_cascade = cv2.CascadeClassifier('cars.xml')

# Create a VideoCapture object to read from video file or webcam
cap = cv2.VideoCapture(0) # Set to 0 for using the default webcam

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

# Loop through frames of the video
while(cap.isOpened()):
    # Read the frame
    ret, frame = cap.read()

    # If frame read successfully
    if ret == True:
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect vehicles in the frame
        cars = car_cascade.detectMultiScale(gray, 1.1, 3)

        # Draw rectangles around the detected vehicles
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Vehicle Detection', frame)

        # Exit if user presses 'q' key
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
