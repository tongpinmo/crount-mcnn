import os
import torch
import numpy as np
from skimage import io, color
import cv2
from torchvision import transforms
from get_density_map_gaussian import *

#SET SEED
np.random.seed(1)
torch.manual_seed(1)
torch.cuda.manual_seed_all(1)

N = 9?
dataset = 'Acacia'
dataset_name = ['shanghaitech_part_' + dataset + '_patches_' + str(N)]
path = ['../data/original/shanghaitech/part_' + dataset +'_final/train_data/images/']
output_path = '../data/formatted_trainval/'
train_path_img = os.path.join(output_path, dataset_name, '/train/')
train_path_den = os.path.join(output_path, dataset_name, '/train_den/')
val_path_img = os.path.join(output_path, dataset_name, '/val/')
val_path_den = os.path.join(output_path, dataset_name, '/val_den/')
gt_path = ['../data/original/shanghaitech/part_'+ dataset +'_final/train_data/ground_truth/']

os.mkdir(output_path)
os.mkdir(train_path_img)
os.mkdir(train_path_den)
os.mkdir(val_path_img)
os.mkdir(val_path_den)

if (dataset == 'Acacia'):
    num_images = 4869


num_val = np.ceil(num_images * 0.1)                             #10% as val
indices = np.random.permutation(np.arange(num_images))          #array list

for idx in range(num_images):
    i = indices(idx)
    if (idx % 10) == 0:
        print(1, 'Processing %3d/%d files\n', idx, num_images)

GT_img_mat_path = (os.path.join(gt_path, 'GT_IMG_', str(i), '.mat'))
input_img_name = os.path.join(path, 'IMG_', str(i), '.jpg')
im = io.imread(input_img_name)
[h, w, c] = im.size()
if (c == 3):
    im = color.rgb2gray(im)


wn2 = w / 8
hn2 = h / 8
wn2 = 8 * np.floor(wn2 / 8)
hn2 = 8 * np.floor(hn2 / 8)

annPoints = image_info{1}.location
if (w <= 2 * wn2):
    im = im.resize(im, [h, 2 * wn2 + 1])
    annPoints(:, 1) = annPoints(:, 1)*2 * wn2 / w

if (h <= 2 * hn2):
    im = im.resize(im, [2 * hn2 + 1, w])
    annPoints(:, 2) = annPoints(:, 2)*2 * hn2 / h

[h, w, c] = size(im)
a_w = wn2 + 1
b_w = w - wn2
a_h = hn2 + 1
b_h = h - hn2

im_density = get_density_map_gaussian(im, annPoints)
for j = 1:N

x = floor((b_w - a_w) * rand + a_w)
y = floor((b_h - a_h) * rand + a_h)
x1 = x - wn2
y1 = y - hn2
x2 = x + wn2 - 1
y2 = y + hn2 - 1

im_sampled = im(y1:y2, x1: x2,:)
im_density_sampled = im_density(y1:y2, x1: x2)

annPoints_sampled = annPoints(annPoints(:, 1) > x1 & ...
annPoints(:, 1) < x2 & ...
annPoints(:, 2) > y1 & ...
annPoints(:, 2) < y2,:);
annPoints_sampled(:, 1) = annPoints_sampled(:, 1) - x1
annPoints_sampled(:, 2) = annPoints_sampled(:, 2) - y1
img_idx = strcat(num2str(i), '_', num2str(j))

if (idx < num_val)
    imwrite(im_sampled, [val_path_img num2str(img_idx) '.jpg'])
    csvwrite([val_path_den num2str(img_idx) '.csv'], im_density_sampled)
else
    imwrite(im_sampled, [train_path_img num2str(img_idx) '.jpg'])
    csvwrite([train_path_den num2str(img_idx) '.csv'], im_density_sampled)
end

end

end

