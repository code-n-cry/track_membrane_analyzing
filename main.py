import numpy as np
import cv2
from imutils import contours
import numpy as np
from keras.preprocessing.image import load_img
from tensorflow import keras
import tensorflow as tf
from keras.models import load_model
from PIL import Image
import os


model = load_model('saved_model.h5')
class_names = ['correct', 'wrong']
full_image = cv2.imread(input('Input track membrane image: '))
original = full_image.copy()
gray = cv2.cvtColor(full_image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 120, 255, 1)
holes_number = 0
cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
results = {'correct': 0, 'wrong': 0}
if len(cnts) == 2:
    cnts = cnts[0]
else:
    cnts = cnts[1]
cnts, _ = contours.sort_contours(cnts, method="left-to-right")
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    holes = full_image[y: y + h + 2, x: x + w + 2]
    hole = original[y: y + h + 2, x: x + w + 2]
    cv2.imwrite('results/hole_{}.jpg'.format(holes_number), hole)
    image = Image.open('results/hole_{}.jpg'.format(holes_number))
    image = image.resize((30, 30))
    image.save('results/hole_{}.jpg'.format(holes_number))
    img_array = load_img(
        'results/hole_{}.jpg'.format(holes_number), target_size=(30, 30))
    img_array = keras.preprocessing.image.img_to_array(img_array)
    img_array = tf.expand_dims(img_array, 0)
    predict_img = model.predict(img_array)
    label = tf.nn.softmax(predict_img[0])
    os.remove('results/hole_{}.jpg'.format(holes_number))
    image.save(f'results/{class_names[np.argmax(label)]}/hole_{holes_number}.jpg')
    results[class_names[np.argmax(label)]] += 1
    holes_number += 1
print(f'Total: {holes_number} holes. {results["correct"]} are correct and {results["wrong"]} are wrong')
print(f'Correct percentage: {round(results["correct"] / holes_number * 100, 2)}%')
print(f'Wrong percentage: {round(results["wrong"] / holes_number * 100, 2)}%')
