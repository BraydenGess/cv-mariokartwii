from keras.models import load_model
import cv2
import tensorflow as tf
import numpy as np
import h5py
from keras import backend as K

def imgtobinary(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(image, bg, scale=255)
    out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU)[1]
    return out_binary

def single_conversion(frame):
    array = np.ones(shape = (1,len(frame)*len(frame[0])))
    frame = frame//255
    count = 0
    for row in range(len(frame)):
        for col in range(len(frame[row])):
            data = frame[row][col]
            value = (data * 2) - 1
            array[0][count] = value
            count += 1
    return array

def predict():
    model = load_model('models/coursedetectionmodel')
    img = cv2.imread('/Users/bradygess/PycharmProjects/mariokartwii/audio/traincourserecognition/coursenametrainingimages/CoconutMall3.png')
    img = imgtobinary(img)
    arr = single_conversion(img)
    print(model.predict(arr,verbose=False))

#predict()
#exit()

#import tensorflow as tf

#model = tf.keras.models.load_model('models/coursedetectionmodel.h5')
#tf.keras.Model.save(model, 'models/my_saved_model')

def f(x):
    return 2*x

def g(y):
    return f(y)*f(y)

print(g(6))
