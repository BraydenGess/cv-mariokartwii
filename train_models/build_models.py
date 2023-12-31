import cv2 as cv
import sys
import os

def set_homemodelparameters():
    coordinates = [135,490,80,180]
    training_folder = 'training_images/home_trainingimages/'
    label_key = {'None':'0','Home':'1'}
    binarydata_file = 'train_models/binary_imagedata/homeimages.csv'
    return coordinates,training_folder,label_key,binarydata_file

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

def build_neuralnetwork(coordinates, training_folder, label_key, binarydata_file):
    prepare_data(coordinates, training_folder, label_key, binarydata_file)

def main():
    coordinates,training_folder,label_key,binarydata_file = set_homemodelparameters()
    build_neuralnetwork(coordinates, training_folder, label_key, binarydata_file)


main()