import numpy as np
import cv2 as cv

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((12*8,3), np.float32)
objp[:,:2] = np.mgrid[0:12,0:8].T.reshape(-1,2)
objp *= 31 # 31mm squares

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

# read video from file
cap = cv.VideoCapture("calibration_video.mp4")
cap.set(cv.CAP_PROP_FPS, 5)
width_value = 1920  
height_value = 1080  
cap.set(cv.CAP_PROP_FRAME_WIDTH, width_value)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height_value)

while True:

    ret, frame = cap.read()

    if ret:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (12, 8), None)
        if corners is not None:
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            objpoints.append(objp)
            print('points detected')       
        else:
            print("points not found")
    else:
        break

cap.release()
cv.destroyAllWindows()

# Perform camera calibration if we have collected any samples
if len(objpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print("Camera matrix:", mtx)
    print("Distortion coefficients:", dist)
else:
    print("No frames captured for calibration")