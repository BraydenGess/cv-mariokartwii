import cv2 as cv
import sys

def set_homemodelparameters():
    coordinates = [135,490,80,180]
    training_folder = 'training_images/home_trainingimages/'
    label_key = {'None':'0','Home':'1'}
    img = cv.imread('training_images/home_trainingimages/Home#0.png')
    newframe = img[80:180,135:490]
    cv.imwrite('cack.png',newframe)

def main():
    set_homemodelparameters()
    print(sys.argv)


main()