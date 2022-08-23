# System information:
# - Linux Mint 18.1 Cinnamon 64-bit
# - Python 2.7 with OpenCV 3.2.0

import numpy as np
import cv2
from cv2 import aruco
import pickle
import glob


# ChAruco board variables
CHARUCOBOARD_ROWCOUNT = 7
CHARUCOBOARD_COLCOUNT = 5
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)

# Create constants to be passed into OpenCV and Aruco methods
CHARUCO_BOARD = aruco.CharucoBoard_create(
    squaresX=CHARUCOBOARD_COLCOUNT,
    squaresY=CHARUCOBOARD_ROWCOUNT,
    squareLength=0.036,
    markerLength=0.029,
    dictionary=ARUCO_DICT)

# Create the arrays and variables we'll use to store info like corners and IDs from images processed
f = open('./cfg/calibration.pckl', 'rb')
cameraMatrix, distCoeffs, rvecs, tvecs = pickle.load(f)
corners_all = []  # Corners discovered in all images processed
ids_all = []  # Aruco ids corresponding to corners discovered
image_size = None  # Determined at runtime


# This requires a camera you want to calibrate

cam = cv2.VideoCapture(0)

# Loop through camera
while True:
    # Turn on camera
    ret, img = cam.read()
    # Grayscale the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find aruco markers in the query image
    corners, ids, _ = aruco.detectMarkers(
        image=gray,
        dictionary=ARUCO_DICT)

    # Outline the aruco markers found in our query image
    img = aruco.drawDetectedMarkers(
        image=img,
        corners=corners)

    # Get charuco corners and ids from detected aruco markers
    if ids is not None:
        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=gray,
            board=CHARUCO_BOARD)

        # If a Charuco board was found, let's collect image/corner points
        # Requiring at least 20 squares
        if response > 20:
            # Add these corners and ids to our calibration arrays
            corners_all.append(charuco_corners)
            ids_all.append(charuco_ids)

            # Draw the Charuco board we've detected to show our calibrator the board was properly detected
            img = aruco.drawDetectedCornersCharuco(
                image=img,
                charucoCorners=charuco_corners,
                charucoIds=charuco_ids)

            # If our image size is unknown, set it now
            if not image_size:
                image_size = gray.shape[::-1]

            
            calibration, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
                charucoCorners=corners_all,
                charucoIds=ids_all,
                board=CHARUCO_BOARD,
                imageSize=image_size,
                cameraMatrix=cameraMatrix,
                distCoeffs=distCoeffs)

            print(cameraMatrix)
            print(distCoeffs)
            # # Reproportion the image, maxing width or height at 1000
            # proportion = max(img.shape) / 1000.0
            # img = cv2.resize(
            #     img, (int(img.shape[1]/proportion), int(img.shape[0]/proportion)))
            # # Pause to display each image, waiting for key press

    cv2.imshow('frame', img)

    key = cv2.waitKey(1)

    if key % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        cam.release()
        cv2.destroyAllWindows()
        break
# Destroy any open CV windows
cv2.destroyAllWindows()

# Make sure we were able to calibrate on at least one charucoboard by checking
# if we ever determined the image size
if not image_size:
    # Calibration failed because we didn't see any charucoboards of the PatternSize used
    print("Calibration was unsuccessful. We couldn't detect charucoboards in any of the images supplied. Try changing the patternSize passed into Charucoboard_create(), or try different pictures of charucoboards.")
    # Exit for failure
    exit()

# Now that we've seen all of our images, perform the camera calibration
# based on the set of points we've discovered
# calibration, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
#     charucoCorners=corners_all,
#     charucoIds=ids_all,
#     board=CHARUCO_BOARD,
#     imageSize=image_size,
#     cameraMatrix=None,
#     distCoeffs=None)

# Print matrix and distortion coefficient to the console
print(cameraMatrix)
print(distCoeffs)

# Save values to be used where matrix+dist is required, for instance for posture estimation
# I save files in a pickle file, but you can use yaml or whatever works for you
f = open('./cfg/calibration.pckl', 'wb')
pickle.dump((cameraMatrix, distCoeffs, rvecs, tvecs), f)
f.close()

# Print to console our success
print('Calibration successful. Calibration file used: {}'.format(
    './cfg/calibration.pckl'))
