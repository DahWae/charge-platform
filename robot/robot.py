# system package
import asyncio
import datetime
from pydantic import BaseModel
import json

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
    target: Target() = None
    status: str = 'idle'
    startFlag: bool = False


def contains(list, filter):
    for x in list:
        if filter(x):
            return x
    return None


def newRobot():
    return RobotStatus()


async def pose(client, pose):
    match pose:
        case 'default':
            arm.postState(client=client, state=1)
            await asyncio.sleep(0.5)    
            print(arm.getReturn(client=client))
            while(arm.getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                arm.postState(client=client, state=0)
                print('waiting')

        case 'ready':
            arm.postState(client=client, state=2)
            await asyncio.sleep(0.5)    
            print(arm.getReturn(client=client))
            while(arm.getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                arm.postState(client=client, state=0)
                print('waiting')

        case 'aim':
            arm.postState(client=client, state=3)
            await asyncio.sleep(0.5)    
            print(arm.getReturn(client=client))
            while(arm.getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                arm.postState(client=client, state=0)
                print('waiting')

        case 'plug':
            arm.postState(client=client, state=4)
            await asyncio.sleep(0.5)    
            print(arm.getReturn(client=client))
            while(arm.getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                arm.postState(client=client, state=0)
                print('waiting')

        case 'charge':
            arm.postState(client=client, state=5)
            await asyncio.sleep(0.5)    
            print(arm.getReturn(client=client))
            while(arm.getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                arm.postState(client=client, state=0)
                print('waiting')

    return

async def goCharge(robotStatus: RobotStatus, target: Target):
    if robotStatus.status == 'idle':
        if robotStatus.startFlag == False:
            robotStatus.status = 'charge'
            robotStatus.target = target
            robotStatus.startFlag = True
    else:
        return False

    # AMR
    allPoint = amr.currentAllGoalPoint()
    # print('all point loaded')
    # match target.space and GoalPoint coordination
    matchedPoint = contains(allPoint, lambda x: x['name'] == target.space)
    if matchedPoint is None:
        print('ERR, Point not found')
        return False
    # print('point found, moving')
    print(matchedPoint)
    print(amr.moveToGoal(matchedPoint))
    await asyncio.sleep(1)
    while(amr.currentStatus() == 'running'):
        # print('still moving')
        await asyncio.sleep(2)
    # print('start magnetic find')
    print(amr.startMagneticFind())
    await asyncio.sleep(1)
    while(amr.magneticState() == 1):
        # print('still finding')
        await asyncio.sleep(2)
    # print('start magnetic goal')
    print(amr.startMagneticGoal())
    await asyncio.sleep(1)
    while(amr.magneticState() == 1):
        # print('still tracing')
        await asyncio.sleep(2)
    # print('end of moving')

    # ARM
    # arm.postCoord(client=c, coords=coords)
    # arm.postState(client=c, state=1)
    # while(~arm.getReturn(client=c)):
    #     None
    # arm.postState(client=c, state=2)

    robotStatus.startFlag = False
    return True


async def goReturn(robotStatus: RobotStatus):
    if robotStatus.status == 'charge':
        if robotStatus.startFlag == False:
            robotStatus.status = 'return'
            robotStatus.target = None
            robotStatus.startFlag = True
    else:
        return False

    # ARM

    # AMR
    allPoint = amr.currentAllGoalPoint()
    # match target to Base
    matchedPoint = contains(allPoint, lambda x: x['name'] == 'P0')
    amr.moveToGoal(matchedPoint)
    await asyncio.sleep(1)
    while(amr.currentStatus() == 'running'):
        # print('still moving')
        await asyncio.sleep(2)
    # while(amr.currentStatus()):
    #     await asyncio.sleep(2)
    # amr.startMagneticFind()
    # while(amr.magneticState()):
    #     await asyncio.sleep(2)
    # amr.startMagneticGoal()
    # while(amr.magneticState()):
    #     await asyncio.sleep(2)

    robotStatus.status = 'idle'
    robotStatus.startFlag = False
    return True


async def getRobotStatus(robotStatus):
    amrStatus = amr.currentStatus()
    ret = []
    ret.append(amrStatus)
    ret.append(robotStatus)
    ret = json.dumps(ret.__dict__)
    return ret
