import cv2
import numpy
import numpy as np
from keras.preprocessing.image import load_img
from tensorflow import keras
import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageDraw
import os
from typing import Union
from imutils import contours
import base64


class Analyzer:
    def __init__(self, images: Union[list, str]):
        if isinstance(images, str):
            self.images = [images]
        else:
            self.images = images
        self.holes = []
        self.images_data = []
        self.holes_number = 0
        self.model = load_model('saved_model.h5')
        self.class_names = ['correct', 'not_a_hole', 'wrong']
        if not os.path.isdir('/results/'):
            os.mkdir('/results')

    def detect_holes(self):
        for image in self.images:
            full_image = numpy.asarray(Image.open(image))
            original = full_image.copy()
            gray = cv2.cvtColor(full_image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            canny = cv2.Canny(blurred, 120, 255, 1)
            cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            cnts, _ = contours.sort_contours(cnts, method="left-to-right")
            self.holes.append(cnts)
            self.images_data.append([original, (len(full_image[0]), len(full_image)), (40, 40)])

    def sort_holes(self):
        data = []
        results = {'correct': [], 'wrong': [], 'digits': []}
        for ind, value in enumerate(self.images_data):
            img_res = {'correct': 0, 'wrong': 0, 'not_a_hole': 0}
            mks_per_pixel = round(value[2][0] / value[1][0], 3)
            for hole in self.holes[ind]:
                x, y, w, h = cv2.boundingRect(hole)
                hole = value[0][y: y + h, x: x + w]
                cv2.imwrite('results/hole_{}.jpg'.format(self.holes_number), hole)
                image = Image.open('results/hole_{}.jpg'.format(self.holes_number))
                diameter = mks_per_pixel * len(hole[0])
                image = image.resize((30, 30))
                image.save('results/hole_{}.jpg'.format(self.holes_number))
                predict_img = self.model.predict(
                    tf.expand_dims(keras.preprocessing.image.img_to_array(
                        load_img('results/hole_{}.jpg'.format(self.holes_number),
                                 target_size=(30, 30))), 0))
                class_name = self.class_names[np.argmax(tf.nn.softmax(predict_img[0]))]
                img_res[class_name] += 1
                if class_name != 'not_a_hole':
                    self.holes_number += 1
                    if class_name == 'correct':
                        draw = ImageDraw.Draw(image)
                        draw.line((0, 15, 30, 15), fill=(0, 255, 0), width=1)
                    with open('results/hole_{}.jpg'.format(self.holes_number), 'rb') as r_img:
                        img_data = r_img.read()
                        img = base64.urlsafe_b64encode(img_data).decode('ascii')
                    os.remove('results/hole_{}.jpg'.format(self.holes_number))
                    data.append(round(diameter, 2))
                    results[class_name].append({f'hole_{self.holes_number}.jpg': img})
            results['digits'].append(img_res)
        return results, data
