# system package
import multiprocessing
import asyncio
import cv2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime

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
    while True:
        ret, frame = cam.read()
        coord = camera.getCoord(frame=frame)
        if coord is not None:
            inView.value = 1
            for i in range(6):
                coords[i] = coord[0][i]
        else:
            inView.value = 0


def printPosition():
    print(amr.currentXY())
    return


async def goCharge(target):
    # AMR
    printPosition()
    allPoint = amr.currentAllGoalPoint()
    print('all point loaded')
    # match target.space and GoalPoint coordination
    matchedPoint = contains(allPoint, lambda x: x['name'] == target.space)
    if matchedPoint is None:
        print('ERR, Point not found')
        return
    print('point found, moving')
    print(matchedPoint)
    print(amr.moveToGoal(matchedPoint))
    await asyncio.sleep(1)
    while(amr.currentStatus() == 'running'):
        print('still moving')
        await asyncio.sleep(2)
    print('start magnetic find')
    print(amr.startMagneticFind())
    await asyncio.sleep(1)
    while(amr.magneticState() == 1):
        print('still finding')
        await asyncio.sleep(2)
    print('start magnetic goal')
    print(amr.startMagneticGoal())
    await asyncio.sleep(1)
    while(amr.magneticState() == 1):
        print('still tracing')
        await asyncio.sleep(2)
    print('end of charge')

    # ARM
    # arm.postCoord(client=c, coords=coords)
    # arm.postState(client=c, state=1)
    # while(~arm.getReturn(client=c)):
    #     None
    # arm.postState(client=c, state=2)
    return


async def goReturn():
    # ARM

    # AMR
    allPoint = amr.currentAllGoalPoint()
    # match target to Base
    matchedPoint = contains(allPoint, lambda x: x['name'] == 'P0')
    amr.moveToGoal(matchedPoint)
    # while(amr.currentStatus()):
    #     await asyncio.sleep(2)
    # amr.startMagneticFind()
    # while(amr.magneticState()):
    #     await asyncio.sleep(2)
    # amr.startMagneticGoal()
    # while(amr.magneticState()):
    #     await asyncio.sleep(2)
    return


def getRobotStatus():
    amrStatus = amr.currentStatus()

    return amrStatus


def contains(list, filter):
    for x in list:
        if filter(x):
            return x
    return False


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)


@app.post('/action/charge')
async def chargeTarget(target: Target):
    if robot.status == 'idle':
        if robot.startFlag == False:
            robot.status = 'charge'
            robot.target = target
            robot.startFlag = True
            print('start of charge')
            await goCharge(robot.target)
            robot.startFlag = False
            return True
    return False


@app.post('/action/return')
async def returnToBase():
    if robot.status == 'charge':
        if robot.startFlag == False:
            robot.status = 'return'
            robot.target = None
            robot.startFlag = True
            print('start of return')
            await goReturn()
            robot.status = 'idle'
            robot.startFlag = False
            return True
    return False


@app.get('/action/status')
async def returnStatus():
    return {'status': robot.status, 'startFlag': robot.startFlag}


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
    return 'Response'


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    coords = multiprocessing.Array('d', 6)
    inView = multiprocessing.Value('i', 0)
    # multiprocessing.Process(target=subP, args=(coords, inView)).start()

    print(amr.annulment())
    print(amr.stopMagnetic())

    c = arm.openClient()
    uvicorn.run(app, host='127.0.0.1', port=8000)

    # print('Service on')

    # while True:

    #     if robot.startFlag:
    #         match robot.status:
    #             case 'charge':
    #                 print('start of charge')
    #                 goCharge(robot.target)
    #                 robot.startFlag = False
    #             case 'return':
    #                 print('start of return')
    #                 goReturn()
    #                 robot.status = 'idle'
    #                 robot.startFlag = False

    #     print(arm.getReturn(client=c))

    #     match arm.getReturn(client=c):
    #         case 0:  # active mode
    #             if inView.value:   # marker found
    #                 arm.postCoord(client=c, coords=coords)
    #                 # start after the coordinate is given
    #                 arm.postState(client=c, state=1)
    #                 print('posted')
    #         case 1:  # hold mode
    #             arm.postState(client=c, state=2)
    #         case 2:  # idle mode
    #             arm.postState(client=c, state=0)
