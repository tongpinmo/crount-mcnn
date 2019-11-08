import os
import numpy as np
import scipy.io as scio
import shutil

##### convert all IMG_point file to .mat gt file

origin_point_file = './data/acacia-test/12months/IMG_point'
ground_mat_file = './data/acacia-test/12months/ground_truth'

filenames = os.listdir(origin_point_file)

if os.path.exists(ground_mat_file):
    shutil.rmtree(ground_mat_file)
os.mkdir(ground_mat_file)


for file in filenames:
    print(file)
    np_file = np.loadtxt(os.path.join(origin_point_file + '/' + file))
    print('np_file: ',np_file)
    print('type of np_file: ',type(np_file))
    img_number = file.split('.')[0]
    print('img_number: ',img_number)
    img_mat_file = os.path.join(ground_mat_file + '/' + img_number + '.mat')
    print('img_mat_file: ',img_mat_file)

    scio.savemat(img_mat_file,{'image_info':np_file})

