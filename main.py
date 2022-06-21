# system package
import time
import multiprocessing
import cv2
import sys

# self package
import camera
import amr
import arm


def subPTest(cnt):
    while True:
        cnt.value = cnt.value+1
        time.sleep(2)


def subP(coords, inView):
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        coord = camera.getCoord(frame=frame)
        if coord is not None:
            inView.value = 1
            for i in range(6):
                coords[i] = coord[0][i]
        else:
            inView.value = 0


if __name__ == '__main__':
    coords = multiprocessing.Array('d', 6)
    inView = multiprocessing.Value('i', 0)

    # cnt = multiprocessing.Value('i', 0)   # child test
    # multiprocessing.Process(target=subPTest, args=(cnt,)).start()

    multiprocessing.Process(target=subP, args=(coords, inView)).start()
    c = arm.openClient(host='192.168.0.29', port=502)

    while True:

        print(arm.getReturn(client=c))

        match arm.getReturn(client=c):
            case 0:  # active mode
                if inView.value:   # marker found
                    arm.postCoord(client=c, coords=coords)
                    # start after the coordinate is given
                    arm.postState(client=c, state=1)
                    print('posted')
            case 1:  # hold mode
                arm.postState(client=c, state=2)
            case 2:  # idle mode
                arm.postState(client=c, state=0)
                
