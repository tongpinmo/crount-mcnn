#include "get_cut_center.hpp"


int CountLines(char *filename)
{
    std::ifstream ReadFile;
    int n = 0;
    std::string tmp;
    ReadFile.open(filename, std::ios::in); // read only

    while (getline(ReadFile, tmp, '\n')) {
        n++;
    }
    ReadFile.close();
    return n;
}


int get_img(char *ImgPath, char *ResultName_, int Dst_img_width,
            int Dst_img_height, int ImgBeginX, int ImgBeginY)
{
    cv::Mat Img = cv::imread(ImgPath);
    if (!Img.data) { cout << "can't open img" << endl; return -1; }

    cv::Mat SubImg = Mat::zeros(Dst_img_height, Dst_img_width, CV_8UC3);
    for (int i = 0; i<Dst_img_height; i++) {
        for (int j = 0; j<Dst_img_width; j++) {
            SubImg.at<Vec3b>(i, j) = Img.at<Vec3b>
                    (ImgBeginY + i, ImgBeginX + j);
        }
    }

    std::string ResultName = ResultName_;
    cv::imwrite(ResultName, SubImg);

    return 0;

}


int cut_img(char *palm_file, char *palmxyfile, int N_small_img, int Size_small_img,
            char *palm_box, char *img_name_, int ImgBeginX, int ImgBeginY )
{
    srand((unsigned)time(NULL));
    Mat youngpalm   = imread(palm_file); //after getted_image
    Mat palm        = youngpalm.clone();
    int nline       = CountLines(palmxyfile);//the origin gt file :06Months.txt
    int nwidth      = youngpalm.cols;
    int nheight     = youngpalm.rows;

    ofstream palmboxfile(palm_box, ios::app);//the gt_palm.txt we want to get
    for (int i = 0; i < N_small_img; i++)
    {
        int X_Top_Left_position = (int)rand() % (nwidth  - Size_small_img);//random integer
        int Y_Top_Left_position = (int)rand() % (nheight - Size_small_img);
        int X_Bottom_Right_position = X_Top_Left_position + Size_small_img;
        int Y_Bottom_Right_position = Y_Top_Left_position + Size_small_img;
        string filename = "0000.jpg";
        std::string img_name = img_name_; // the name of each training sample image

        if (i < 10) {
            filename[0] = '0';        
            filename[1] = '0';
            filename[2] = '0';
            filename[3] = i % 10 + '0';
        }
        else if (i < 100) {
            filename[0] = '0';
            filename[1] = '0';
            filename[2] = i / 10 + '0';
            filename[3] = i % 10 + '0';
        }
        else if (i < 1000) {
            filename[0] = '0';
            filename[1] = i / 100 + '0';
            filename[2] = (i % 100) / 10 + '0';
            filename[3] = i % 100 % 10 + '0';
        }
        else {
            filename[0] = i / 1000 + '0';
            filename[1] = (i / 100) % 10 + '0';
            filename[2] = (i % 100) / 10 + '0';
            filename[3] = (i % 100) % 10 + '0';
        }
        img_name += filename;
        ifstream xyFile(palmxyfile);//read origin 06Months.txt

        double **palmxyarray = new double *[nline];
        double **BOX_xyarray = new double *[nline];

        int index = 0;
        for (int j = 0; j < nline; j++)
        {

            palmxyarray[j] = new double[3];
            BOX_xyarray[j] = new double[4];

            xyFile >> palmxyarray[j][0];//x offset
            xyFile >> palmxyarray[j][1];//y offset


            int center_left_x = palmxyarray[j][0]  - ImgBeginX ;
            int center_left_y = palmxyarray[j][1]  - ImgBeginY ;

            //calculate how many trees in the box size of 500*500
            if (center_left_x > X_Top_Left_position && center_left_y >
                Y_Top_Left_position && center_left_x < X_Bottom_Right_position &&
                center_left_y < Y_Bottom_Right_position) {

                BOX_xyarray[index][0] = center_left_x  - X_Top_Left_position;
                BOX_xyarray[index][1] = center_left_y  - Y_Top_Left_position;

                index++;
            }
        }

        if (index == 0) continue;
        //get 500*500 picture
        cv::Mat SubImg = Mat::zeros(Size_small_img, Size_small_img, CV_8UC3);
        for (int ii = 0; ii<Size_small_img; ii++) {
            for (int jj = 0; jj<Size_small_img; jj++) {
                SubImg.at<Vec3b>(ii, jj) = youngpalm.at<Vec3b>
                        (Y_Top_Left_position + ii, X_Top_Left_position + jj);
            }
        }
        cv::imwrite(img_name, SubImg);

        palmboxfile << img_name << " ";
        palmboxfile << index << " ";
        for (int k = 0; k < index; k++) {
            palmboxfile << BOX_xyarray[k][0] << " ";
            palmboxfile << BOX_xyarray[k][1] << " ";
        }
        palmboxfile << endl;
    }

    return 0;
}

