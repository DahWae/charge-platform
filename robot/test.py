
import time
import requests
import datetime

import amr


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
    params = None
    r = requests.post(url=path, params=params)
    print(r.text)
    return


def amrTest():
    allPoint = amr.currentAllGoalPoint()
    print('all point loaded')
    # match target.space and GoalPoint coordination
    matchedPoint = contains(allPoint, lambda x: x['name'] == 'P1')
    if matchedPoint is None:
        print('ERR, Point not found')
        return
    print('point found, moving')
    print(matchedPoint)
    print(amr.moveToGoal(matchedPoint))
    print('end of moving')
    print(amr.currentXY())
    while True:
        print(amr.currentStatus())
        time.sleep(2)

    # print(amr.getAllMap())
    # mapName = amr.currentMap()
    # print(mapName)
    # print(amr.allGoalPoint(name=mapName))
    # print(amr.currentAllGoalPoint())


    # print(amr.startMagneticGoal(name='P2'))

    # mapName = amr.currentMap()
    # print(mapName)
    # print(amr.currentAllGoalPoint())
    # temp = amr.allGoalPoint(name='abc')
    # temp = amr.updateGoalPoint(mapName=mapName, pointName='P0', newPointName='Base')
    # temp = amr.moveToGoal()
    # print(temp)
    return


if __name__ == '__main__':
    chargeTest()
    # amrTest()
    # amr.annulment()
    # amr.stopMagnetic()

