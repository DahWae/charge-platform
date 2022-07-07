# This program is the controller of AMR
# using HTTP request

import requests
from requests.exceptions import Timeout

url = 'http://10.42.0.1'  # TODO: change the url

class ConnectionError(Exception):
    # raise when connection timeout
    pass

def mapMode(mode):
    path = url + ':6010/map/mapMode'
    params = {'MODE': mode}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def saveMap(name):
    path = url + ':6010/map/saveMap'
    params = {'name': name}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def deleteMap(name):
    path = url + ':6010/map/deleteMap'
    json = {'name': name}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def switchMap(name):
    path = url + ':6010/map/switchMap'
    json = {'name': name}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.json()
    except Timeout:
        raise ConnectionError


def currentMap():
    path = url + ':6010/map/currentMap'
    try:
        r = requests.get(url=path, timeout=10)
        return r.text
    except Timeout:
        raise ConnectionError


def renameMap(name, newName):
    path = url + ':6010/map/renameMap'
    params = {'name': name, 'newName': newName}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def getAllMap():
    path = url + ':6010/map/getAllMap'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        raise ConnectionError


def newGoalPoint(name):
    path = url + ':6010/navigation/newGoalPoint'
    params = {'name': name}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def deleteGoalPoint(mapName, pointName):
    path = url + ':6010/navigation/deleteGoalPoint'
    params = {'mapName': mapName, 'pointName': pointName}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def updateGoalPoint(mapName, pointName, newPointName):
    path = url + ':6010/navigation/updateGoalPoint'
    params = {'mapName': mapName, 'pointName': pointName,
            'newPointName': newPointName}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r.text
    except Timeout:
        raise ConnectionError


def currentAllGoalPoint():
    path = url + ':6010/navigation/currentAllGoalPoint'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        raise ConnectionError


def allGoalPoint(name):
    path = url + ':6010/navigation/allGoalPoint'
    json = {'name': name}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.json()
    except Timeout:
        raise ConnectionError


def currentXY():
    path = url + ':6010/navigation/currentXY'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        raise ConnectionError


def moveToGoal(point):
    path = url + ':6010/amrCommand/moveToGaol' # typo
    json = {'x': point['x'], 'y': point['y'], 'qz': point['qz'], 'qw': point['qw']}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.text
    except Timeout:
        raise ConnectionError


def annulment():
    path = url + ':6010/amrCommand/annulment'
    try:
        r = requests.post(url=path, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def currentStatus():
    path = url + ':6010/amrCommand/currentStatus'
    try:
        r = requests.get(url=path, timeout=10)
        ret = r.json()
        return ret['taskState']
    except Timeout:
        raise ConnectionError


def battery():
    path = url + ':6010/amrHardware/batter'
    try:
        r = requests.get(url=path, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def velocity(name):
    path = url + ':6010/amrHardware/velocity'
    params = {'name': name}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def sensor():
    path = url + ':6010/amrHardware/sensor'
    try:
        r = requests.get(url=path, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def light(name, flag):
    path = url + ':6010/amrHardware/velocity'
    params = {'name': name, 'flag': flag}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def startMagneticFind():
    path = url + ':6010/amrHardware/startMagneticFind'
    try:
        r = requests.get(url=path, timeout=10)
        return r.text
    except Timeout:
        raise ConnectionError


def startMagneticGoal():
    path = url + ':6010/amrHardware/startMagneticGoal'
    json = {'name': '0'}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.text
    except Timeout:
        raise ConnectionError


def stopMagnetic():
    path = url + ':6010/amrHardware/stopMagnetic'
    try:
        r = requests.get(url=path, timeout=10)
        return r
    except Timeout:
        raise ConnectionError


def magneticState():
    path = url + ':6010/amrHardware/magneticState'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        raise ConnectionError
