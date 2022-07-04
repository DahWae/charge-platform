
import requests
import datetime

class Target:
    space: str
    leaveTime: datetime.datetime = None
    tStamp: int=None
    power: int=None

url = 'http://127.0.0.1'  # TODO: change the url

if __name__ == '__main__':
    path = url + ':8000/test'
    data = {'test': 'Dawae'}
    r = requests.post(url=path, params=data)
    print(r.json())