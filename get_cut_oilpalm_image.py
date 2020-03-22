import ctypes
import natsort
import os 
import sys
import shutil
import numpy as np
import scipy.io as scio

#create library files 
lib = ctypes.cdll.LoadLibrary
lib_so = lib("./get_cut_palm_center.so")

#------------------------------------------------get image from the origin--------------------------------
ImgPath = "./data/raw_data/oilpalm-insight-2.jpg"
Dst_img_width  = 9000
Dst_img_height = 9000
ImgBeginX = 5000
ImgBeginY = 5000

ImgPath_split = ImgPath.split('/')
ResultName_ = os.path.join(ImgPath_split[2][:-4]+'-x'+str(ImgBeginX)+'-y'+str(ImgBeginY)+'-'+
                           str(Dst_img_width)+'-'+str(Dst_img_height)+'.jpg')

get = lib_so.get_img(ImgPath,ResultName_,Dst_img_width,Dst_img_height,ImgBeginX,ImgBeginY)

print('ok,get finished')
#---------------------------------------------cut image after the getted image----------------------------
palm_file = ResultName_
palmxyfile = "./data/raw_data/oilpalm_center.txt"
N_small_img = 100
Size_small_img = 1024
palm_box = "./data-oilpalm/oilpalm-test/gt_palm.txt"
img_dir = "./data-oilpalm/oilpalm-test/IMG_Palm"
img_name_ = "./data-oilpalm/oilpalm-test/IMG_Palm/IMG_"

#---------------remove the exist gt_palm.txt & train.txt & IMG_Palm file
if os.path.exists(palm_box):
    os.remove(palm_box)
if os.path.exists(img_dir):
    shutil.rmtree(img_dir)
os.mkdir(img_dir)

cut = lib_so.cut_img(palm_file,palmxyfile,N_small_img,Size_small_img,palm_box,img_name_,ImgBeginX,ImgBeginY)

print('ok,cut finished')
# #-----------------------------------------get train.txt correspond to the cut images------------------------
path = './data-oilpalm/oilpalm-test/'
with open(path+'train.txt','w') as tf:
    imfiles = os.listdir(os.path.join(path+'IMG_Palm'))
    imfiles = natsort.natsorted(imfiles)
    frame_id = [os.path.basename(fi)[:-4] for fi in imfiles]
    for frame in frame_id:
        print('frame:',frame)
        tf.write('%s \n'% (frame))

print('ok,get train.txt finished')


#------------------------------------get IMG_point file
IMG_point_path = path

if os.path.exists(IMG_point_path + 'IMG_point/'):
    shutil.rmtree(IMG_point_path + 'IMG_point/')
os.mkdir(IMG_point_path + 'IMG_point/')

with open(IMG_point_path + 'gt_palm.txt','r') as f15:
    f15_lines = f15.readlines()
    for line in f15_lines:
        print('line: ',line)
        line = line.strip().split(' ')
        point_name = os.path.basename(line[0])[0:-4]
        print('point_name: ',point_name)
        point_number = int(line[1])
        with open(IMG_point_path + 'IMG_point/' + point_name + '.txt', 'w') as f16:
            for i in range(point_number):
                x = list(map(int, line[2::2]))
                y = list(map(int, line[3::2]))

                f16.writelines('%s %s\n'%(x[i],y[i]))



#####----------------- convert all IMG_point file to .mat gt file

origin_point_file = './data-oilpalm/oilpalm-test/IMG_point'
ground_mat_file = './data-oilpalm/oilpalm-test/ground_truth'

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

