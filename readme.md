# Digital Police Backend Repository

Backend server for Digital Police Application

## HOW TO RUN

---
**NOTE**
How to Run steps assume that you are using python 3 and linux based OS

---
### How to Run This (Without Docker)

1. Clone this repository.
1. Create a new python virtual environment ``` python3 -m venv env ```.
1. Enter that virtual environment ``` source env/bin/activate ```.
1. Run this code to install all dependency ``` pip install -r requirements.txt ```.
1. Make sure to create ```.env``` file. There's an example in the ```.env.example```.
1. Download the classifying weights link in the link provided below, and put it at the project root folder (same level with ```manage.py```, ```requirements.txt```, ```Dockerfile```, etc). Make sure you name it ```classify_weights_tf.h5```
1. Download the credentials and put it at the project root folder and name it ```credentials.json```. You can follow [this link](https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python) to get the json file.
1. Run a database migration with ```python manage.py migrate```
1. Run ```python manage.py runserver```, and the webserver will run on port 8000 on your localhost.
1. All endpoint will be in backend documentation
1. To test a video, open ```http://localhost:8000``` and choose video that you want to categorize, then click upload new video. If true returned, then the video contains crime activity, and will be uploaded to firebase storage, if false, then the video doesn't contain crime activity.

### How to Run This (With Docker, and PostgreSQL database)
1. Clone this repository.
1. Create ```.env``` file. There's an example in the ```.env.example```. Set the ```PRODUCTION``` variable to ```TRUE```
1. Download the classifying weights link in the link provided below, and put it at the project root folder (same level with ```manage.py```, ```requirements.txt```, ```Dockerfile```, etc). Make sure you name it ```classify_weights_tf.h5```
1. Download the credentials and put it at the project root folder and name it ```credentials.json```. You can follow [this link](https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python) to get the json file.
1. run ```docker-compose up -d```.
1. Run a database migration by entering bash with ```docker exec -it {your_container_id} /bin/bash``` and run ```python manage.py migrate```. You shouldn't do this again if you already did this before.

## ACCESSING ADMIN PAGE
---
**NOTE**
1. To access built in django admin page, first you should create a superuser. Run ```python manage.py createsuperuser``` and write the desired username and password, email is optional. Note that if you are using docker, access the container bash with ```docker exec -it {your_container_id} /bin/bash```.

---
Admin page purpose is to manage all entity on the database. To know all the table in the database, follow the database design documentation.

### How to Add FCM Devices to Get Notification if Crime Detected
1. Access ```http://localhost:8000/admin/``` to go to the admin page.
1. Login with superuse credential.
1. To get a notification about crime happening, user must add FCM Devices. The required fields are ```Name (unique)```, ```Registration Token```, and ```Type```. To get device registration token, follow [this guide](https://firebase.google.com/docs/cloud-messaging/android/client).
1. Click Save to save the FCM Device. To test this, open ```http://localhost:8000``` and choose video that you want to categorize, then click upload new video. If true returned, then the notification will be send to your device.


### EXTRA NOTE
- CCTV Object would be automatically created if you predict the video via ```http://localhost:8000```. The name would be dummy, with latitude and longitude zero, with a city named dummy.
- Predicting for the first time can take a long time because it needs to download the C3D weights and mean.


##### Classifying weights link : [Drive Link](https://drive.google.com/file/d/1Whn_Hj8xOxd1Fl5z6Jcbr7RMgZsuvW4B/view?usp=sharing)
##### API Documentation : [Drive Link](https://drive.google.com/file/d/1Hdzv-wOX2Jf_vaJF8i_7RoVWctbi-vIn/view?usp=sharing)
##### Datbase Design Documentation : [Drive Link](https://drive.google.com/file/d/1wul2BK2_o7vwZi8LWkI9MRBhgdEA4iWC/view?usp=sharing)