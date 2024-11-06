import numpy as np
import cv2 as cv

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((12*8,3), np.float32)
objp[:,:2] = np.mgrid[0:12,0:8].T.reshape(-1,2)
objp *= 31

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

cap = cv.VideoCapture(4)

width_value = 1920  # Replace with your camera's max width
height_value = 1080  # Replace with your camera's max height


cap.set(cv.CAP_PROP_FRAME_WIDTH, width_value)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height_value)

while True:

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow('Camera feed', frame)
    key = cv.waitKey(1) & 0xFF

    ret, corners = cv.findChessboardCorners(gray, (12, 8), None)

    # Draw and display the corners if found
    if key == ord('s') and ret:
        cv.drawChessboardCorners(frame, (12, 8), corners, ret)
        cv.imshow('Chessboard corners', frame)
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        print("Captured frame for calibration")
    else:
        print("Chessboard corners not found")
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

# Perform camera calibration if we have collected any samples
if len(objpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print("Camera calibrated successfully")
    print("Camera matrix:", mtx)
    print("Distortion coefficients:", dist)
else:
    print("No frames captured for calibration")
