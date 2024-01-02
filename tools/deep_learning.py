from tools.imagemanipulation import *
from sklearn.model_selection import train_test_split
from keras.layers import Dense
from keras.models import Sequential
import numpy as np

class Neural_Network():
    def __init__(self,trainingdata_file=None,layers=None,activations=None,num_outnodes=None,loss_function=None,
                 opt_function=None,measure=None,batch_size=None,num_epochs=None):
        self.trainingdata_file = trainingdata_file
        self.layers = layers
        self.activations = activations
        self.num_outnodes = num_outnodes
        self.loss_function = loss_function
        self.opt_function = opt_function
        self.measure = measure
        self.batch_size = batch_size
        self.num_epochs = num_epochs
    def load_data(self):
        array = np.loadtxt(self.trainingdata_file,delimiter=',',dtype=int)
        Y = np.array(array[:,0])
        X = np.array(array[:,1:])
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2)
        return X_train,X_test,Y_train,Y_test
    def train_model(self,X_train,Y_train):
        self.layers = [X_train.shape[1]]+self.layers
        model = Sequential()
        for i in range(1,len(self.layers)):
            model.add(Dense(self.layers[i],activation=self.activations[i-1],input_shape=(self.layers[i-1],)))
        model.add(Dense(self.num_outnodes,activation=self.activations[-1]))
        model.compile(loss=self.loss_function,optimizer=self.opt_function,metrics=self.measure)
        model.summary()
        model.fit(X_train,Y_train,batch_size=self.batch_size,epochs=self.num_epochs,
                  verbose=1,validation_data=(X_train,Y_train))
        return model
    def evaluate_model(self,model,X_test,Y_test):
        score = model.evaluate(X_test,Y_test,verbose=0)
        print('Test loss:',score[0])
        print('Test accuracy',score[1])
    def construct_model(self):
        X_train, X_test, Y_train, Y_test = self.load_data()
        model = self.train_model(X_train,Y_train)
        self.evaluate_model(model,X_test,Y_test)




def filter_frame(frame,coordinates,filter):
    [x0,x1,y0,y1] = coordinates
    new_frame = frame[y0:y1,x0:x1].copy()
    if filter == 'imgtobinary':
        new_frame = imgtobinary(new_frame)
    return new_frame

def single_conversion(frame):
    array = np.ones(shape=(1, len(frame) * len(frame[0])))
    frame = frame//255
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