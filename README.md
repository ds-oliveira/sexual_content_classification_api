# Building a Sexual Content Filter Using Python, Flask, and Docker

Hi guys, a lot of people on the internet are looking for some way to analyze images and predict if it is sexual content or not (everyone by its own motivations). However, it's almost impossible to do it without thousands of images to train a convolutional neural network model. I'm making this article to show you that you can have a simple application that can do it for you, without worrying about neural networks stuff. We're going to use a convolutional neural network, but the model will be already trained, so you don't need to worry.

### What am I going to learn?
- How to create a Python Rest API with Flask.
- How to create a simple service to check if a content is sexual or not.


### Requirements:
- Docker Installed
- Python 3 Installed
- Pip Installed

## Let's get our hands dirty!

### Creating the directory structure
- Open your favorite terminal.
- Create a project's root directory where we're going to put the project's files.
```
mkdir sexual_content_classification_api
```
- Let's navigate to the folder we just created and create some files.
```
cd sexual_content_classification_api
touch app.py
touch Dockerfile
```
- Open the project's root directory with your favorite code editor.

### Creating a Flask API
- Open the `app.py` file in your code editor.
- Let's code our prediction and health check routes.

`app.py`
```
import requests
import uuid
import os
from flask import Flask, request
from open_nsfw_python3 import NSFWClassifier


__name__ = 'sexual_content_classification_api'
app = Flask(__name__)
classifier = NSFWClassifier()


@app.route('/health', methods=['GET'])
def health():
    return {
        "status": "OK"
    }, 200


@app.route('/classify', methods=['GET'])
def classify_image():
    try:
        url = request.json['image']
        print('Downloading the image: {}'.format(url))
        r = requests.get(url, allow_redirects=True)
        hash = str(uuid.uuid4())
        open(hash, 'wb').write(r.content)
        score = classifier.get_score(hash)
        os.remove(hash)
        return {
            "score": score
        }, 200
    except Exception as err:
        return str(err), 400
```

### Creating the Docker environment
- Let's implement our Dockerfile to install the required python modules and to run the application. 

`Dockerfile`
```
FROM python:3.7.4
WORKDIR /app
COPY ./ ./
RUN pip install open-nsfw-python3==0.0.5
RUN pip install uuid==1.30
RUN pip install requests==2.22.0
RUN pip install flask==1.1.1
RUN apt update && apt install caffe-cpu --yes

ENV PYTHONPATH=/usr/lib/python3/dist-packages:
ENV FLASK_APP=app.py

CMD flask run -h 0.0.0.0 -p 80
```
- Building the docker image.
```
docker build -t sexual_content_classification_api:latest .
```
- Starting a container on the port 80 of your local machine.
```
docker run -t -p 80:80 sexual_content_classification_api:latest
```
- The API should be running and ready to receive requests.

### Testing our API
- Testing if the API is online. I'm using curl here, but you're free to use your favorite HTTP client.
```
curl localhost/health
```
- Expected response
```
{"status":"OK"}
```
- Testing the classification route.
```
curl -X GET localhost/classify -H 'Content-Type: application/json' -d '{"image":"https://helpx.adobe.com/content/dam/help/en/stock/how-to/visual-reverse-image-search/jcr_content/main-pars/image/visual-reverse-image-search-v2_intro.jpg"}'
```
- Expected response
```
{"score":0.0013733296655118465}
```
- The score attribute in the response object is a guessing rate from 0 to 1, where 0 is equal to `no sexual content`, and 1 is equal to `sexual content`.


That's all folks! I hope you enjoyed this article, please let me know if you have some doubt.

You can get the source code of this article in the following link:

https://github.com/ds-oliveira/sexual_content_classification_api
