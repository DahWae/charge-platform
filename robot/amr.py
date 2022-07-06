# This program is the controller of AMR
# using HTTP request

import requests
from requests.exceptions import Timeout

url = 'http://10.42.0.1'  # TODO: change the url


def mapMode(mode):
    path = url + ':6010/map/mapMode'
    params = {'MODE': mode}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def saveMap(name):
    path = url + ':6010/map/saveMap'
    params = {'name': name}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def deleteMap(name):
    path = url + ':6010/map/deleteMap'
    json = {'name': name}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def switchMap(name):
    path = url + ':6010/map/switchMap'
    json = {'name': name}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.json()
    except Timeout:
        return 'ERROR: Timeout'


def currentMap():
    path = url + ':6010/map/currentMap'
    try:
        r = requests.get(url=path, timeout=10)
        return r.text
    except Timeout:
        return 'ERROR: Timeout'


def renameMap(name, newName):
    path = url + ':6010/map/renameMap'
    params = {'name': name, 'newName': newName}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def getAllMap():
    path = url + ':6010/map/getAllMap'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        return 'ERROR: Timeout'


def newGoalPoint(name):
    path = url + ':6010/navigation/newGoalPoint'
    params = {'name': name}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def deleteGoalPoint(mapName, pointName):
    path = url + ':6010/navigation/deleteGoalPoint'
    params = {'mapName': mapName, 'pointName': pointName}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def updateGoalPoint(mapName, pointName, newPointName):
    path = url + ':6010/navigation/updateGoalPoint'
    params = {'mapName': mapName, 'pointName': pointName,
            'newPointName': newPointName}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r.text
    except Timeout:
        return 'ERROR: Timeout'


def currentAllGoalPoint():
    path = url + ':6010/navigation/currentAllGoalPoint'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        return 'ERROR: Timeout'


def allGoalPoint(name):
    path = url + ':6010/navigation/allGoalPoint'
    json = {'name': name}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.json()
    except Timeout:
        return 'ERROR: Timeout'


def currentXY():
    path = url + ':6010/navigation/currentXY'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        return 'ERROR: Timeout'


def moveToGoal(point):
    path = url + ':6010/amrCommand/moveToGaol' # typo
    json = {'x': point['x'], 'y': point['y'], 'qz': point['qz'], 'qw': point['qw']}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.text
    except Timeout:
        return 'ERROR: Timeout'


def annulment():
    path = url + ':6010/amrCommand/annulment'
    try:
        r = requests.post(url=path, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def currentStatus():
    path = url + ':6010/amrCommand/currentStatus'
    try:
        r = requests.get(url=path, timeout=10)
        ret = r.json()
        return ret['taskState']
    except Timeout:
        return 'ERROR: Timeout'


def battery():
    path = url + ':6010/amrHardware/batter'
    try:
        r = requests.get(url=path, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def velocity(name):
    path = url + ':6010/amrHardware/velocity'
    params = {'name': name}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def sensor():
    path = url + ':6010/amrHardware/sensor'
    try:
        r = requests.get(url=path, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def light(name, flag):
    path = url + ':6010/amrHardware/velocity'
    params = {'name': name, 'flag': flag}
    try:
        r = requests.post(url=path, params=params, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def startMagneticFind():
    path = url + ':6010/amrHardware/startMagneticFind'
    try:
        r = requests.get(url=path, timeout=10)
        return r.text
    except Timeout:
        return 'ERROR: Timeout'


def startMagneticGoal():
    path = url + ':6010/amrHardware/startMagneticGoal'
    json = {'name': '0'}
    try:
        r = requests.post(url=path, json=json, timeout=10)
        return r.text
    except Timeout:
        return 'ERROR: Timeout'


def stopMagnetic():
    path = url + ':6010/amrHardware/stopMagnetic'
    try:
        r = requests.get(url=path, timeout=10)
        return r
    except Timeout:
        return 'ERROR: Timeout'


def magneticState():
    path = url + ':6010/amrHardware/magneticState'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        return 'ERROR: Timeout'
