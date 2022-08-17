# system package
import jsons
import multiprocessing
import asyncio
import cv2
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import numpy as np
import sys
from loguru import logger

import uvicorn

# self package
import camera
import amr
import arm

logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")


class Target(BaseModel):
    space: str
    leaveTime: datetime.datetime = None
    tStamp: int = None
    power: int = None


class RobotStatus:
    target: Target = None
    status: str = 'idle'
    isAvailable: bool = True


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

    logger.info('Start of Charge Task')

    robot.status = 'arrive'
    robot.target = target
    robot.isAvailable = False

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
        logger.error('AMR Connection ERROR')
        robot.isAvailable = True
        return

    # ARM
    try:
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

    except arm.ConnectionERROR:
        logger.error('Robot Arm Connection ERROR')
        robot.isAvailable = True
        return

    robot.status = 'charge'
    robot.isAvailable = True

    logger.info('End of Charge Task')

    return


async def goReturn():

    logger.info('Start of Return Task')

    robot.status = 'return'
    robot.target = None
    robot.isAvailable = False

    # ARM
    try:
        await arm.setPose(client=c, pose='unplug')
        await arm.setPose(client=c, pose='prep')
        await arm.setPose(client=c, pose='default')

    except arm.ConnectionERROR:
        logger.error('Robot Arm Connection ERROR')
        robot.isAvailable = True
        return

    # AMR
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
        logger.error('AMR Connection ERROR')
        robot.isAvailable = True
        return

    robot.status = 'idle'
    robot.isAvailable = True

    logger.info('End of Return Task')

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
    if robot.status == 'idle':
        if robot.isAvailable == True:
            robot.target = target
            asyncio.create_task(goCharge(robot.target))
            return {'message': 'True'}
        logger.error('Robot in Use ERROR!!')
    else:
        logger.error('Status ERROR!!')
    return {'message': 'False'}


@app.post('/action/return')
async def returnToBase():
    if robot.status == 'charge':
        if robot.isAvailable == True:
            asyncio.create_task(goReturn())
            return {'message': 'True'}
        logger.error('Robot in Use ERROR!!')
    else:
        logger.error('Status ERROR!!')
    return {'message': 'False'}


@app.get('/info/currentXY')  # deprecated
async def returnXY(request: Request):
    '''
    def newMessage():
        try:
            ret = amr.currentXY()
            x = ret['x']
            y = ret['y']
            res=False
            if newMessage.lastX != x:
                res= True
            elif newMessage.lastY != y:
                res =  True

            newMessage.lastX = x
            newMessage.lastY = y

            return res

        except AttributeError:
            newMessage.lastX = 0
            newMessage.lastY = 0
    '''

    async def eventGenerator():
        while True:
            if await request.is_disconnected():
                break  # stop streaming when disconnected

            ret = amr.currentXY()

            yield {
                "event": "new_message",  # idk how to set this
                "id": "message_id",
                "retry": 15000,
                "data": {
                }
            }

            await asyncio.sleep(2)  # stream delay
    return EventSourceResponse(eventGenerator())


@app.get('/info/status')
async def returnStatus():
    data = {
        'position': amr.currentXY(),
        'robotStatus': jsons.dump(robot),
        'amrStatus': amr.currentStatus(),
        'batteryStatus': amr.battery(),
    }

    return data


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

    try:
        amr.annulment()
        amr.stopMagnetic()
    except amr.ConnectionError:
        logger.error('AMR Connection ERROR')

    # try:
    #     c = arm.openClient()
    #     asyncio.run(arm.setPose(client=c, pose='default'))

    # except arm.ConnectionERROR:
    #     logger.error('Robot Arm Connection ERROR')

    uvicorn.run(app, host='0.0.0.0', port=8000)
