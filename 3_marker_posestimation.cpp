#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>
#include <cmath>
#include <iostream>


int main(){

    //detection
    cv::Mat inputImage, outputImage;
    inputImage = cv::imread("./results/lenova_7cam.png");
    inputImage.copyTo(outputImage);

    std::vector<int> markerIds;
    std::vector<std::vector<cv::Point2f>> markerCorners;
    cv::Ptr<cv::aruco::Dictionary> dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_6X6_50);
    cv::aruco::detectMarkers(inputImage, dictionary, markerCorners, markerIds);
    

    //estimation
    int image_width = 1920;
    int image_height = 1080;
    float fov = 95;
    float fovx = 47.5;
    float fovy = 47.5;
    float fx = image_width / (2.0f * std::tan(fovx * M_PI / 360.0f));
    float cx = image_width / 2.0f;
    float fy = image_height / (2.0f * std::tan(fovy * M_PI / 360.0f));
    float cy = image_height / 2.0f;
    cv::Mat cameraMatrix, distCoeffs;
    cameraMatrix = (cv::Mat_<float>(3,3) << fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0);
    distCoeffs = (cv::Mat_<float>(1,5) < 0, 0, 0, 0, 0); // << rd1, rd2, td1, td2, rd3);
    std::vector<cv::Vec3d> rvecs, tvecs;

    if (markerIds.size() > 0)
    {
        std::cout << "Detected " << markerIds.size() << " markers." << std::endl;
        cv::aruco::drawDetectedMarkers(outputImage, markerCorners, markerIds);
        cv::aruco::estimatePoseSingleMarkers(markerCorners, 0.05, cameraMatrix, distCoeffs, rvecs, tvecs);

        // draw axis for each marker
        for(int i=0; i<markerIds.size(); i++)
            cv::drawFrameAxes(outputImage, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], 0.1);
    }
    cv::imwrite("./results/lenova_7cam_pose.png", outputImage);

}