#coding:utf-8
import os
import cv2
import sys
import natsort
import shutil
from PIL import Image
import numpy as np
import pandas as pd

origin_file_path = './data/acacia-train_months/'
new_file_path = './data/acacia-train/'


###################------------------------step1 get new IMG_Palm_12 dir------------------------
new_12_months_path = os.path.join(origin_file_path + 'new_IMG_Palm_12/')
if os.path.exists(new_12_months_path):
    shutil.rmtree(new_12_months_path)
os.mkdir(new_12_months_path)

imfiles = os.listdir(os.path.join(origin_file_path + 'IMG_Palm_12'))
imfiles = natsort.natsorted(imfiles)
print('imfiles: ',imfiles)
for i in imfiles:
    print('i: ',i)
    img_name = int(os.path.basename(i)[4:-4])
    img = cv2.imread(os.path.join(origin_file_path + 'IMG_Palm_12/'+i))
    # cv2.imshow('test_img',img)
    # cv2.waitKey(1)
    print('img_name: ',img_name)
    img_name = img_name + 1000
    print('new_img_number: ',img_name)
    new_img_name = os.path.join(i[0:4:]+str(img_name) + '.jpg')
    print('new_img_name: ',new_img_name)
    cv2.imwrite(os.path.join(new_12_months_path + new_img_name),img)

###################-------------------------step2--combine IMG_Palm_06 + new_IMG_Palm_12  -------
IMG_acacia_path = os.path.join(new_file_path + 'IMG_Palm/')
if os.path.exists(IMG_acacia_path):
    shutil.rmtree(IMG_acacia_path)
os.mkdir(IMG_acacia_path)

#write 06 month
IMG_acacia_06_month = os.listdir(os.path.join(origin_file_path + 'IMG_Palm_06'))
IMG_acacia_06_month = natsort.natsorted(IMG_acacia_06_month)
for i in IMG_acacia_06_month:
    print('i: ',i)
    img_06 = cv2.imread(os.path.join(origin_file_path + 'IMG_Palm_06/' + i))
    new_06_name = os.path.join(i[0:-4:] + '.jpg')

    cv2.imwrite(os.path.join(IMG_acacia_path + new_06_name),img_06)

#write 12 month
IMG_acacia_12_month = os.listdir(new_12_months_path)
IMG_acacia_12_month = natsort.natsorted(IMG_acacia_12_month)
for i in IMG_acacia_12_month:
    print('i: ',i)
    img_12 = cv2.imread(os.path.join(new_12_months_path + i))
    new_12_name = os.path.join(i[0:-4:] + '.jpg')
    cv2.imwrite(os.path.join(IMG_acacia_path + new_12_name),img_12)


###################-------------------------step3--get new_gt_palm_06.txt & new_gt_palm_12.txt-------
####------------------------------------------06months----------------------------------------------------------------------------
if os.path.exists(origin_file_path + 'new_gt_palm_06.txt'):
    os.remove(origin_file_path + 'new_gt_palm_06.txt')
with open(origin_file_path + 'gt_palm_06.txt','r') as f5:
    f5_lines = f5.readlines()
    print('lines:',f5_lines)
    for i in f5_lines:
        img_name = i.strip().split(' ',1)[0]
        img_bb = i.strip().split(' ',1)[1]
        print('img_name: ',img_name)
        print('img_bb: ',img_bb)
        img_name = img_name.split('/')
        new_img_name = os.path.join('./data/acacia-train/IMG_Palm/'+img_name[4])
        print('new_img_name: ',new_img_name)

        new_line = os.path.join(new_img_name + ' '+img_bb)
        print('new_line: ',new_line)

        with open(origin_file_path + 'new_gt_palm_06.txt','a+') as f6:
            f6.write('%s\n'% (new_line))

####-----------------------------------------12months-------------------------------------------------
if os.path.exists(origin_file_path + 'new_gt_palm_12.txt'):
    os.remove(origin_file_path + 'new_gt_palm_12.txt')
with open(origin_file_path + 'gt_palm_12.txt','r') as f7:
    f7_lines = f7.readlines()
    print('lines:',f7_lines)
    for i in f7_lines:
        img_name = i.strip().split(' ',1)[0]
        img_bb = i.strip().split(' ',1)[1]
        print('img_name: ',img_name)
        print('img_bb: ',img_bb)
        img_index = os.path.basename(img_name)[4:-4]
        print('img_index: ',img_index)
        img_index = int(img_index) + 1000
        new_img_name = os.path.join('./data/acacia-train/IMG_Palm/'+'IMG_'+str(img_index)+'.jpg')
        print('new_img_name: ',new_img_name)

        new_line = os.path.join(new_img_name + ' ' + img_bb)
        print('new_line: ',new_line)

        with open(origin_file_path + 'new_gt_palm_12.txt','a+') as f8:
            f8.write('%s\n'% (new_line))

# ###################----------------------------step4 get gt_palm.txt for acacia-train---------
with open(origin_file_path + 'new_gt_palm_06.txt') as f9:
    f9_lines = f9.readlines()
    print('f9_lines: ',f9_lines)
    with open(origin_file_path + 'new_gt_palm_12.txt') as f10:
        f10_lines = f10.readlines()
        print('f10_lines: ',f10_lines)
        new_lines = f9_lines + f10_lines
        # print('new_lines: ',new_lines)
        print('len(new_lines): ',len(new_lines))
        with open(new_file_path + 'gt_palm.txt','w') as f12:
            for i in new_lines:
                f12.write('%s \n'% (i.strip()))


###########----------------------------------------step5 get train.txt for acacia_train---------
#MAKE SURE THAT THE IMG_Palm is not empty
IMG_acacia = new_file_path
imfiles = os.listdir(IMG_acacia + 'IMG_Palm')
imfiles = natsort.natsorted(imfiles)
print('imfiles: ',imfiles)
with open(IMG_acacia+'train.txt','w') as f14:
    for i in imfiles:
        f14.write('%s\n'% (i))

########-----------------------------------------step6 get IMG_point
if os.path.exists(new_file_path + 'IMG_point/'):
    shutil.rmtree(new_file_path + 'IMG_point/')
os.mkdir(new_file_path + 'IMG_point/')

with open(new_file_path + 'gt_palm.txt','r') as f15:
    f15_lines = f15.readlines()
    for line in f15_lines:
        print('line: ',line)
        line = line.strip().split(' ')
        point_name = os.path.basename(line[0])[0:-4]
        print('point_name: ',point_name)
        point_number = int(line[1])
        with open(new_file_path + 'IMG_point/' + point_name + '.txt', 'w') as f16:
            for i in range(point_number):
                x = list(map(int, line[2::2]))
                y = list(map(int, line[3::2]))

                f16.writelines('%s %s\n'%(x[i],y[i]))


#



            



        


        
        



    

    


























