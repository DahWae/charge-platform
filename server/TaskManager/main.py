import datetime
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


class SubmittForm(BaseModel):
    ts: float = None
    Plate: str
    ParkID: str
    Power: float
    PickTime: str
    Time: datetime.time = None


logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")

conn = sl.connect('test.db')
cur = conn.cursor()
conn.execute('''DROP TABLE if exists Vehicle ''')
conn.execute('''CREATE TABLE if not exists Vehicle (ts, plate, parkID, power, pickTime, status)''')

robotUrl = 'http://192.168.100.2' # TODO: change to list of robots' URL if multiple robots

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)


async def mainTask():
    while True:
        cur.execute('''SELECT * from Vehicle''')
        records = cur.fetchall()
        for row in records:
            print(row)
            if row[5] == 'waiting': # ts, plate, parkID, power, pickTime, status
                logger.info('found task waiting')
                # if getRobotStatus()['robotStatus']['status'] == 'idle':
                #     setRobotCharge(row[2])

        await asyncio.sleep(10) # check every 10 sec

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
                    "event": "new_message",
                    "id": "message_id",
                    "retry": 15000,
                    "data": {
                        'data1': num,
                        'data2': 'Hello'
                    }
                }
                logger.info(num)

            num += 1
            await asyncio.sleep(1)  # stream delay
    return EventSourceResponse(eventGenerator())


@app.post('/submit')
async def submit(form: SubmittForm):
    logger.info('recieved submission')
    form.Time = datetime.time()
    now = datetime.datetime.now()
    form.Power /= 10
    form.ts = datetime.datetime.timestamp(now)
    print(form)

    cur.execute('INSERT INTO Vehicle VALUES(?,?,?,?,?,?)', (form.ts,
                form.Plate, form.ParkID, form.Power, form.PickTime, 'waiting'))
    conn.commit()

    # path = robotUrl + ':8000/action/charge'
    # json = {
    #     'space': form.ParkID,
    #     'leaveTime': form.PickTime,
    #     'tStamp': form.ts,
    #     'power': form.Power,
    #     }

    # try:
    #     r = requests.post(url=path, json=json, timeout=10)
    # except Timeout:
    #     raise ConnectionError

    return


@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.on_event('startup')
async def startupEvent():
    asyncio.create_task(mainTask())

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8001)
