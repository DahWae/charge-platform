import datetime
import jsons
import sys
import asyncio
import sqlite3 as sl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from sse_starlette.sse import EventSourceResponse
from loguru import logger
import requests
from requests.exceptions import Timeout
from types import SimpleNamespace
from munch import DefaultMunch


class SubmittForm(BaseModel):
    ts: float = None
    Plate: str
    ParkID: str
    Power: float
    PickTime: str
    Time: datetime.time = None


# TODO: change to list of robots' URL if multiple robots
# robotUrl = 'http://192.168.100.3'
robotUrl = 'http://localhost'

logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")

conn = sl.connect('test.db')
cur = conn.cursor()
conn.execute('''DROP TABLE if exists Vehicle ''')
conn.execute(
    '''CREATE TABLE if not exists Vehicle (ts, plate, parkID, power, pickTime, percentage, status)''')
conn.execute('''DROP TABLE if exists Robot ''')
conn.execute(
    '''CREATE TABLE if not exists Robot (x, y, robotTarget, robotStatus, amrStatus, amrBattery, amrTemp)''')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)


async def mainTask():

    msg = getRobotStatus()
    bot = DefaultMunch.fromDict(msg)
    cur.execute('''INSERT INTO Robot VALUES(?,?,?,?,?,?,?)''', (bot.position.x, bot.position.y, bot.robotStatus.target,
                                                                bot.robotStatus.status, bot.amrStatus, bot.batteryStatus.power, bot.batteryStatus.temp))
    conn.commit()

    while True:

        msg = getRobotStatus()
        bot = DefaultMunch.fromDict(msg)
        cur.execute('''UPDATE Robot SET x = ?,
                                        y = ?,
                                        robotTarget = ?,
                                        robotStatus = ?,
                                        amrStatus = ?,
                                        amrBattery = ?,
                                        amrTemp = ?''',
                    (bot.position.x, bot.position.y, bot.robotStatus.target,
                     bot.robotStatus.status, bot.amrStatus, bot.batteryStatus.power, bot.batteryStatus.temp))
        conn.commit()

        cur.execute('''SELECT * from Vehicle''')
        records = cur.fetchall()
        for row in records:
            if row[5] == 'waiting':  # ts, plate, parkID, power, pickTime, status
                logger.info('found task waiting')
                if bot.robotStatus.status == 'idle':
                    setRobotCharge(row[2])
                    cur.execute('''UPDATE Vehicle SET status = ?
                    WHERE ts = ?''', ('charging', row[0]))

        await asyncio.sleep(2)  # check every 10 sec


def getRobotStatus():
    path = robotUrl + ':8000/info/status'
    try:
        r = requests.get(url=path, timeout=10)
        return r.json()
    except Timeout:
        raise ConnectionError


def setRobotCharge(parkID: str):
    path = robotUrl + ':8000/action/charge'
    json = {
        'space': parkID,
    }
    try:
        r = requests.post(url=path, json=json, timeout=10)
    except Timeout:
        raise ConnectionError

    return


def setRobotReturn():
    path = robotUrl + ':8000/action/return'
    try:
        r = requests.post(url=path, timeout=10)
    except Timeout:
        raise ConnectionError

    return


@app.get('/stream')
async def taskManager(request: Request):
    def newMessage():  # check new value
        return True

    async def eventGenerator():
        num = 0
        while True:
            if await request.is_disconnected():
                break  # stop streaming when disconnected

            if newMessage():
                yield {
                    "event": "new_message",  # idk how to set this
                    "id": "message_id",
                    "retry": 15000,
                    "data": {
                        "data1": num,
                        "data2": "Hello"
                    }
                }
                logger.info(num)

            num += 1
            await asyncio.sleep(2)  # stream delay
    return EventSourceResponse(eventGenerator())


@app.get('/robot')
async def returnRobot(request: Request):
    async def eventGenerator():
        while True:
            if await request.is_disconnected():
                break  # stop streaming when disconnected

            cur.execute('''SELECT * from Robot''')
            msg = cur.fetchall()  # x, y, robotTarget, robotStatus, amrStatus, amrBattery, amrTemp

            allRobots = []
            for robots in msg:
                temp = [{
                    'position': {
                        'x': robots[0],
                        'y': robots[1]
                    },
                    'robot': {
                        'robotTarget': robots[2],
                        'robotStatus': robots[3],
                        'amrStatus': robots[4],
                        'amrBattery': robots[5],
                        'amrTemp': robots[6]
                    }
                }]
                allRobots.append(temp)

            yield {
                "event": "new_message",  # idk how to set this
                "id": "message_id",
                "retry": 15000,
                "data": jsons.dump(allRobots)
            }

            await asyncio.sleep(2)  # stream delay
    return EventSourceResponse(eventGenerator())


@app.get('/vehicle')
async def returnRobot(request: Request):
    async def eventGenerator():
        while True:
            if await request.is_disconnected():
                break  # stop streaming when disconnected

            cur.execute('''SELECT * from Vehicle''')
            msg = cur.fetchall()  # ts, plate, parkID, power, pickTime, percentage, status

            allTasks = []
            for task in msg:
                temp = [{
                    'ts': task[0],
                    'plate': task[1],
                    'parkID': task[2],
                    'power': task[3],
                    'pickTime': task[4],
                    'percentage': task[5],
                    'status': task[6],
                }]
                allTasks.append(temp)
            yield {
                "event": "new_message",  # idk how to set this
                "id": "message_id",
                "retry": 15000,
                "data": jsons.dump(allTasks)
            }

            await asyncio.sleep(2)  # stream delay
    return EventSourceResponse(eventGenerator())


@app.post('/submit')
async def submit(form: SubmittForm):
    logger.info('recieved submission')
    form.Power /= 10
    form.ts = datetime.datetime.now().strftime("%H:%M:%S")
    # print(form)

    cur.execute('INSERT INTO Vehicle VALUES(?,?,?,?,?,?,?)', (form.ts,
                form.Plate, form.ParkID, form.Power, form.PickTime, 0, 'waiting'))
    conn.commit()

    return


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.on_event('startup')
async def startupEvent():
    asyncio.create_task(mainTask())

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8001)
