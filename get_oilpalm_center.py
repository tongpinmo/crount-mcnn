import numpy as np
import natsort
import shutil
import os 
#
# origin_gt_file = './raw_data/BIA2_v1.txt'
# oilpalm_center_file = './raw_data/oilpalm_center.txt'
#
#
# with open(origin_gt_file,'r') as tf:
#     flines = tf.readlines()
#     print('flines: ',flines)
#     for line in flines:
#         line = line.strip().split(' ')
#         print('line: ',line)
#         x_0 = line[1]
#         y_0 = line[2]
#         x_1 = line[3]
#         y_1 = line[4]
#         print('x0:',x_0)
#         print('y_1:',y_1)
#         x_center = int((int(x_0) + int(x_1)) / 2)
#         y_center = int((int(y_0) + int(y_1)) / 2)
#
#         with open(oilpalm_center_file,'a+') as wf:
#             wf.writelines('%s %s\n'%(x_center,y_center))


########-----------------------------------------step6 get IMG_point
new_file_path = './oilpalm-train/'
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
















