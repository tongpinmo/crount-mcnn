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
# ImgPath = "./data/raw_data/6Months_Crop.jpg"
# ImgBeginX = 6500
# ImgBeginY = 8500
# Dst_img_width  = 10000
# Dst_img_height = 10000

# acacia-12-month
ImgPath = "./data/raw_data/12Months_Crop.jpg"
ImgBeginX = 8000
ImgBeginY = 9000
Dst_img_width  = 9000
Dst_img_height = 9000


ImgPath_split = ImgPath.split('/')
ResultName_ = os.path.join(ImgPath_split[3][:-4]+'-x'+str(ImgBeginX)+'-y'+str(ImgBeginY)+'-'+
                           str(Dst_img_width)+'-'+str(Dst_img_height)+'.jpg')


get = lib_so.get_img(ImgPath,ResultName_,Dst_img_width,Dst_img_height,ImgBeginX,ImgBeginY)

print('ok,get finished')
#---------------------------------------------cut image after the getted each month image----------------------------

palm_file = ResultName_
palmxyfile = "./data/raw_data/12Months.txt"
N_small_img = 500
Size_small_img = 1024
palm_box = "./data/acacia-test/12months/gt_test_12.txt"
img_dir = "./data/acacia-test/12months/Palm_test_12"
img_name_ = "./data/acacia-test/12months/Palm_test_12/IMG_"
#---------------remove the exist gt_palm.txt & train.txt & IMG_Palm file
if os.path.exists(palm_box):
    os.remove(palm_box)
if os.path.exists(img_dir):
    shutil.rmtree(img_dir)
os.mkdir(img_dir)

cut = lib_so.cut_img(palm_file, palmxyfile, N_small_img, Size_small_img, palm_box, img_name_, ImgBeginX, ImgBeginY)

print('ok,cut finished')
#-----------------------------------------get train.txt for each month correspond to the cut images------------------------
############-------------can produce it at last for multiple months
path = './data/acacia-test/12months/'
with open(path+'test_12.txt','w') as tf:
    imfiles = os.listdir(os.path.join(path+'Palm_test_12'))
    imfiles = natsort.natsorted(imfiles)
    frame_id = [os.path.basename(fi)[:-4] for fi in imfiles]
    for frame in frame_id:
        print('frame:',frame)
        tf.write('%s \n'% (frame))

print('ok,get test.txt finished')


#------------------------------------get IMG_point file
IMG_point_path = './data/acacia-test/12months/'

if os.path.exists(IMG_point_path + 'IMG_point/'):
    shutil.rmtree(IMG_point_path + 'IMG_point/')
os.mkdir(IMG_point_path + 'IMG_point/')

with open(IMG_point_path + 'gt_test_12.txt','r') as f15:
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

