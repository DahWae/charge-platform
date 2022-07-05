# This program is the controller of AMR
# using HTTP request

import requests

url = 'http://10.42.0.1'  # TODO: change the url


def mapMode(mode):
    path = url + ':6010/map/mapMode'
    params = {'MODE': mode}
    r = requests.post(url=path, params=params)
    return r


def saveMap(name):
    path = url + ':6010/map/saveMap'
    params = {'name': name}
    r = requests.post(url=path, params=params)
    return r


def deleteMap(name):
    path = url + ':6010/map/deleteMap'
    json = {'name': name}
    r = requests.post(url=path, json=json)
    return r


def switchMap(name):
    path = url + ':6010/map/switchMap'
    json = {'name': name}
    r = requests.post(url=path, json=params)
    return r.json()


def currentMap():
    path = url + ':6010/map/currentMap'
    r = requests.get(url=path)
    return r.text


def renameMap(name, newName):
    path = url + ':6010/map/renameMap'
    params = {'name': name, 'newName': newName}
    r = requests.post(url=path, params=params)
    return r


def getAllMap():
    path = url + ':6010/map/getAllMap'
    r = requests.get(url=path)
    return r.json()


def newGoalPoint(name):
    path = url + ':6010/navigation/newGoalPoint'
    params = {'name': name}
    r = requests.post(url=path, params=params)
    return r


def deleteGoalPoint(mapName, pointName):
    path = url + ':6010/navigation/deleteGoalPoint'
    params = {'mapName': mapName, 'pointName': pointName}
    r = requests.post(url=path, params=params)
    return r


def updateGoalPoint(mapName, pointName, newPointName):
    path = url + ':6010/navigation/updateGoalPoint'
    params = {'mapName': mapName, 'pointName': pointName,
            'newPointName': newPointName}
    r = requests.post(url=path, params=params)
    return r.text


def currentAllGoalPoint():
    path = url + ':6010/navigation/currentAllGoalPoint'
    r = requests.get(url=path)
    return r.json()


def allGoalPoint(name):
    path = url + ':6010/navigation/allGoalPoint'
    json = {'name': name}
    r = requests.post(url=path, json=json)
    return r.json()


def currentXY():
    path = url + ':6010/navigation/currentXY'
    r = requests.get(url=path)
    return r.json()


def moveToGoal(point):
    path = url + ':6010/amrCommand/moveToGaol' # typo
    json = {'x': point['x'], 'y': point['y'], 'qz': point['qz'], 'qw': point['qw']}
    r = requests.post(url=path, json=json)
    return r.text


def annulment():
    path = url + ':6010/amrCommand/annulment'
    r = requests.post(url=path)
    return r


def currentStatus():
    path = url + ':6010/amrCommand/currentStatus'
    r = requests.get(url=path)
    ret = r.json()
    return ret['taskState']


def battery():
    path = url + ':6010/amrHardware/batter'
    r = requests.get(url=path)
    return r


def velocity(name):
    path = url + ':6010/amrHardware/velocity'
    params = {'name': name}
    r = requests.post(url=path, params=params)
    return r


def sensor():
    path = url + ':6010/amrHardware/sensor'
    r = requests.get(url=path)
    return r


def light(name, flag):
    path = url + ':6010/amrHardware/velocity'
    params = {'name': name, 'flag': flag}
    r = requests.post(url=path, params=params)
    return r


def startMagneticFind():
    path = url + ':6010/amrHardware/startMagneticFind'
    r = requests.get(url=path)
    return r.text


def startMagneticGoal(name):
    path = url + ':6010/amrHardware/startMagneticGoal'
    json = {'name': name}
    r = requests.post(url=path, json=json)
    return r.text


def stopMagnetic():
    path = url + ':6010/amrHardware/stopMagnetic'
    r = requests.get(url=path)
    return r


def magneticState():
    path = url + ':6010/amrHardware/magneticState'
    r = requests.get(url=path)
    return r.json()
