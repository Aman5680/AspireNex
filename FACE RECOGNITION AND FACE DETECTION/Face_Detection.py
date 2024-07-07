import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from keras.models import load_model

# Load the face detection model
facedetect = cv2.CascadeClassifier('FACE RECOGNITION AND FACE DETECTION/haarcascade_frontalface_default.xml')

# Open video capture
cap = cv2.VideoCapture(1)  # Try changing the index if necessary
cap.set(3, 640)
cap.set(4, 480)
font = cv2.FONT_HERSHEY_COMPLEX

# Load the face recognition model
model = load_model('FACE RECOGNITION AND FACE DETECTION/Keras/keras_model.h5')

# Compile the model if not compiled
if not hasattr(model, 'optimizer'):
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define the class names
def get_className(classNo):
    if classNo == 0:
        return "Tony Stark"
    elif classNo == 1:
        return "Elon Musk"

while True:
    success, imgOriginal = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    faces = facedetect.detectMultiScale(imgOriginal, 1.3, 5)
    for x, y, w, h in faces:
        crop_img = imgOriginal[y:y + h, x:x + w]
        img = cv2.resize(crop_img, (224, 224))
        img = img.reshape(1, 224, 224, 3)
        img = img / 255.0  # Normalize the image

        prediction = model.predict(img)
        classIndex = np.argmax(prediction)
        probabilityValue = np.amax(prediction)

        if classIndex in [0, 1]:
            cv2.rectangle(imgOriginal, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(imgOriginal, (x, y - 40), (x + w, y), (0, 255, 0), -1)
            cv2.putText(imgOriginal, str(get_className(classIndex)), (x, y - 10), font, 0.75, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(imgOriginal, str(round(probabilityValue * 100, 2)) + "%", (x, y + h + 30), font, 0.75, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Result", imgOriginal)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()