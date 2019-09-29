#-------------------------------------------for different data_preparing months----------------------------
import ctypes
import natsort
import shutil
import os 
import sys

# os.environ["CUDA_VISIBLE_DEVICES"] = "1,2"

#create library files 
lib = ctypes.cdll.LoadLibrary
lib_so = lib("./data_preparation/get_cut_center.so")

#------------------------------------------------get image from the origin each month image--------------------------------
#acacia-06-month
ImgPath = "./data/raw_data/Image_06months.jpg"
ImgBeginX = 9500
ImgBeginY = 6500
Dst_img_width  = 10000
Dst_img_height = 8000

#acacia-12-month
# ImgPath = "./data/raw_data/Image_12months.jpg"
# ImgBeginX = 17000
# ImgBeginY = 10000
# Dst_img_width  = 10000
# Dst_img_height = 9000


ImgPath_split = ImgPath.split('/')
ResultName_ = os.path.join(ImgPath_split[2][:-4]+'-x'+str(ImgBeginX)+'-y'+str(ImgBeginY)+'-'+
                           str(Dst_img_width)+'-'+str(Dst_img_height)+'.jpg')


get = lib_so.get_img(ImgPath,ResultName_,Dst_img_width,Dst_img_height,ImgBeginX,ImgBeginY)

print('ok,get finished')
#---------------------------------------------cut image after the getted each month image----------------------------

palm_file = ResultName_
palmxyfile = "./data/raw_data/06Months.txt"
N_small_img = 1000
Size_small_img = 1024
palm_box = "./data/acacia-train_months/gt_palm_06.txt"
img_dir = "./data/acacia-train_months/IMG_Palm_06"
img_name_ = "./data/acacia-train_months/IMG_Palm_06/IMG_"
#---------------remove the exist gt_palm.txt & train.txt & IMG_Palm file
if os.path.exists(palm_box):
    os.remove(palm_box)
if os.path.exists(img_dir):
    shutil.rmtree(img_dir)
os.mkdir(img_dir)

cut = lib_so.cut_img(palm_file, palmxyfile, N_small_img, Size_small_img, palm_box, img_name_, ImgBeginX, ImgBeginY)

print('ok,cut finished')
#-----------------------------------------get train.txt correspond to the cut images------------------------
############-------------can produce it at last for multiple months
# path = './acacia-train_months/'
# with open(path+'train.txt','w') as tf:
#     imfiles = os.listdir(os.path.join(path+'IMG_Palm'))
#     imfiles = natsort.natsorted(imfiles)
#     frame_id = [os.path.basename(fi)[:-4] for fi in imfiles]
#     for frame in frame_id:
#         print('frame:',frame)
#         tf.write('%s \n'% (frame))
#
# print('ok,get train.txt finished')



