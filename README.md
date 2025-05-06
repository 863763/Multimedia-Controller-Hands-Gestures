# Multimedia Controller using Custom Hand Gestures

Estimate hand pose using MediaPipe (Python version).
This is a sample program that recognises hand signs and finger gestures with a simple MLP using the detected key points.

**❗This is the English translated version of the [original repo](https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe/blob/main/README.md). All Content is translated to English along with comments and notebooks❗**

![Hands Gestures Recognition GIF](https://user-images.githubusercontent.com/37477845/102222442-c452cd00-3f26-11eb-93ec-c387c98231be.gif)

This repository contains the following contents:
- Sample program.
- Hand sign recognition model (TFLite).
- Finger gesture recognition model (TFLite).
- Learning data for hand sign recognition and notebook for learning.
- Learning data for finger gesture recognition and notebook for learning.

# Requirements

- Mediapipe 0.8.4
- OpenCV 4.6.0.66 or Later
- Tensorflow 2.9.0 or Later
- protobuf <3.20,>=3.9.2
- scikit-learn 1.0.2 or Later (only if you want to show the confusion matrix during training)
- matplotlib 3.5.1 or later (only if you want to show the confusion matrix during training)
