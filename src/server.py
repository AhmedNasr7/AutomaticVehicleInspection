import os 

from flask import Flask
from flask import request
from flask import jsonify

import cv2
from alpr import *
from models import *
import json



damage_part_model = Damage_Part_Model(damage_weights, parts_weights, device="cuda")
# damage_part = damage_part_model(image_path)


response = {
    "plate_check": False,
    "damage": False,
    "damage_parts": []
}

app = Flask(__name__)


@app.route('/upload_data', methods=['POST'])
def upload_data():
    print("here")
    request_data = request.json
    # print("request data: ", request.json)

    _input_plate_num = request_data["plate_num"]

    img_paths = []

    for i in range(4):
        path = request_data[str(i)]
        img_paths.append(path)

    
    ## plate number check


    for path in img_paths:
        plate_num = get_plate_number(path)
        if plate_num != _input_plate_num or plate_num == None:
            plate_check_res = False
            return jsonify(message = response)

        else:
            plate_check_res = True


    
    response["plate_check"] = plate_check_res # True

    ## plate number check done
    
    damage_parts = []
    for path in img_paths:
        _damage_part = damage_part_model(path)
        if _damage_part != None:
            if _damage_part[0] != "damage":
                damage_parts.extend(_damage_part)


    if len(damage_parts) == 0:
        response["damage"] = False

    else:
        response["damage"] = True
        response["damage_parts"] = damage_parts

    
    return jsonify(
        message = response
    )


if __name__ == "__main__":

    app.run(host='localhost', port=5000)