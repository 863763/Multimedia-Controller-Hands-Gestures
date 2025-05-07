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

#### 1. Learning data collection
Press "k" to enter the mode to save key points（displayed as MODE: Logging Key Point」）<br>
<img src="https://user-images.githubusercontent.com/37477845/102249074-4d78fc80-3f45-11eb-9c1b-3eb975798871.jpg" width="60%"><br><br>
If you press "0" to "9", the key points will be added to "model/point_history_classifier/point_history.csv" as shown below.<br>
1st column: Pressed number (used as class ID), 2nd and subsequent columns: Coordinate history<br>
<img src="https://user-images.githubusercontent.com/37477845/102345850-54ede380-3fe1-11eb-8d04-88e351445898.png" width="80%"><br><br>
The key point coordinates are the ones that have undergone the following preprocessing up to ④.<br>
<img src="https://user-images.githubusercontent.com/37477845/102244148-49e27700-3f3f-11eb-82e2-fc7de42b30fc.png" width="80%"><br><br>
In the initial state, 4 types of learning data are included: stationary (class ID: 0), clockwise (class ID: 1), counterclockwise (class ID: 2), and moving (class ID: 4). <br>
If necessary, add 5 or later, or delete the existing CSV data to prepare the training data.<br>
<img src="https://user-images.githubusercontent.com/37477845/102350939-02b0c080-3fe9-11eb-94d8-54a3decdeebc.jpg" width="20%">　<img src="https://user-images.githubusercontent.com/37477845/102350945-05131a80-3fe9-11eb-904c-a1ec573a5c7d.jpg" width="20%">　<img src="https://user-images.githubusercontent.com/37477845/102350951-06444780-3fe9-11eb-98cc-91e352edc23c.jpg" width="20%">　<img src="https://user-images.githubusercontent.com/37477845/102350942-047a8400-3fe9-11eb-9103-dbf383e67bf5.jpg" width="20%">

#### 2.Model training
Open "[point_history_classification.ipynb](point_history_classification.ipynb)" in Jupyter Notebook and execute from top to bottom.<br>
To change the number of training data classes, change the value of "NUM_CLASSES = 4" and <br>modify the label of "model/point_history_classifier/point_history_classifier_label.csv" as appropriate. <br><br>

#### X. Model structure
The image of the model prepared in "[point_history_classification.ipynb](point_history_classification.ipynb)" is as follows.
<img src="https://user-images.githubusercontent.com/37477845/102246771-7481ff00-3f42-11eb-8ddf-9e3cc30c5816.png" width="50%"><br>
The model using "LSTM" is as follows. <br>Please change "use_lstm = False" to "True" when using (tf-nightly required (as of 2020/12/16))<br>
<img src="https://user-images.githubusercontent.com/37477845/102246817-8368b180-3f42-11eb-9851-23a7b12467aa.png" width="60%">

# Application example

Here are some application examples.

* [Control DJI Tello drone with Hand gestures](https://towardsdatascience.com/control-dji-tello-drone-with-hand-gestures-b76bd1d4644f)
* [Classifying American Sign Language Alphabets on the OAK-D](https://www.cortic.ca/post/classifying-american-sign-language-alphabets-on-the-oak-d)

# Reference

* [MediaPipe](https://mediapipe.dev/)

# Author

Kazuhito Takahashi(<https://twitter.com/KzhtTkhs>)

# Translation & other improvements

Fadil Ahmed(<https://github.com/863763>)

# License

Multimedia-Controller-Hand-Gestures is under [GNU General Public License v3.0](LICENSE).
