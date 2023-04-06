import cv2
import pytesseract
import numpy as np
import tensorflow as tf
from tensorflow import keras

#model = keras.models.load_model('C:/FYP Emotion/Car-Speed-Detector')

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Load the pre-trained car detection classifier
car_classifier = cv2.CascadeClassifier("cars.xml")

# Load the pre-trained brand detection classifier
brand_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Define the lower and upper bounds for the color of a blue car in the HSV color space
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

def detect_car(frame):
    # Convert the input frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect cars in the input frame
    cars = car_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    # Draw rectangles around the detected cars
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        car_roi_gray = gray[y:y+h, x:x+w]
        car_roi_color = frame[y:y+h, x:x+w]

        # Detect the brand of the car in the car region of interest (ROI)
        brand, brand_location = detect_brand(car_roi_color)

        # If a brand is detected, recognize it using Tesseract OCR
        if brand is not None:
            brand_text = recognize_text(car_roi_gray, brand_location)
            print(f"Brand: {brand_text}")

        # Detect the color of the car in the car region of interest (ROI)
        color = detect_color(car_roi_color)
        print(f"Color: {color}")

        car_detected = True
        print("A car was detected.")

    if not car_detected:
        print("No cars were detected.")

    return frame, car_detected

def detect_brand(frame):
    # Convert the input frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect brands in the input frame
    brands = brand_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    # Draw rectangles around the detected brands
    for (x, y, w, h) in brands:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        brand_roi_gray = gray[y:y+h, x:x+w]
        brand_roi_color = frame[y:y+h, x:x+w]

        return brand_roi_color, (x, y, w, h)

    return None, None

def recognize_text(frame, location):
    x, y, w, h = location

    # Crop the region of interest (ROI) around the text
    roi = frame[y:y + h, x:x + w]

    # Perform OCR on the ROI
    text = pytesseract.image_to_string(roi, config='--psm 6')

    return text

def detect_color(frame):
    # Convert the input frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the blue color range
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply the mask to the input frame
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert the masked frame to grayscale
    gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)

    # Calculate the mean of the grayscale image
    mean = cv2.mean(gray)[0]

    # If the mean is above a threshold, the car is considered blue
    if mean > 50:
        return "blue"
    else:
        return "unknown"

# Open the video capture object
cap = cv2.VideoCapture("cars.mp4")
while True: 
    # Read a frame from the video capture object 
    ret, frame = cap.read()
    # If the frame was not read successfully, break out of the loop
    if not ret:
        break

    # Detect cars in the frame
    frame, car_detected = detect_car(frame)

    # Display the resulting frame
    cv2.imshow("Car Detection", frame)

    # If the 'q' key is pressed, break out of the loop
    if cv2.waitKey(1) == ord('q'):
        break
# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
