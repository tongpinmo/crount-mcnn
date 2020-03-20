import os
import torch
import numpy as np

from src.crowd_count import CrowdCounter
from src import network
from src.data_loader import ImageDataLoader
from src import utils

torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = False
vis = False
save_output = True

data_path = './data/acacia-test/12months/Palm_test_12/'
gt_path = './data/acacia-test/12months/ground_truth_csv/'
model_path = './acacia_saved_models/mcnn_acacia_36.h5'

output_dir = './output/'
model_name = os.path.basename(model_path).split('.')[0]
file_results = os.path.join(output_dir, 'results_' + model_name + '_.txt')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
output_dir = os.path.join(output_dir, 'density_maps_' + model_name)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

net = CrowdCounter()

trained_model = os.path.join(model_path)
network.load_net(trained_model, net)
net.cuda()
net.eval()
mae = 0.0
rmse = 0.0
mrmse = 0.0

# load test data
data_loader = ImageDataLoader(data_path, gt_path, shuffle=False, gt_downsample=True, pre_load=True)

for blob in data_loader:
    im_data = blob['data']
    gt_data = blob['gt_density']
    # print('gt_data: ',gt_data)
    density_map = net(im_data, gt_data)
    density_map = density_map.data.cpu().numpy()
    # print('density_map: ',density_map)
    gt_count = np.sum(gt_data)
    # print('gt_count: ',gt_count)
    et_count = np.sum(density_map)
    # print('et_count: ',et_count)
    mae += abs(gt_count - et_count)
    rmse += ((gt_count - et_count) * (gt_count - et_count))
    if vis:
        utils.display_results(im_data, gt_data, density_map)
    if save_output:
        utils.save_density_map(density_map, output_dir, 'output_' + blob['fname'].split('.')[0] + '.png')

mae = mae / data_loader.get_num_samples()
rmse = np.sqrt(rmse / data_loader.get_num_samples())
print('rmse: ',rmse)
mrmse = np.sqrt(rmse / data_loader.get_num_samples()).mean()
print('\nMAE: %0.3f, RMSE: %0.3f' % (mae, rmse))
print('\nmRMSE:%0.3f'%(mrmse))

f = open(file_results, 'w')
f.write('MAE: %0.3f, MSE: %0.3f' % (mae, rmse))
f.close()