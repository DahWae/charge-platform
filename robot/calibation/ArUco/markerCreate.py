import numpy as np
import cv2
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl

workdir = "./marker/"
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
marker = aruco.drawMarker(aruco_dict, 1, 2000)
cv2.imwrite(workdir + "marker.png", marker)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.imshow(marker, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")
plt.show()