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
    coordinates = [[135,490,80,180]]
    training_folder = 'train_models/training_images/home_trainingimages/'
    label_key = {'None':'0','Home':'1'}
    binarydata_file = 'train_models/binary_imagedata/homeimages.csv'
    model_path = 'models/homedetectionmodel'
    p = Parameters(layers=[14,8],activations=['relu','sigmoid','softmax'],num_outnodes=len(label_key),
                   loss_function='sparse_categorical_crossentropy',
                 opt_function='adam',measure=['accuracy'],batch_size=12,num_epochs=110)
    return model_path,coordinates,training_folder,label_key,binarydata_file,p

def make_characterlabeldict(file):
    f = open(file,'r')
    label_dict = {'None':'0'}
    lines = f.readlines()
    for i in range(1,len(lines)):
        character_name = lines[i].split(',')[0]
        label_dict[character_name] = i
    return label_dict

def set_4charactermodelparameters():
    coordinates = [[155,445,452,480],[1455,1745,452,480],[155,445,834,862],[1455,1745,834,862]]
    training_folder = 'train_models/training_images/char_trainingimages4/'
    label_key = make_characterlabeldict(file='nextgenstats/information/characterstats.csv')
    binarydata_file = 'train_models/binary_imagedata/char4images.csv'
    model_path = 'models/chardetectionmodel4'
    p = Parameters(layers=[36, 18], activations=['relu', 'relu', 'softmax'], num_outnodes=len(label_key),
                   loss_function='sparse_categorical_crossentropy',
                   opt_function='adam', measure=['accuracy'], batch_size=12, num_epochs=150)
    return model_path, coordinates, training_folder, label_key, binarydata_file, p

def set_menumodelparameters():
    coordinates = [[120,675,80,140]]
    training_folder = 'train_models/training_images/menu_trainingimages/'
    label_key = {'None':0,'Singleplayer':1,'Multiplayer':2,'Character':3,'Vehicle':4,'Drift':5,'Start':6}
    binarydata_file = 'train_models/binary_imagedata/menuimages.csv'
    model_path = 'models/menudetectionmodel'
    p = Parameters(layers=[30,18], activations=['relu', 'relu', 'softmax'], num_outnodes=len(label_key),
                   loss_function='sparse_categorical_crossentropy',
                   opt_function='adam', measure=['accuracy'], batch_size=8, num_epochs=150)
    return model_path, coordinates, training_folder, label_key, binarydata_file, p

def set_playercountmodelparameters():
    coordinates = [[555,640,80,140]]
    training_folder = 'train_models/training_images/playercount_trainingimages/'
    label_key = {'None':0,'players2':1,'players3':2,'players4':3}
    binarydata_file = 'train_models/binary_imagedata/playercountimages.csv'
    model_path = 'models/playercountdetectionmodel'
    p = Parameters(layers=[18,8], activations=['relu', 'relu', 'softmax'], num_outnodes=len(label_key),
                   loss_function='sparse_categorical_crossentropy',
                   opt_function='adam', measure=['accuracy'], batch_size=4, num_epochs=150)
    return model_path, coordinates, training_folder, label_key, binarydata_file, p

def set_gomodel2parameters():
    coordinates = [[740,1140,200,360]]
    training_folder = 'train_models/training_images/go_trainingimages2/'
    label_key = {'GO':0,'1':1,'2':2,'3':3,'ANone':4}
    binarydata_file = 'train_models/binary_imagedata/go2images.csv'
    model_path = 'models/go2detectionmodel'
    p = Parameters(layers=[22,14], activations=['relu', 'relu', 'softmax'], num_outnodes=len(label_key),
                   loss_function='sparse_categorical_crossentropy',
                   opt_function='adam', measure=['accuracy'], batch_size=16, num_epochs=80)
    return model_path, coordinates, training_folder, label_key, binarydata_file, p

def get_playerdict(file):
    f = open(file, 'r')
    character_dict = dict()
    datalines = f.readlines()
    for i in range(1, len(datalines)):
        data = datalines[i].split(',')
        character_name = data[0]
        character_dict[character_name] = i-1
    character_dict["None"] = 0
    return character_dict

