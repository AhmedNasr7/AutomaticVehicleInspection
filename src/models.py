#!/usr/bin/env python3
import detectron2
from detectron2.utils.logger import setup_logger

setup_logger()
import numpy as np
import os, json, cv2, random
import matplotlib.pyplot as plt
import skimage.io as io

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode


from pathlib import Path
from time import time


## configs: 

class Metadata:
    def __init__(self, classes):
        self.classes = classes
        
    def get(self, classes, cls):
        return self.classes # your class labels


class Model:

    def __init__(self, weights = "", device="cuda") -> None:

        self.model = None
        self.weights = weights


        self.classes = []
        self.classes_num = len(self.classes)
        self.device = device
        # self.model = self.get_model(self.weights)
        self.metadata = Metadata(self.classes)

        self.save_path = "/app/output_model/"



    
    def get_model(self, weights):

        model_config = get_cfg()
        model_config.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")) # Load pretrained model from model zoo. You can try other models, maybe you can get better results :)
        # model_config.DATALOADER.NUM_WORKERS = 4

        model_config.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128  

        model_config.MODEL.ROI_HEADS.NUM_CLASSES = self.classes_num
        model_config.MODEL.RETINANET.NUM_CLASSES = self.classes_num
        # model_config.TEST.EVAL_PERIOD = 100
        model_config['MODEL']['DEVICE']= self.device

        model_config.MODEL.WEIGHTS = weights # Load your previously trained weights

        model_config.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # You can try some other thresholds
        predictor = DefaultPredictor(model_config)

        return predictor


    def __call__(self, image_path,  save_image=True):

        t0 = time()


        output_image_path = self.save_path + Path(image_path).name

        image = cv2.imread(image_path)
        outputs = self.model(image)
        v = Visualizer(image[:, :, ::-1],
                        metadata=self.metadata, 
                        scale=1.0, 
                        instance_mode=ColorMode.IMAGE
        )

        print("output: ", outputs["instances"])
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        output_image = out.get_image()

        # print("DEBUG: image shape", output_image.shape)

        if save_image:
            print(output_image_path)
            cv2.imwrite(output_image_path, output_image)
 
        t1 = time()

        print("model inference time: ", t1 - t0)
        return output_image



class Damage_Model(Model):
    def __init__(self, weights="", device="cuda") -> None:
        super().__init__(weights, device)

        damage_classes = ["damage"]
        # part_classes = ["cheadlamp", "rear_bumper", "door", "hood", "front_bumper"]

        self.classes = damage_classes
        self.classes_num = len(self.classes)

        self.model = self.get_model(self.weights)
  
        self.metadata = Metadata(self.classes)

        self.class_mapping = {0: 'damage'}




class Part_Model(Model):
    def __init__(self, weights="", device="cuda") -> None:
        super().__init__(weights, device)

        part_classes = ["cheadlamp", "rear_bumper", "door", "hood", "front_bumper"]

        self.classes = part_classes
        self.classes_num = len(self.classes)

        self.model = self.get_model(self.weights)

        self.metadata = Metadata(self.classes)

        self.class_mapping = {0:'headlamp',1:'rear_bumper', 2:'door', 3:'hood', 4: 'front_bumper'}




if __name__ == "__main__":


    image_path = "/app/data/Car2.jpg"
    damage_weights = "/app/model/Detectron2_damage.pth"
    parts_weights = "/app/model/Detectron2_part.pth"

    damage_model = Damage_Model(weights=damage_weights, device="cpu")

    t0 = time()
    parts_model = Part_Model(weights=parts_weights, device="cpu")

    print("model loading time: ", time() - t0)

    # output_image = damage_model(image_path)
    image = parts_model(image_path=image_path)

        