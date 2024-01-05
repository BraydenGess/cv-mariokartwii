from tools.imagemanipulation import *
from sklearn.model_selection import train_test_split
from keras.layers import Dense
from keras.models import Sequential
import numpy as np
import tensorflow as tf
from keras.models import load_model


model_path = '/Users/bradygess/PycharmProjects/mariokartwii/characterselection/vehicles/vehicledetection2.h5'
model = load_model(model_path)
new_path = 'models/vehicle2detectionmodel'
tf.keras.Model.save(model,new_path)

