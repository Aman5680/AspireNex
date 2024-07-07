Face Recognition and Detection Software

Prerequisites
1. Install Python 3.x
2. Install the following Python libraries:
        1.OpenCV: pip install opencv-python
        2.TensorFlow: pip install tensorflow
        3.Keras: pip install keras
        4.NumPy: pip install numpy

File Structure
    Ensure the following directory structure:


FACE RECOGNITION AND FACE DETECTION/
├── haarcascade_frontalface_default.xml
├── Keras/
│   └── keras_model.h5
├── images/
│   └── [User Images]
├── [Face_Detection].py
└── [Face_Recognition].py

Step-by-Step Guide
1. Face Registration(Face_Detection.py)
This step involves capturing face images and saving them into a directory.

Usage:
1.Run the script.
2.Enter your name when prompted.
3.The script will capture 500 face images and store them in the images/your_name directory.

2. Now Visit the Site -> [https://teachablemachine.withgoogle.com/train/image]

Usage: 
1.Upload all captured images and change the class name according to Name.
2.After Uploading Click on Train Model.
3.Export Model in Tensorflow and paste it on Keras Folder.

2. Face Recognition(Face_Recognition.py)
This step involves recognizing faces from a video feed using a pre-trained model.

Usage:
Run the script.
The camera feed will open, and the model will recognize faces in real-time.
Press 'q' to quit the application.