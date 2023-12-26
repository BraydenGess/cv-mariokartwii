from tools.imagemanipulation import *
import numpy as np

def filter_frame(frame,coordinates,filter):
    [x0,x1,y0,y1] = coordinates
    #new_frame = frame[y0:y1,x0:x1].copy()
    new_frame = frame.copy()
    if filter == 'imgtobinary':
        new_frame = imgtobinary(new_frame)
    return new_frame

def single_conversion(frame):
    array = np.ones(shape=(1, len(frame) * len(frame[0])))
    frame = frame // 255
    count = 0
    for row in range(len(frame)):
        for col in range(len(frame[row])):
            data = frame[row][col]
            value = (data * 2) - 1
            array[0][count] = value
            count += 1
    return array

def predict(frame,coordinates,model,filter):
    new_frame = filter_frame(frame,coordinates,filter)
    binary_array = single_conversion(new_frame)
    prediction = model.predict(binary_array,verbose=False)
    index = np.argmax(prediction[0])
    confidence = prediction[0][index]
    return index,confidence