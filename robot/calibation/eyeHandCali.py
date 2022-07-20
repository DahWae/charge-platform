import pickle
import cv2
from scipy.spatial.transform import Rotation as R
import numpy as np

def rot2eul(R):
    beta = -np.arcsin(R[2, 0])
    alpha = np.arctan2(R[2, 1]/np.cos(beta), R[2, 2]/np.cos(beta))
    gamma = np.arctan2(R[1, 0]/np.cos(beta), R[0, 0]/np.cos(beta))
    return np.array((alpha, beta, gamma))

if __name__ == '__main__':

    fh = open('../result/handCoord.pckl', 'rb')
    fe = open('../result/eyeHandCali.pckl', 'rb')

    hand = pickle.load(fh)
    eye = pickle.load(fe)

    Ts_hand2base_all = []
    Ts_cam2board_all = []


    for el in hand:
        print(el)

    for i in range(len(hand)):
        tvecH = [float(el) for el in hand[i][:3]]
        rvecH = R.from_euler('XYZ', hand[i][3:], degrees=True).as_matrix()

        Ts_H = np.zeros((4, 4))

        Ts_H[:3, :3] = rvecH
        Ts_H[:3, 3] = np.array(tvecH).flatten()
        Ts_H[3, 3] = 1

        Ts_hand2base_all.append(Ts_H)

        tvecE = [float(el) for el in eye[i][:3]]
        rvecE = R.from_euler('XYZ', eye[i][3:], degrees=True).as_matrix()

        Ts_E = np.zeros((4, 4))

        Ts_E[:3, :3] = rvecE
        Ts_E[:3, 3] = np.array(tvecE).flatten()
        Ts_E[3, 3] = 1

        Ts_cam2board_all.append(Ts_E)

    R_base2hand = []
    T_base2hand = []
    R_board2cam = []
    T_board2cam = []

    R_hand2base = []
    T_hand2base = []
    R_cam2board = []
    T_cam2board = []

    for i in range(len(Ts_hand2base_all)):
        Ts_base2hand_all = np.linalg.inv(Ts_hand2base_all[i])
        R_base2hand.append(np.array(Ts_base2hand_all[:3, :3]))
        T_base2hand.append(np.array(Ts_base2hand_all[:3, 3]))
        # R_base2hand.append(np.array(Ts_hand2base_all[i][:3, :3]))
        # T_base2hand.append(np.array(Ts_hand2base_all[i][:3, 3]))
        R_board2cam.append(np.array(Ts_cam2board_all[i][:3, :3]))
        T_board2cam.append(np.array(Ts_cam2board_all[i][:3, 3]))

    # print(tvecH)
    # print(type(tvecH[0][0]))
    rvecE2H, tvecE2H = cv2.calibrateHandEye(R_base2hand, T_base2hand, R_board2cam, T_board2cam)

    print(rvecE2H)
    print(tvecE2H)


    rotM, jacobian = cv2.Rodrigues(rvecE2H)

    print(rotM[0, 0])
    # ang = rot2eul(rotM)  # yaw, pitch, row
    ang=rotM

    for j, e in enumerate(ang):
        ang[j] = e/np.pi*180

    # if ang[0]<0:
    #     ang[0]=ang[0]+360
    # ang[0] = ang[0]-180
    
    temp =[]

    temp.append(tvecE2H[0,0])  # x    (mm)
    temp.append(tvecE2H[1,0])  # y    (mm)
    temp.append(tvecE2H[2,0])  # z    (mm)
    temp.append(ang[0,0])             # rx    (deg)
    temp.append(ang[1,0])             # ry    (deg)
    temp.append(ang[2,0])             # rz    (deg）

    print(temp)