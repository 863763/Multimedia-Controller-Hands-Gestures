# Multimedia Controller using Custom Hand Gestures

Estimate hand pose using MediaPipe (Python version).
This is a sample program that recognizes hand signs and finger gestures with a simple MLP using the detected key points.

**❗This is the English translated version of the [original repo](https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe/blob/main/README.md). All Content is translated to English along with comments and notebooks❗**

![Hands Gestures Recognition GIF](https://user-images.githubusercontent.com/37477845/102222442-c452cd00-3f26-11eb-93ec-c387c98231be.gif)

This repository contains the following contents:
* Sample program.
* Hand sign recognition model (TFLite).
* Finger gesture recognition model (TFLite).
* Learning data for hand sign recognition and notebook for learning.
* Learning data for finger gesture recognition and notebook for learning.

# Requirements

* Mediapipe 0.8.4
* OpenCV 4.6.0.66 or Later
* Tensorflow 2.9.0 or Later
* protobuf <3.20,>=3.9.2
* scikit-learn 1.0.2 or Later (only if you want to show the confusion matrix during training)
* matplotlib 3.5.1 or later (only if you want to show the confusion matrix during training)

# Demonstration

Here's how to run the demo using your webcam.

```bash
python main.py
```
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

* --device\
Specifying the camera device number (Default：0)
* --width\
Width at the time of camera capture (Default：960)
* --height\
Height at the time of camera capture (Default：540)
* --use_static_image_mode\
Whether to use the static_image_mode option for MediaPipe inference (Default： Unspecified)
* --min_detection_confidence\
Detection confidence threshold (Default：0.5)
* --min_tracking_confidence\
Tracking confidence threshold (Default：0.5)

# Directory
<pre>
│  main.py
│  keypoint_classification.ipynb
│  point_history_classification.ipynb
│
├─model
│  ├─keypoint_classifier
│  │  │  keypoint.csv
│  │  │  keypoint_classifier.hdf5
│  │  │  keypoint_classifier.py
│  │  │  keypoint_classifier.tflite
│  │  └─ keypoint_classifier_label.csv
│  │
│  └─point_history_classifier
│      │  point_history.csv
│      │  point_history_classifier.hdf5
│      │  point_history_classifier.py
│      │  point_history_classifier.tflite
│      └─ point_history_classifier_label.csv
│
└─utils
    └─cvfpscalc.py
</pre>
### main.py
This is a sample program for inference.<br>
In addition, learning data (key points) for hand sign recognition,<br>
You can also collect training data (index finger coordinate history) for finger gesture recognition.

### keypoint_classification.ipynb

This is a model training script for hand sign recognition.

### point_history_classification.ipynb

This is a model training script for finger gesture recognition.

### model/keypoint_classifier

This directory stores files related to hand sign recognition.<br>
The following files are stored.

* Training data(keypoint.csv)
* Trained model(keypoint_classifier.tflite)
* Label data(keypoint_classifier_label.csv)
* Inference module(keypoint_classifier.py)

### model/point_history_classifier

This directory stores files related to finger gesture recognition.<br>
The following files are stored.

* Training data(point_history.csv)
* Trained model(point_history_classifier.tflite)
* Label data(point_history_classifier_label.csv)
* Inference module(point_history_classifier.py)

### utils/cvfpscalc.py
This is a module for FPS measurement.

# Training

Hand sign recognition and finger gesture recognition can add and change training data and retrain the model.

### Hand sign recognition training

#### 1.Learning data collection
Press "k" to enter the mode to save key points（displayed as MODE:Logging Key Point」）<br>
