import cv2 as cv
import sys
import os
from tools.deep_learning import Neural_Network

class Parameters():
    def __init__(self,layers=None,activations=None,num_outnodes=None,loss_function=None,
                 opt_function=None,measure=None,batch_size=None,num_epochs=None):
        self.layers = layers
        self.activations = activations
        self.num_outnodes = num_outnodes
        self.loss_function = loss_function
        self.opt_function = opt_function
        self.measure = measure
        self.batch_size = batch_size
        self.num_epochs = num_epochs
def set_homemodelparameters():
    coordinates = [135,490,80,180]
    training_folder = 'train_models/training_images/home_trainingimages/'
    label_key = {'None':'0','Home':'1'}
    binarydata_file = 'train_models/binary_imagedata/homeimages.csv'
    model_path = 'models/homedetectionmodel'
    p = Parameters(layers=[14,8],activations=['relu','sigmoid','softmax'],num_outnodes=len(label_key),
                   loss_function='sparse_categorical_crossentropy',
                 opt_function='adam',measure=['accuracy'],batch_size=12,num_epochs=110)
    return model_path,coordinates,training_folder,label_key,binarydata_file,p

def write_imgtobinary(f,label,image):
    f.write(label)
    f.write(',')
    for row in range(len(image)):
        for col in range(len(image[row])):
            data = image[row][col]
            value = (max(data)*2)-1
            f.write(str(value))
            if row != len(image) - 1 or col != len(image[row]) - 1:
                f.write(',')
            else:
                f.write('\n')

def prepare_data(coordinates,training_folder,label_key,binarydata_file):
    f = open(binarydata_file,'w')
    images = os.listdir(training_folder)
    [x0,x1,y0,y1] = coordinates
    for image_name in images:
        image_path = training_folder + image_name
        image = cv.imread(image_path)
        image = image[y0:y1,x0:x1]//255
        label = label_key[image_name.split('#')[0]]
        write_imgtobinary(f, label, image)
    f.close()

def build_neuralnetwork(model_path,coordinates, training_folder, label_key, binarydata_file,p):
    prepare_data(coordinates, training_folder, label_key, binarydata_file)
    network = Neural_Network(model_path=model_path,trainingdata_file=binarydata_file,layers=p.layers,
                             activations=p.activations,num_outnodes=p.num_outnodes,loss_function=p.loss_function,
                             opt_function=p.opt_function,measure=p.measure,batch_size=p.batch_size,
                             num_epochs=p.num_epochs)
    network.construct_model()


def main():
    model_path,coordinates,training_folder,label_key,binarydata_file,p = set_homemodelparameters()
    build_neuralnetwork(model_path,coordinates, training_folder, label_key, binarydata_file,p)


main()