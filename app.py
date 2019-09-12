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
