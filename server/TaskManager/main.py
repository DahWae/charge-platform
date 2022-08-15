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
# conn.execute('''CREATE TABLE vehicle (ts, plate, parkID, power, pickTime, done)''')

robotUrl = 'http://192.168.100.2'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)


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
    form.Time = datetime.time()
    now = datetime.datetime.now()
    form.ts = datetime.datetime.timestamp(now)
    cur.execute('INSERT INTO vehicle VALUES(?,?,?,?,?)', (form.ts,
                form.Plate, form.ParkID, form.Power/10, form.PickTime, False))
    conn.commit()

    path = robotUrl + ':8000/action/charge'
    json = {
        'space': form.ParkID,
        'leaveTime': form.PickTime,
        'tStamp': form.ts,
        'power': form.Power,
        }

    return


@app.get('/')
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8001)
