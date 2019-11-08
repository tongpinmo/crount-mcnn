%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% File to create grount truth density map for test set%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


clc; clear all;
%path = ['../data/acacia-test/12months/Palm_test_12/'];
%gt_path = ['../data/acacia-test/12months/ground_truth/'];
%gt_path_csv = ['../data/acacia-test/12months/ground_truth_csv/'];
%test_txt = ['../data/acacia-test/12months/test_12.txt'];

path = ['../data/acacia-test/6months/Palm_test_06/'];
gt_path = ['../data/acacia-test/6months/ground_truth/'];
gt_path_csv = ['../data/acacia-test/6months/ground_truth_csv/'];
test_txt = ['../data/acacia-test/6months/test_06.txt'];

mkdir(gt_path_csv)


test_file = fopen(test_txt,'r');
test_content = textscan(test_file,'%s');              %cell

num_images = length(test_content{1});
num_val = ceil(num_images*0.1);

for i = 1:num_images    
    if (mod(i,10)==0)
        fprintf(1,'Processing %3d/%d files\n', i, num_images);
    end
    
    input_img_name = strcat(path,test_content{1}{i},'.jpg');
    %disp(input_img_name)
    input_img_split = strsplit(test_content{1}{i},'.')
    input_img_num = input_img_split{1}
    disp(input_img_num)
    
    matfile = load(strcat(gt_path,input_img_num,'.mat'))
    im = imread(input_img_name);
    [h, w, c] = size(im);
    if (c == 3)
        im = rgb2gray(im);
    end     
    annPoints = matfile.('image_info')  
    [h, w, c] = size(im);
    im_density = get_density_map_gaussian(im,annPoints);    
    csvwrite([gt_path_csv,input_img_num '.csv'], im_density);       
end
