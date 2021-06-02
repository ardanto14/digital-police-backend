# Digital Police Backend Repository

Backend server for Digital Police Application

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

##### Classifying weights link : [in_progress](about:blank)
##### API Documentation : [in_progress](about:blank)