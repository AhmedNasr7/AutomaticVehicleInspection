import os 

from flask import Flask
from flask import request
from flask import jsonify

import cv2
from alpr import *
from models import *
import json


damage_weights = "/app/model/damage_2.pth"
parts_weights = "/app/model/parts_model_final.pth"

damage_part_model = Damage_Part_Model(damage_weights, parts_weights, device="cuda")
# damage_part = damage_part_model(image_path)


response = {
    "license_check": False,
    "damage": False,
    "damage_parts": []
}

app = Flask(__name__)


@app.route('/upload_data', methods=['POST'])
def upload_data():
    # print("here")

    response = {
        "license_check": False,
        "damage": False,
        "damage_parts": []
        }

    request_data = request.json
    # print("request data: ", request.json)

    print("body: ", request_data)

    _input_plate_num = request_data["li"]



    img_paths = [] # request_data["files"]

    for f in request_data["files"]:
        path = "/app/uploads/" + f
        img_paths.append(path)

    
    ## plate number check


    for path in img_paths:
        plate_num = get_plate_number(path)
        print(f"detected plate number: {plate_num} for path: path: {path}")


        if plate_num != _input_plate_num:
            plate_check_res = False
            return jsonify(message = response)

        else:
            plate_check_res = True


    
    response["license_check"] = plate_check_res # True

    ## plate number check done
    
    damage_parts = []
    for path in img_paths:
        _damage_part = damage_part_model(path)
        print("debug, damage: ", _damage_part)
        if _damage_part != None:
            # if _damage_part[0] != "damage":
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

