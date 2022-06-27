import numpy as np
import cv2
from cv2 import aruco
import pickle
import math

# ArUco variables
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)
ARUCO_LENGTH = 0.033

# camera parameters
f = open('./cfg/calibrationC310.pckl', 'rb')
cameraMatrix, distCoeffs, rvecs, tvecs = pickle.load(f)

def rot2eul(R):
    beta = -np.arcsin(R[2, 0])
    alpha = np.arctan2(R[2, 1]/np.cos(beta), R[2, 2]/np.cos(beta))
    gamma = np.arctan2(R[1, 0]/np.cos(beta), R[0, 0]/np.cos(beta))
    return np.array((alpha, beta, gamma))


def eul2rot(theta):

    R = np.array([[np.cos(theta[1])*np.cos(theta[2]),       np.sin(theta[0])*np.sin(theta[1])*np.cos(theta[2]) - np.sin(theta[2])*np.cos(theta[0]),      np.sin(theta[1])*np.cos(theta[0])*np.cos(theta[2]) + np.sin(theta[0])*np.sin(theta[2])],
                  [np.sin(theta[2])*np.cos(theta[1]),       np.sin(theta[0])*np.sin(theta[1])*np.sin(theta[2]) + np.cos(theta[0])
                   * np.cos(theta[2]),      np.sin(theta[1])*np.sin(theta[2])*np.cos(theta[0]) - np.sin(theta[0])*np.cos(theta[2])],
                  [-np.sin(theta[1]),                        np.sin(theta[0])*np.cos(theta[1]),                                                           np.cos(theta[0])*np.cos(theta[1])]])

    return R

def getCoord(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # If our image size is unknown, set it now
    # if not image_size:
    #     image_size = gray.shape[::-1]

    # Find aruco markers in the query image
    corners, ids, _ = aruco.detectMarkers(
        image=gray,
        dictionary=ARUCO_DICT)

    # Outline the aruco markers found in our query image
    frame = aruco.drawDetectedMarkers(
        image=frame,
        corners=corners)

    coord = None
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
            corners=corners,
            markerLength=ARUCO_LENGTH,
            cameraMatrix=cameraMatrix,
            distCoeffs=distCoeffs)

        (rvec-tvec).any()

        # print('rvec: {}, tvec: {}'.format(rvec, tvec))
        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, cameraMatrix, distCoeffs,
                           rvec[i, :, :], tvec[i, :, :], ARUCO_LENGTH/2)

            temp = []

            rotM, jacobian = cv2.Rodrigues(rvec[i])
            ang = rot2eul(rotM)  # yaw, pitch, row

            for j, e in enumerate(ang):
                ang[j] = e/math.pi*180

            if ang[0]<0:
                ang[0]=ang[0]+360
            ang[0] = ang[0]-180
            
            temp.append(tvec[i, 0, 0]*1000)  # x    (mm)
            temp.append(tvec[i, 0, 1]*1000)  # y    (mm)
            temp.append(tvec[i, 0, 2]*1000)  # z    (mm)
            temp.append(ang[0])             # rx    (deg)
            temp.append(ang[1])             # ry    (deg)
            temp.append(ang[2])             # rz    (deg)

            coord = []
            coord.append(temp)
        return coord
    else:
        return None