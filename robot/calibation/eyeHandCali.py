import pickle
import cv2
from scipy.spatial.transform import Rotation as R
import numpy as np


fh = open('../result/handCoord.pckl', 'rb')
fe = open('../result/eyeHandCali.pckl', 'rb')

hand = pickle.load(fh)
ans = pickle.load(fe)

for el in hand:
    print(el)

for j  in range(len(hand)):
#     for i in range(3):
#         hand[j][3+i] = hand[j][3+i]/360*np.pi
    test = R.from_euler('XYZ', hand[j][3:], degrees=True).as_matrix()
    print(test)