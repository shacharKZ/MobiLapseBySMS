# MobiLapse Robot Platform repository

This repository is part of the [MobiLapse](https://github.com/MPTG94/Mobi-Lapse) project, specifically this repository
is dedicated to the Robot Platform code, including driving, direction, camera and file upload modules,
all exposed through a [flask](https://flask.palletsprojects.com/en/2.0.x/) python REST API

## Requirements

* This project was developed and tested on a Raspberry Pi 4 Model B
* Operating System: Raspberry Pi OS (64-bit) based on Debian 11 (Bullseye), kernel version: 5.10.63
* Additional needed libraries:
  * requests
  * flask
  * flask_cors
  * firebase_admin
  * opencv-python
  * numpy
* The robot platform also makes extensive use of Firebase services including Realtime Database and Cloud Storage
  
  So in order to run the project properly you will need a firebase.json file with information about your project (configurable in the config.py file)

## Running instructions

In order to run the project on an RPi supporting device, clone the repository using:

```git clone https://github.com/shacharKZ/MobiLapseBySMS.git mobi```

After cloning, change the working directory to the project directory:

```cd mobi```

Run the REST API (which will invoke the rest of the functionality) using:

```python3 app.py```

