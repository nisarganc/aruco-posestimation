import numpy as np
import cv2 as cv

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((12*8,3), np.float32)
objp[:,:2] = np.mgrid[0:12,0:8].T.reshape(-1,2)
objp *= 31 # 31mm squares

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

cap = cv.VideoCapture(4)
cap.set(cv.CAP_PROP_FPS, 5)

width_value = 1920  # camera's max width
height_value = 1080  # camera's max height

cap.set(cv.CAP_PROP_FRAME_WIDTH, width_value)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height_value)

# create video
fourcc = cv.VideoWriter_fourcc(*"mp4v")
video_writer = cv.VideoWriter("calibration_video_1.mp4", fourcc, 5, (width_value, height_value))

# write video
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow('Camera feed', frame)
    key = cv.waitKey(1) & 0xFF

    video_writer.write(frame)

    if key == ord('q'):
        video_writer.release()
        break
