import numpy as np
import natsort
import shutil
from PIL import Image
import os
import cv2
##################################################plot the whole IMG_palm corresponding to gt_palm.txt ****

filepath = './data/acacia-train/gt_palm.txt'
imgpath = './data/acacia-train/IMG_Palm/IMG_'


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
#-----------------------------------plt-center images----------------
        x = list(map(int,line[2::2]))
        y = list(map(int,line[3::2]))
        # print("x: ", x)
        # print("y: ", y)
        #read each image
        # im = np.array(Image.open(os.path.join(imgpath+img_name+'.jpg')))
        # #plot
        # plt.imshow(im)
        # plt.plot(x, y,'ro')
        # plt.title('figure')
        # plt.show()


#------------------------------------cv2-center images-------------------
        radius = 2
        thickness = 8
        point_color = (0,0,255)
        img = cv2.imread(os.path.join(imgpath+img_name+'.jpg'))
        for i in range(number):
            point = (x[i],y[i])
            print('point:',point)
            cv2.circle(img,point,radius,point_color,thickness)

            cv2.imwrite(os.path.join('cv2_center/'+img_name+'.jpg'),img)

#------------------------------------cv2-Rectangle images-------------------

	#point_color = (0,0,255)
	#img = np.array(Image.open(os.path.join(imgpath+img_name+'.jpg')))
	#x_left = map(int,line[2::4])
	#y_left = map(int,line[3::4])
	#x_right = map(int,line[4::4])
        #y_right = map(int,line[5::4])
        #print('x_left:',x_left)
        #print('y_left:',y_left)
        #print('x_right:',x_right)
        #print('y_right:',y_right)
        #for i in range(number):
        #    cv2.rectangle(img,(x_left[i],y_left[i]),(x_right[i],y_right[i]),point_color,2)
        #cv2.imwrite(os.path.join('cv2_box/'+img_name+'.jpg'),img)
        
