#include <stdio.h>
#include <fstream>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

#include <opencv/cv.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/video/video.hpp>

using namespace std;
using namespace cv;

extern "C" {
int CountLines(char *filename);
int get_img(char *ImgPath, char *ResultName_ , int Dst_img_width, int Dst_img_height, int ImgBeginX, int ImgBeginY);
int cut_img(char *palm_file, char *palmxyfile, int N_small_img, int Size_small_img, char *palm_box,char *img_name_,
            int ImgBeginX, int ImgBeginY );

}

