# import matplotlib.pyplot as plt
import numpy as np
import natsort
import shutil
from PIL import Image
import os
import cv2

filepath = 'acacia-train/gt_palm.txt'
imgpath = 'acacia-train/IMG_Palm/IMG_'


if os.path.exists('cv2_center/'):
    shutil.rmtree('cv2_center/')

os.mkdir('cv2_center/')

with open(filepath,'r') as f:
    f = f.readlines()
    for line in f:
        line = line.strip().split(' ')
        img_name = os.path.basename(line[0])[4:-4]
        print("img name: ", img_name)

        number = int(line[1])

#------------------------------------cv2-center images-------------------
        radius = 1
        thickness = 8
        point_color = (0,0,255)
        img = cv2.imread(os.path.join(imgpath+img_name+'.jpg'))
        for i in range(number):
            point = (x[i],y[i])
            print('point:',point)
            cv2.circle(img,point,radius,point_color,thickness)

            cv2.imwrite(os.path.join('cv2_center/'+img_name+'.jpg'),img)

