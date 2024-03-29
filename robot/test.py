
import time
import requests
import datetime
import asyncio
import cv2
import pickle
import numpy as np

import amr
import arm
import camera


class Target:
    space: str
    leaveTime: datetime.datetime = None
    tStamp: int = None
    power: int = None


robotUrl = 'http://127.0.0.1'  # TODO: change the url


def contains(list, filter):
    for x in list:
        if filter(x):
            return x
    return False


def chargeTest():
    path = robotUrl + ':8000/action/charge'
    json = {
        'space': 'P1',
    }
    r = requests.post(url=path, json=json)
    print(r.text)
    return


def returnTest():
    path = robotUrl + ':8000/action/return'
    r = requests.post(url=path)
    print(r.text)
    return


def apiTest():
    path = robotUrl + ':8000/test'
    params = {'test': '123'}
    r = requests.post(url=path, params=params)
    print(r.text)
    return


def amrTest():
    # allPoint = amr.currentAllGoalPoint()
    # print('all point loaded')
    # # match target.space and GoalPoint coordination
    # matchedPoint = contains(allPoint, lambda x: x['name'] == 'P1')
    # if matchedPoint is None:
    #     print('ERR, Point not found')
    #     return
    # print('point found, moving')
    # print(matchedPoint)
    # print(amr.moveToGoal(matchedPoint))
    # print('end of moving')
    # print(amr.currentXY())
    # while True:
    #     print(amr.currentStatus())
    #     time.sleep(2)

    # print(amr.getAllMap())
    # mapName = amr.currentMap()
    # print(mapName)
    # print(amr.allGoalPoint(name=mapName))
    # print(amr.currentAllGoalPoint())

    print(amr.startMagneticGoal(name=0))

    # print(amr.allGoalPoint(name='Uni'))
    # mapName = amr.currentMap()
    # print(mapName)
    # print(amr.currentAllGoalPoint())
    # temp = amr.allGoalPoint(name='map')
    # temp = amr.updateGoalPoint(mapName=mapName, pointName='P0', newPointName='Base')
    # temp = amr.moveToGoal()
    # print(temp)
    return


async def armTest(c, mode):

    if(arm.getReturn(client=c) == 0):
        match mode:

            case 0:
                print('return mode')
                arm.postState(client=c, state=1)
                await asyncio.sleep(1)
                arm.postState(client=c, state=0)

            case 1:
                print('ready mode')
                arm.postState(client=c, state=2)
                await asyncio.sleep(0.5)
                print(arm.getReturn(client=c))
                while(arm.getReturn(client=c) == 1):
                    await asyncio.sleep(0.5)
                    arm.postState(client=c, state=0)
                    print('waiting')

            case 2:
                print('test mode')
                cam = cv2.VideoCapture(0)
                coords = []
                coords.append([-100, 0, -50, 0, 15, 0])
                coords.append([0, -150, 0, -20, -5, 0])
                coords.append([-50, -50, -50, -25, 5, 45])
                coords.append([50, -30, 0, -10, -15, 30])
                coords.append([-30, 50, 0, 10, 10, -90])

                ans = []
                hans = []

                for item in coords:
                    arm.postCoord(client=c, coords=item)
                    arm.postState(client=c, state=6)

                    await asyncio.sleep(1)
                    print(arm.getReturn(client=c))

                    while(arm.getReturn(client=c) == 1):
                        await asyncio.sleep(0.5)
                        arm.postState(client=c, state=0)
                        print('waiting')

                    coord = []

                    for _ in range(300):
                        ret, frame = cam.read()
                        cv2.imshow('frame', frame)

                        capture = camera.getCoord(frame=frame)

                        if capture is not None:
                            print('captured')
                            coord.append(capture)

                            if len(coord)>30:
                                allCoord=[[] for _ in range(6)]
                                allStd=[[] for _ in range(6)]
                                averageCoord=[0,0,0,0,0,0]
                                for e in coord:
                                    for i, j in enumerate(e):
                                        allCoord[i].append(j)
                                        averageCoord[i] += j/len(coord)
                                        
                                testPass = 1
                                for i, e in enumerate(allCoord):
                                    allStd[i] = np.std(e)
                                    if allStd[i]>3:
                                        testPass=0
                                        break
                                if testPass:
                                    # print(allStd)
                                    print(averageCoord)
                                    ans.append(averageCoord)
                                    pose = arm.getCoord(client=c)
                                    hans.append(pose)
                                    break

                                coord = []

                        else:
                            print('coord is None!!')

                f = open('./result/eyeHandCali.pckl', 'wb')
                fh = open('./result/handCoord.pckl', 'wb')
                pickle.dump((ans), f)
                pickle.dump((hans), fh)
                f.close()
                fh.close()

                print(hans)
                print(ans)
            case 3:
                print('test coord')
                coords = []
                coords.append([0, 0, 0, 0, 0, 3])

                for item in coords:
                    arm.postCoord(client=c, coords=item)
                    arm.postState(client=c, state=6)
                    await asyncio.sleep(1)
                    print(arm.getReturn(client=c))
                    while(arm.getReturn(client=c) == 1):
                        await asyncio.sleep(0.5)
                        arm.postState(client=c, state=0)
                        print('waiting')

            case 4:
                print('reading mode')
                ret = arm.getCoord(client=c)
                for el in ret:
                    print(el)

    else:
        print('reset mode')
        arm.postState(client=c, state=1)

    print('end')

if __name__ == '__main__':
    c = arm.openClient()
    # while True:
        # coord = arm.getCoord(client=c)
        # print(coord)
        # asyncio.run(asyncio.sleep(0.5))
    chargeTest()
    # returnTest()
    # apiTest()
    # amrTest()
    # amr.annulment()
    # amr.stopMagnetic()
    # asyncio.run(armTest(c=c, mode=1))
