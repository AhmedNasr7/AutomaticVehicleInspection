import os 

from flask import Flask
from flask import request
from flask import jsonify

import cv2
from alpr import *
from models import *
import json




app = Flask(__name__)


@app.route('/upload_data', methods=['POST'])
def upload_data():
    print("here")
    # request_data = request.json()
    print("request data: ", request.json)

    ## Do processing here

    response = {
        
    }
    return jsonify(
        message = response
    )


if __name__ == "__main__":

    app.run(host='localhost', port=5000)