def get_coordinates():
    coordinates = []
    [x0, x1, y0, y1] = [600, 1100, 73, 149]
    boxheight = y1 - y0
    for i in range(12):
        y2 = y0 + (boxheight * i)
        y3 = y2 + boxheight
        coordinates.append([x0,x1,y2,y3])
    return coordinates

def set_scoringmodelparameters():
    coordinates = get_coordinates()
    training_folder = 'train_models/training_images/scoring_trainingimages/'
    label_key = get_playerdict(file='nextgenstats/information/characterstats.csv')
    binarydata_file = 'train_models/binary_imagedata/scoringimages.csv'
    model_path = 'models/scoringdetectionmodel'
    p = Parameters(layers=[42,28], activations=['relu','relu','softmax'], num_outnodes=len(label_key),
                   loss_function='sparse_categorical_crossentropy',
                   opt_function='adam', measure=['accuracy'], batch_size=32, num_epochs=100)
    return model_path, coordinates, training_folder, label_key, binarydata_file, p
def write_imgtobinary(f,label,image):
    f.write(str(label))
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
    for image_name in images:
        image_path = training_folder + image_name
        image = cv.imread(image_path)
        for i in range(len(coordinates)):
            [x0,x1,y0,y1] = coordinates[i]
            new_image = image[y0:y1,x0:x1]//255
            label = label_key[image_name.split('#')[i]]
            write_imgtobinary(f, label, new_image)
    f.close()

def build_neuralnetwork(model_path,coordinates, training_folder, label_key, binarydata_file,p):
    prepare_data(coordinates, training_folder, label_key, binarydata_file)
    network = Neural_Network(model_path=model_path,trainingdata_file=binarydata_file,layers=p.layers,
                             activations=p.activations,num_outnodes=p.num_outnodes,loss_function=p.loss_function,
                             opt_function=p.opt_function,measure=p.measure,batch_size=p.batch_size,
                             num_epochs=p.num_epochs)
    network.construct_model()

def main():
    command = sys.argv
    if "home" in command:
        model_path, coordinates, training_folder, label_key, binarydata_file, p = set_homemodelparameters()
        if "prepare" in command:
            prepare_data(coordinates, training_folder, label_key, binarydata_file)
        build_neuralnetwork(model_path, coordinates, training_folder, label_key, binarydata_file, p)
    if "4p" in command:
        model_path, coordinates, training_folder, label_key, binarydata_file, p = set_4charactermodelparameters()
        if "prepare" in command:
            prepare_data(coordinates, training_folder, label_key, binarydata_file)
        build_neuralnetwork(model_path, coordinates, training_folder, label_key, binarydata_file, p)
    if 'menu' in command:
        model_path, coordinates, training_folder, label_key, binarydata_file, p = set_menumodelparameters()
        if "prepare" in command:
            prepare_data(coordinates, training_folder, label_key, binarydata_file)
        build_neuralnetwork(model_path, coordinates, training_folder, label_key, binarydata_file, p)
    if 'playercount' in command:
        model_path, coordinates, training_folder, label_key, binarydata_file, p = set_playercountmodelparameters()
        if "prepare" in command:
            prepare_data(coordinates, training_folder, label_key, binarydata_file)
        build_neuralnetwork(model_path, coordinates, training_folder, label_key, binarydata_file, p)
    if 'go' in command:
        model_path, coordinates, training_folder, label_key, binarydata_file, p = set_gomodel2parameters()
        if "prepare" in command:
            prepare_data(coordinates, training_folder, label_key, binarydata_file)
        build_neuralnetwork(model_path, coordinates, training_folder, label_key, binarydata_file, p)
    if 'scoring' in command:
        model_path, coordinates, training_folder, label_key, binarydata_file, p = set_scoringmodelparameters()
        if "prepare" in command:
            prepare_data(coordinates, training_folder, label_key, binarydata_file)
        build_neuralnetwork(model_path, coordinates, training_folder, label_key, binarydata_file, p)



main()