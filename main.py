import numpy as np
import cv2
from imutils import contours
import numpy as np
from keras.preprocessing.image import load_img
from tensorflow import keras
import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageDraw, ImageFont
import os

model = load_model('saved_model.h5')
class_names = ['correct', 'not_a_hole', 'wrong']
full_image = cv2.imread(input('Input track membrane image: '))
original = full_image.copy()
mkms_per_pixel = round(
    40 / len(full_image[0]), 3), round(40 / len(full_image), 3)
gray = cv2.cvtColor(full_image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 120, 255, 1)
holes_number = 0
with open('results/correct_sizes.txt', 'w') as sizes_file:
    sizes_file.write('SIZES:\n')
cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
results = {'correct': 0, 'wrong': 0, 'not_a_hole': 0}
if len(cnts) == 2:
    cnts = cnts[0]
else:
    cnts = cnts[1]
cnts, _ = contours.sort_contours(cnts, method="left-to-right")
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    hole = original[y: y + h + 2, x: x + w + 2]
    cv2.imwrite('results/hole_{}.jpg'.format(holes_number), hole)
    image = Image.open('results/hole_{}.jpg'.format(holes_number))
    width, height = image.size
    image = image.resize((30, 30))
    image.save('results/hole_{}.jpg'.format(holes_number))
    predict_img = model.predict(tf.expand_dims(keras.preprocessing.image.img_to_array(
        load_img('results/hole_{}.jpg'.format(holes_number), target_size=(30, 30))), 0))
    os.remove('results/hole_{}.jpg'.format(holes_number))
    results[class_names[np.argmax(tf.nn.softmax(predict_img[0]))]] += 1
    if class_names[np.argmax(tf.nn.softmax(predict_img[0]))] != 'not_a_hole':
        holes_number += 1
        if class_names[np.argmax(tf.nn.softmax(predict_img[0]))] == 'correct':
            draw = ImageDraw.Draw(image)
            draw.line((0, 13, 28, 13), fill=(0, 255, 0), width=1)
            draw.line((13, 0, 13, 28), fill=(0, 255, 0), width=1)
            with open('results/correct_sizes.txt', 'a') as sizes_file:
                sizes_file.write(
                    f'hole_{holes_number}.jpg\tVERTICAL {round(mkms_per_pixel[0] * (height - 2), 2)} mkm\tHORIZONTAL {round(mkms_per_pixel[0] * (width - 2), 2)} mkm\n')
    image.save(
        f'results/{class_names[np.argmax(tf.nn.softmax(predict_img[0]))]}/hole_{holes_number}.jpg')
print(
    f'Total: {holes_number} holes. {results["correct"]} are correct and {results["wrong"]} are wrong')
print(
    f'Correct percentage: {round(results["correct"] / holes_number * 100, 2)}%')
print(f'Wrong percentage: {round(results["wrong"] / holes_number * 100, 2)}%')
