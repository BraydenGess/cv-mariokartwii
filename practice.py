from keras.models import load_model
import cv2
import tensorflow as tf
import numpy as np
import h5py
from keras import backend as K

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = tf.graph_util.convert_variables_to_constants(
            session, input_graph_def, output_names, freeze_var_names)
        return frozen_graph

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

predict()
exit()

import tensorflow as tf

model = tf.keras.models.load_model('models/coursedetectionmodel.h5')
tf.keras.Model.save(model, 'models/my_saved_model')
