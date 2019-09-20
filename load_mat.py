import numpy as np
import scipy.io as scio
import os

dataFile = '/home/ubuntu/users/tongpinmo/projects/crowdcount-mcnn/data/original/shanghaitech/part_A_final/train_data/ground_truth/GT_IMG_20.mat'

data = scio.loadmat(dataFile)

print('type: ',type(data))
print('keys: ',data.keys())
print('image_info: ',data['image_info'])
# print('version: ',data['__version__'])
# print('header: ',data['__header__'])
# print('globals: ',data['__globals__'])

data_numpy = data['image_info']
print('type(data_numpy): ',type(data_numpy))
print('data_numpy.shape: ',data_numpy.shape)        #(1,1)
data_numpy_x = data_numpy[0]
print('data_numpy_x: ',data_numpy_x.shape)
data_numpy_x0 = data_numpy_x[0]
print('data_numpy_x0.shape: ',data_numpy_x0.shape)
print('data_numpy_x0: ',data_numpy_x0)

data_numpy_x1 = data_numpy_x0[0]
print('data_numpy_x1: ',data_numpy_x1)


