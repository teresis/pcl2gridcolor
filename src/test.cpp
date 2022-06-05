#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>

using std::cout;
using std::ifstream;
using std::vector;
using std::string;
using std::stringstream;

#define HEADER_LINE_NUM 11

inline int scale_x(float f, float s, float min){
	return static_cast<int>(f/s + (-min+1));
}

inline int scale_z(float f, float s, float min){
	return static_cast<int>(f/s + (-min+1));
}

int main(int argc, char* argv[]){
	cout << "This is pcl converter\n";

	ifstream file;
	file.open(argv[1]);
	if(!file.is_open()){
		cout << "file open error\n";
		return 1;
	}
	int scale = std::stoi(argv[2]);	
	int threshold = std::stoi(argv[3]);


	int point_num = 0;
	for(int i = 0; i < HEADER_LINE_NUM; ++i){
		string line, word;
		getline(file, line);
		stringstream sstream(line);
		vector<string> tokens;
		while(getline(sstream, word, ' ')){
			tokens.push_back(word);
		}
		if(!tokens[0].compare("POINTS")){
			point_num = std::stoi(tokens[1]);
		}
	}

	vector<float> vec[3];
	unsigned char **gridmap = new unsigned char*[scale+10];
	for(int i =0; i<scale+10; ++i){
		gridmap[i] = new unsigned char[scale+10];
	}
	for(int i =0; i<scale+10; ++i){
		for(int j =0; j<scale+10; ++j){
			gridmap[i][j] = 0;
		}
	}
	for(int i = 0; i < point_num; ++i){
		string line, word;
		getline(file, line);
		std::istringstream in(line);
		float x,y,z;

		in >> x >> y >> z;
		vec[0].push_back(x);
		vec[1].push_back(y);
		vec[2].push_back(z);
	}


	int x_max = *max_element(vec[0].begin(), vec[0].end())+1;
	int x_min = *min_element(vec[0].begin(), vec[0].end())-1;	
	int x_diff = (x_max - x_min) ;

	int z_max = *max_element(vec[2].begin(), vec[2].end())+1;
	int z_min = *min_element(vec[2].begin(), vec[2].end())-1;
	int z_diff = (z_max - z_min) ;

	float s_z = z_diff/(float)scale;
	float s_x = x_diff/(float)scale;

	for(int i =0 ; i< point_num; ++i){
		float x,y,z;
		x = vec[0][i];
		y = vec[1][i];
		z = vec[2][i];
		int z_scale = scale_z(z, s_z, z_min/s_z);
		int x_scale = scale_x(x, s_x, x_min/s_x);
		
		gridmap[z_scale][x_scale]++;
	}


	for (int i = 0; i < scale + 10; ++i){
		for (int j=0; j< scale + 10; ++j){
			if(gridmap[i][j] > threshold) gridmap[i][j] = 255;
		}
	}

	cv::Mat mat = cv::Mat(scale+10, scale+10, CV_8U);
	
	for (int i = 0; i< scale+10; ++i){
		for(int j=0; j<scale+10; ++j){
			mat.at<unsigned char>(i,j) = gridmap[i][j];
		}
	}
	cv::Mat canny;
	cv::Mat img1,img2;
	cv::Canny(mat, canny, 100,150);

	cv::namedWindow("window1", cv::WINDOW_AUTOSIZE);
//	cv::namedWindow("window2", cv::WINDOW_AUTOSIZE);

	cv::resize(canny, img1, cv::Size(1000,1000));
	cv::resize(mat, img2, cv::Size(1000,1000));

	cv::imshow("window1", img1);
//	cv::imshow("window2", img2);
	cv::waitKey(0);
	return 0;
}
