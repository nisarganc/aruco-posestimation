#include <opencv2/aruco.hpp>
#include <opencv2/imgcodecs.hpp> 
#include <opencv2/highgui.hpp> 

int main()
    {
        cv::Mat markerImage;
        cv::Ptr<cv::aruco::Dictionary> dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_6X6_50);
        // pix = (16cm * 300dpi)/2.54 = 1889.8
        cv::aruco::drawMarker(dictionary, 49, 1889.8, markerImage, 1);
        cv::imwrite("marker49.png", markerImage);
        return 0;
    }
