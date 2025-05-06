# Multimedia Controller using Custom Hand Gestures

Estimate hand pose using MediaPipe (Python version).
This is a sample program that recognizes hand signs and finger gestures with a simple MLP using the detected key points.

**❗This is the English translated version of the [original repo](https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe/blob/main/README.md). All Content is translated to English along with comments and notebooks❗**

![Hands Gestures Recognition GIF](https://user-images.githubusercontent.com/37477845/102222442-c452cd00-3f26-11eb-93ec-c387c98231be.gif)

This repository contains the following contents:
- Sample program.
- Hand sign recognition model (TFLite).
- Finger gesture recognition model (TFLite).
- Learning data for hand sign recognition and notebook for learning.
- Learning data for finger gesture recognition and notebook for learning.

![Hands Gestures Recognition GIF](<Resources/HGR GIF.gif>)
<!-- ![Hands Gestures Recognition GIF](<Resources/HGR GIF.gif>) -->

# Requirements

- Mediapipe 0.8.4
- OpenCV 4.6.0.66 or Later
- Tensorflow 2.9.0 or Later
- protobuf <3.20,>=3.9.2
- scikit-learn 1.0.2 or Later (only if you want to show the confusion matrix during training)
- matplotlib 3.5.1 or later (only if you want to show the confusion matrix during training)

# Demonstration

Here's how to run the demo using your webcam.

````python
python main.py 
````
Here is how to run the demo using Docker and a webcam.

````bash
docker build -t hand_gesture .

host +local: && \
docker run --rm -it \
--device /dev/video0:/dev/video0 \
-v `pwd`:/home/user/workdir \
-v /tmp/.X11-unix/:/tmp/.X11-unix:rw \
-e DISPLAY=$DISPLAY \
hand_gesture:latest

python main.py 
````

The following options can be specified when running the demo:

- --device\
Specifying the camera device number (Default：0)
- --width\
Width at the time of camera capture (Default：960)
- --height\
Height at the time of camera capture (Default：540)
- --use_static_image_mode\
Whether to use the static_image_mode option for MediaPipe inference (Default： Unspecified)
- --min_detection_confidence\
Detection confidence threshold (Default：0.5)
- --min_tracking_confidence\
Tracking confidence threshold (Default：0.5)
