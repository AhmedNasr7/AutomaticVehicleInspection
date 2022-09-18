#!/usr/bin/env python3


import requests
from pathlib import Path
import numpy as np
from datetime import datetime
import string
import time

from PIL import Image
from io import BytesIO


class Configs: 
    url = "https://api.platerecognizer.com/v1/plate-reader/"
    token = "d7ad93a31ab088a532040e45d4841b26acb6d0f1"


def get_plate_number(image_path):


    image = Image.open(image_path)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    results, plate_num = _get_plate_number_from_obj(img_byte_arr)

    return plate_num

    
    
def _get_plate_number_from_obj(image_object):
    
    response = requests.post(Configs.url,
        # data=dict(regions=regions),  # Optional
        files=dict(upload=image_object),
        headers={f'Authorization': f'Token {Configs.token}'})

    

    response = response.json()

    results = response['results']
    
    #print("results: ", results)
    #print("response: ", response)
    
    if len(results) > 0:
        plate_num = results[0]['plate'] ## assuming cropped image of one truck, TODO get the lower one
        plate_num = plate_num.upper()
    
    else:
        return None, None # not detected


    return results, plate_num



if __name__ == "__main__":

    image_path = "/app/data/car1.jpeg"
    # response = requests.get(image_url)

    image = Image.open(image_path)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    results, plate_num = get_plate_number(img_byte_arr)

    print(results, plate_num)