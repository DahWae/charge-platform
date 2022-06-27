# This program is the controller of AMR
# using HTTP request

from asyncio.windows_events import NULL
import requests

url = '192.168.1.1'  # TODO: change the url


def mapMode(mode):
    path = url + ':6010/map/mapMode'
    data = {'MODE': mode}
    r = requests.post(url=path, data=data)
    return r


def saveMap(name):
    path = url + ':6010/map/saveMap'
    data = {'name': name}
    r = requests.post(url=path, data=data)
    return r


def deleteMap(name):
    path = url + ':6010/map/deleteMap'
    data = {'name': name}
    r = requests.post(url=path, data=data)
    return r


def switchMap(name):
    path = url + ':6010/map/switchMap'
    data = {'name': name}
    r = requests.post(url=path, data=data)
    return r


def currentMap():
    path = url + ':6010/map/currentMap'
    r = requests.get(url=path)
    return r


def renameMap(name, newName):
    path = url + ':6010/map/renameMap'
    data = {'name': name, 'newName': newName}
    r = requests.post(url=path, data=data)
    return r


def getAllMap():
    path = url + ':6010/map/getAllMap'
    r = requests.get(url=path)
    return r


def newGoalPoint(name):
    path = url + ':6010/navigation/newGoalPoint'
    data = {'name': name}
    r = requests.post(url=path, data=data)
    return r


def deleteGoalPoint(mapName, pointName):
    path = url + ':6010/navigation/deleteGoalPoint'
    data = {'mapName': mapName, 'pointName': pointName}
    r = requests.post(url=path, data=data)
    return r


def updateGoalPoint(mapName, pointName, newPointName):
    path = url + ':6010/navigation/updateGoalPoint'
    data = {'mapName': mapName, 'pointName': pointName,
            'newPointName': newPointName}
    r = requests.post(url=path, data=data)
    return r


def currentAllGoalPoint():
    path = url + ':6010/navigation/currentAllGoalPoint'
    r = requests.get(url=path)
    return r


def allGoalPoint(name):
    path = url + ':6010/navigation/allGoalPoint'
    data = {'name': name}
    r = requests.post(url=path, data=data)
    return r


def currentXY():
    path = url + ':6010/navigation/currentXY'
    r = requests.post(url=path)
    return r


def moveToGoal(x, y, qz, qw):
    path = url + ':6010/amrCommand/moveToGoal'
    data = {'x': x, 'y': y, 'qz': qz, 'qw': qw}
    r = requests.post(url=path, data=data)
    return r


def annulment():
    path = url + ':6010/amrCommand/annulment'
    r = requests.post(url=path)
    return r


def currentStatus():
    path = url + ':6010/amrCommand/currentStatus'
    r = requests.get(url=path)
    return r


def battery():
    path = url + ':6010/amrHardware/batter'
    r = requests.get(url=path)
    return r


def velocity(name):
    path = url + ':6010/amrHardware/velocity'
    data = {'name': name}
    r = requests.post(url=path, data=data)
    return r


def sensor():
    path = url + ':6010/amrHardware/sensor'
    r = requests.get(url=path)
    return r


def light(name, flag):
    path = url + ':6010/amrHardware/velocity'
    data = {'name': name, 'flag': flag}
    r = requests.post(url=path, data=data)
    return r


def startMagneticFind(name):
    path = url + ':6010/amrHardware/startMagneticFind'
    data = {'name': name}
    r = requests.post(url=path, data=data)
    return r


def startMagneticGoal():
    path = url + ':6010/amrHardware/startMagneticGoal'
    r = requests.get(url=path)
    return r


def stopMagnetic():
    path = url + ':6010/amrHardware/stopMagnetic'
    r = requests.get(url=path)
    return r


def magneticState():
    path = url + ':6010/amrHardware/magneticState'
    r = requests.get(url=path)
    return r
