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
# from detectron2.data import MetadataCatalog, DatasetCatalog
# from detectron2.engine import DefaultTrainer
from detectron2.utils.visualizer import ColorMode
# from detectron2.evaluation import COCOEvaluator, inference_on_dataset
# from detectron2.data import build_detection_test_loader
from pathlib import Path

## configs: 
model = None
classes = ["damage"]

class Metadata:
    def get(self, _):
        return classes # your class labels


def get_model(weights):

    model_config = get_cfg()
    model_config.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")) # Load pretrained model from model zoo. You can try other models, maybe you can get better results :)
    # model_config.DATASETS.TRAIN = ("car_dataset_train",)
    # model_config.DATASETS.TEST = ("car_dataset_val",)
    model_config.DATALOADER.NUM_WORKERS = 4
    # model_config.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Load weights from model zoo

    # model_config.SOLVER.IMS_PER_BATCH = 4
    # model_configcfg1.SOLVER.BASE_LR = 0.001  
    # model_config.SOLVER.MAX_ITER = 600 
    # model_config.SOLVER.GAMMA = 0.05
    model_config.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128  
    model_config.MODEL.ROI_HEADS.NUM_CLASSES = 1 
    model_config.MODEL.RETINANET.NUM_CLASSES = 1
    model_config.TEST.EVAL_PERIOD = 100
    model_config['MODEL']['DEVICE']= 'cuda'
    # model_config.OUTPUT_DIR= "/content/output"

    model_config.MODEL.WEIGHTS = weights # Load your previously trained weights

    model_config.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # You can try some other thresholds
    # model_config.DATASETS.TEST = ("car_dataset_val", )
    predictor = DefaultPredictor(model_config)

    return predictor


def inference(image_path, save_image=False, save_path=""):

    global model
    image = cv2.imread(image_path)
    # image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    outputs = model(image)
    v = Visualizer(image[:, :, ::-1],
                    metadata=Metadata, 
                    scale=0.5, 
                    instance_mode=ColorMode.IMAGE_BW  
    )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    output_image = out.get_image()[:, :, ::-1]

    if save_image:
        if len(save_path) > 0:
            cv2.imwrite(save_path, output_image)
        else:
            cv2.imwrite("output.jpg", output_image)
    
    return output_image




if __name__ == __main__:

    image_path = "./1.jpg"
    weights = "./Detectron2_damage.pth"

    model = get_model(weights)

    output_image = inference(image_path, save_image=True, save_path=Path(image_path).stem + "_output.jpg")

    