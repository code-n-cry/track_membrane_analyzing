import cv2
import numpy
import numpy as np
from keras.preprocessing.image import load_img
from tensorflow import keras
import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import os
import xlsxwriter
from typing import Union
from imutils import contours


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

    def detect_holes(self):
        for image in self.images:
            print(image)
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
        results = []
        fig, ax = plt.subplots()
        worktable = xlsxwriter.Workbook('results/diameters.xlsx')
        worksheet = worktable.add_worksheet('Диаметры(МкМ)')
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        total_correct = 0
        header = worktable.add_format({'bold': True})
        worksheet.write('A1', 'ИЗОБРАЖЕНИЯ:', header)
        worksheet.write('B1', 'ДИАМЕТРЫ:', header)
        for ind, value in enumerate(self.images_data):
            img_res = {'correct': 0, 'wrong': 0, 'not_a_hole': 0}
            mks_per_pixel = round(value[2][0] / value[1][0], 3), round(value[2][1] / value[1][1], 3)
            for hole in self.holes[ind]:
                x, y, w, h = cv2.boundingRect(hole)
                hole = value[0][y: y + h + 2, x: x + w + 2]
                cv2.imwrite('results/hole_{}.jpg'.format(self.holes_number), hole)
                image = Image.open('results/hole_{}.jpg'.format(self.holes_number))
                width, height = image.size
                image = image.resize((30, 30))
                image.save('results/hole_{}.jpg'.format(self.holes_number))
                predict_img = self.model.predict(tf.expand_dims(keras.preprocessing.image.img_to_array(
                    load_img('results/hole_{}.jpg'.format(self.holes_number), target_size=(30, 30))), 0))
                os.remove('results/hole_{}.jpg'.format(self.holes_number))
                img_res[self.class_names[np.argmax(tf.nn.softmax(predict_img[0]))]] += 1
                if self.class_names[np.argmax(tf.nn.softmax(predict_img[0]))] != 'not_a_hole':
                    self.holes_number += 1
                    if self.class_names[np.argmax(tf.nn.softmax(predict_img[0]))] == 'correct':
                        total_correct += 1
                        draw = ImageDraw.Draw(image)
                        draw.line((2, height / 2, width - 2, height / 2), fill=(0, 255, 0), width=1)
                    data.append(round(mks_per_pixel[0] * (width - 2), 2))
                    worksheet.write(total_correct + 1, 0, f'hole_{self.holes_number}.jpg')
                    worksheet.write(total_correct + 1, 1, f'{round(mks_per_pixel[0] * (width - 2), 2)}')
                image.save(
                    f'results/{self.class_names[np.argmax(tf.nn.softmax(predict_img[0]))]}/hole_{self.holes_number}.jpg')
            results.append((self.images[ind], img_res))
        fig.set_figwidth(3)
        fig.set_figheight(6)
        for i in range(len(data)):
            ax.bar(i + 1, data[i])
        plt.savefig('results/plot.png')
        worktable.close()
        return self.holes_number, results


if __name__ == '__main__':
    a = Analyzer(['dataset/photo9.jpg', 'dataset/photo3.jpg', 'dataset/photo10.jpg'])
    a.detect_holes()
    a.sort_holes()
