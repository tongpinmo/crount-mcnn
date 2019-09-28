import numpy as np
import scipy.io as scio
import os

# dataFile = '/home/ubuntu/users/tongpinmo/projects/crowdcount-mcnn/data/original/shanghaitech/part_A_final/train_data/ground_truth/GT_IMG_2.mat'
#
# data = scio.loadmat(dataFile)
#
# print('type: ',type(data))
# print('keys: ',data.keys())
# print('image_info: ',data['image_info'][0][0][0][0][0])
# print('shape of image_info: ',data['image_info'][0][0][0][0][0].shape)                  #(707,2)
#
#
# scio.savemat('./save.mat',{'image_info':data['image_info'][0][0][0][0][0]})
#


####  test .mat file

dataFile = '/home/ubuntu/users/tongpinmo/projects/crowdcount-mcnn/data/acacia-train/ground_truth/GT_IMG_0000.mat'

data = scio.loadmat(dataFile)


print('data: ',data)
print('type: ',type(data))
print('keys: ',data.keys())
print('image_info: ',data['image_info'])
print('shape of image_info: ',data['image_info'].shape)                  #(707,2)
