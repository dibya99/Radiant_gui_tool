#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 21:36:24 2020

@author: dibya
"""

import cv2

import pathlib
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from IPython.display import display

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile



class object_detector:


    def __init__(self):
        self.PATH_TO_LABELS = '/home/dibya/GUI_tool_Radiant/models/research/object_detection/data/mscoco_label_map.pbtxt'
        self.category_index = label_map_util.create_category_index_from_labelmap(self.PATH_TO_LABELS, use_display_name=True)
        self.threshold_factor=0.7
        self.class_selector=1
        #self.show_inference("/home/dibya/GUI_tool_Radiant/models/research/object_detection/test_images/image1.jpg")

    def set_model_name(self,name):
        self.model_name=name
        self.detection_model=self.load_model(self.model_name)

    def set_threshold(self,value):
        self.threshold_factor=value

    def set_class_selector(self,v):
        self.class_selector=v

    def load_model(self,model_name):
        #base_url = 'http://download.tensorflow.org/models/object_detection/'
        #model_file = model_name + '.tar.gz'
        #model_dir = tf.keras.utils.get_file(
        #        fname=model_name,
        #        origin=base_url + model_file,
        #        untar=True)

        model_dir = model_name+"/saved_model"

        model = tf.saved_model.load(str(model_dir))
        model = model.signatures['serving_default']

        return model


    def run_inference_for_single_image(self,model, image):
        image = np.asarray(image)
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis,...]

        # Run inference
        output_dict = model(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(output_dict.pop('num_detections'))
        output_dict = {key:value[0, :num_detections].numpy()
                     for key,value in output_dict.items()}
        output_dict['num_detections'] = num_detections

        # detection_classes should be ints.
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

        # Handle models with masks:
        if 'detection_masks' in output_dict:
            # Reframe the the bbox mask to the image size.
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    output_dict['detection_masks'], output_dict['detection_boxes'],
                    image.shape[0], image.shape[1])
            detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                               tf.uint8)
            output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

        return output_dict

    def show_inference(self, image_path):
        try:
            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            image_np = np.array(Image.open(image_path))
            #print(image_np)
            # Actual detection.
            output_dict = self.run_inference_for_single_image(self.detection_model, image_np)
            #print(output_dict)
            # Visualization of the results of a detection.

            boxes =np.squeeze(output_dict['detection_boxes'])
            scores = np.squeeze(output_dict['detection_scores'])
            classes =np.squeeze(output_dict['detection_classes'])

            print(type(boxes))
            print(type(scores))
            print(type(classes))


            if (boxes.size == 1 or scores.size==1 or classes.size == 1):
                print('Hi')
                boxes=np.asarray([boxes])
                scores=np.asarray([scores])
                classes=np.asarray([classes])

            print(scores[0])

            print(boxes)
            print(scores)
            print(classes)

            print(type(boxes))
            print(type(scores))
            print(type(classes))


            indices = np.argwhere(classes ==  self.class_selector)
            boxes = np.squeeze(boxes[indices])
            scores = np.squeeze(scores[indices])
            classes = np.squeeze(classes[indices])

            if (boxes.size == 1 or scores.size==1 or classes.size == 1):
                print('Hi')
                boxes=np.asarray([boxes])
                scores=np.asarray([scores])
                classes=np.asarray([classes])

            print(boxes)
            print(scores)
            print(classes)



            #print(indices)



            vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    boxes,
                    classes,
                    scores,
                    self.category_index,min_score_thresh=self.threshold_factor,
                    instance_masks=output_dict.get('detection_masks_reframed', None),
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=4,
                    line_thickness=8)
            #print(image_np)
            #img_cv = cv2.resize(image_np,(200,200))
            #plt.imshow(img_cv)
            #display(Image.fromarray(image_np))
            #output=Image.fromarray(image_np)
            return image_np
            #output.show()

        except Exception as e:
             exc_type, exc_obj, exc_tb = sys.exc_info()
             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
             print(exc_type, fname, exc_tb.tb_lineno)
             return image_np

if __name__ == "__main__":
    obj=object_detector()
    #obj.show_inference(detection_model,"/home/dibya/GUI_tool_Radiant/models/research/object_detection/test_images/image1.jpg")
  #  print("HI")
