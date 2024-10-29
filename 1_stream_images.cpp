#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // Open the camera. Change the index to match the USB camera if needed.
    cv::VideoCapture cap(6);  // Use 6 for USB camera, or device file on Linux

    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open the camera." << std::endl;
        return -1;
    }

    cv::Mat frame;
    while (true) {
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "Error: Could not read the frame." << std::endl;
            break;
        }

        cv::imshow("Camera Stream", frame);

        // Press 's' to save the current frame
        char c = (char)cv::waitKey(10);
        if (c == 's') {
            // Save the current frame to a file
            cv::imwrite("./results/lenova_7cam.png", frame);
            std::cout << "Image saved!" << std::endl;
        } else if (c == 'q') {
            // Press 'q' to quit the loop
            break;
        }
    }

    cap.release();
    cv::destroyAllWindows();

    return 0;
}