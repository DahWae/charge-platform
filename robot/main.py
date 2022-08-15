# system package
import json
import multiprocessing
import asyncio
import cv2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import numpy as np

import uvicorn

# self package
import camera
import amr
import arm


class Target(BaseModel):
    space: str
    leaveTime: datetime.datetime = None
    tStamp: int = None
    power: int = None


class RobotStatus:
    target: Target = None
    status: str = 'idle'
    startFlag: bool = False


robot = RobotStatus()


def subP(coords, inView):
    cam = cv2.VideoCapture(0)
    coordAll = []
    while True:
        ret, frame = cam.read()

        coord = camera.getCoord(frame=frame)

        if coord is not None:

            coordAll.append(coord)

            if len(coordAll) > 30:
                allCoord = [[] for _ in range(6)]
                allStd = [[] for _ in range(6)]
                averageCoord = [0, 0, 0, 0, 0, 0]

                for e in coordAll:
                    for i, j in enumerate(e):
                        allCoord[i].append(j)
                        averageCoord[i] += j/len(coordAll)

                testPass = 1
                inView.value = 0

                for i, e in enumerate(allCoord):
                    allStd[i] = np.std(e)
                    if allStd[i] > 3:
                        testPass = 0
                        break

                if testPass:
                    inView.value = 1
                    # print(averageCoord)
                    for i in range(6):
                        coords[i] = averageCoord[i]

                coordAll = []

        else:
            inView.value = 0


def printPosition():
    print(amr.currentXY())
    return


async def goCharge(target: Target):

    robot.status = 'charge'
    robot.target = target
    robot.startFlag = True

    '''
    try:
        # AMR
        allPoint = amr.currentAllGoalPoint()
        # match target.space and GoalPoint coordination
        matchedPoint = contains(allPoint, lambda x: x['name'] == target.space)
        if matchedPoint is None:
            print('ERR, Point not found')
            return

        amr.moveToGoal(matchedPoint)
        await asyncio.sleep(1)
        while(amr.currentStatus() == 'running'):
            await asyncio.sleep(2)

        print(amr.startMagneticFind())
        await asyncio.sleep(1)
        while(amr.magneticState() == 1):
            await asyncio.sleep(2)

        print(amr.startMagneticGoal())
        await asyncio.sleep(1)
        while(amr.magneticState() == 1):
            await asyncio.sleep(2)
    except amr.ConnectionError:
        print('AMR Connection ERROR')
        return
    '''

    # ARM
    await arm.setPose(client=c, pose='prep')

    await asyncio.sleep(3)

    onTarget = None
    aiming = True

    while aiming:
        aiming = False
        for _ in range(20):
            if inView.value == 1:

                onTarget = camera.onTarget(coords)
                if onTarget:
                    await arm.setPose(client=c, pose='ready', coord=coords)
                else:
                    aiming = True
                    await arm.setPose(client=c, pose='aim', coord=coords)
                break

            else:
                print('no marker found')

            await asyncio.sleep(0.5)

    await arm.setPose(client=c, pose='plug')
    

    robot.startFlag = False

    return


async def goReturn():

    robot.status = 'return'
    robot.target = None
    robot.startFlag = True

    print('test')
    # ARM
    await arm.setPose(client=c, pose='unplug')
    await arm.setPose(client=c, pose='prep')
    await arm.setPose(client=c, pose='default')


    # AMR
    '''
    try:
        allPoint = amr.currentAllGoalPoint()
        # match target to Base
        matchedPoint = contains(allPoint, lambda x: x['name'] == 'P0')
        if matchedPoint is None:
            print('ERR, Point not found')
            return
        amr.moveToGoal(matchedPoint)
        await asyncio.sleep(1)
        while(amr.currentStatus() == 'running'):
            await asyncio.sleep(2)
        amr.startMagneticFind()
        while(amr.magneticState()):
            await asyncio.sleep(2)
        amr.startMagneticGoal()
        while(amr.magneticState()):
            await asyncio.sleep(2)
    except amr.ConnectionError:
        print('AMR Connection ERROR')
        return
    '''
    robot.status = 'idle'
    robot.startFlag = False

    return


def contains(list, filter):
    for x in list:
        if filter(x):
            return x
    return None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)


@app.post('/action/charge')
async def chargeTarget(target: Target):
    print(robot.status)
    if robot.status == 'idle':
        if robot.startFlag == False:
            print('start of charge')
            asyncio.create_task(goCharge(robot.target))
            return {'message': 'True'}
        print('Robot is in use!!')
    else:
        print('Status ERROR!!')
        return {'message': 'False'}


@app.post('/action/return')
async def returnToBase():
    print(robot.status)
    if robot.status == 'charge':
        if robot.startFlag == False:
            print('start of return')
            asyncio.create_task(goReturn())
            return {'message': 'True'}
        print('Robot is in use!!')
    else:
        print('Status ERROR!!')
        return {'message': 'False'}


@app.get('/action/status')
async def returnStatus():
    return {'amrStatus': amr.currentStatus, 'robotStatus': json.dumps(robot.__dict__)}


@app.post('/test')
async def testResponse(test: str):
    print(test)
    cnt = 0
    while True:
        print(cnt)
        cnt += 1
        await asyncio.sleep(1)
        if cnt > 30:
            break
    return {'message': 'Response'}


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    coords = multiprocessing.Array('d', 6)
    inView = multiprocessing.Value('i', 0)
    multiprocessing.Process(target=subP, args=(coords, inView)).start()

    # try:
    #     amr.annulment()
    #     amr.stopMagnetic()
    # except amr.ConnectionError:
    #     print('AMR Connection ERROR')

    try:
        c = arm.openClient()

        asyncio.run(arm.setPose(client=c, pose='default'))

    except arm.ConnectionERROR:
        print('Robot Arm Connection ERROR')

    uvicorn.run(app, host='0.0.0.0', port=8000)
