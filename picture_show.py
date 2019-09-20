# import matplotlib.pyplot as plt
import numpy as np
import natsort
import shutil
from PIL import Image
import os
import cv2

filepath = './point_gt.txt'
imgpath = './IMG_20.jpg'


if os.path.exists('cv2_center/'):
    shutil.rmtree('cv2_center/')

os.mkdir('cv2_center/')

with open(filepath,'r') as f:
    f = f.readlines()
    for line in f:
        line = line.strip().split(',')
        print('line: ',line)
        img_name = os.path.basename(imgpath)[:-4]

#------------------------------------cv2-center images-------------------
        radius = 6
        thickness = 10
        point_color = (0,0,255)
        img = cv2.imread(imgpath)

        point = (int(float(line[0])),int(float(line[1])))
        print('point:',point)
        cv2.circle(img,point,radius,point_color,thickness)
    cv2.imwrite(os.path.join('cv2_center/'+img_name+'.jpg'),img)

