import asyncio
from pyModbusTCP.client import ModbusClient

class InputERROR(Exception):
    # raise when function got wrong value
    pass

class ConnectionERROR(Exception):
    # raise when lost connection
    pass


def openClient():
    try:
        c = ModbusClient(host='192.168.100.4', port=502, unit_id=1,
                        auto_open=True, timeout=10)  # 192.168.1.116為UR的IP位置
        # c = ModbusClient(host='192.168.0.28', port=502,unit_id=1,auto_open=True)    #192.168.1.116為UR的IP位置

    except TimeoutError:
        raise ConnectionERROR
    return c


def postCoord(client, coords):
    client.write_single_register(129, int(coords[0]+1000))
    client.write_single_register(130, int(-coords[1]+1000))
    client.write_single_register(131, int(-coords[2]+1000))
    client.write_single_register(132, int((coords[3]+360)*100))
    client.write_single_register(133, int((-coords[4]+360)*100))
    client.write_single_register(134, int((-coords[5]+360)*100))
    return


def postState(client, state):
    client.write_single_register(135, state)
    return


def getCoord(client):
    coord = (client.read_holding_registers(400, 6))
    # print(coord)
    for j, e in enumerate(coord):
        if e > 32767:
            coord[j] = e-65535

    for j, e in enumerate(coord):
        if j < 3:
            coord[j] = e/10
        else:
            coord[j] = e/1000
    return coord


def getReturn(client):
    return client.read_holding_registers(147, 1)[0]


async def setPose(client, pose, coord=None):
    match pose:
        case 'default':
            postState(client=client, state=1)
            await asyncio.sleep(3)    
            # print(getReturn(client=client))
            while(getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                # print('waiting')
            postState(client=client, state=0)
            await asyncio.sleep(2)

        case 'prep':
            postState(client=client, state=2)
            print('state posted')
            await asyncio.sleep(3)    
            # print(getReturn(client=client))
            while(getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                # print('waiting')
            postState(client=client, state=0)
            await asyncio.sleep(2)

        case 'aim':
            postCoord(client=client, coords=coord)
            postState(client=client, state=3)
            await asyncio.sleep(3)    
            # print(getReturn(client=client))
            while(getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                # print('waiting')
            postState(client=client, state=0)
            await asyncio.sleep(2)

        case 'ready':
            postState(client=client, state=4)
            await asyncio.sleep(3)    
            # print(getReturn(client=client))
            while(getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                # print('waiting')
            postState(client=client, state=0)
            await asyncio.sleep(2)

        case 'plug':
            postState(client=client, state=5)
            await asyncio.sleep(3)    
            # print(getReturn(client=client))
            while(getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                # print('waiting')
            postState(client=client, state=0)
            await asyncio.sleep(2)

        case 'unplug':
            postState(client=client, state=6)
            await asyncio.sleep(3)    
            # print(getReturn(client=client))
            while(getReturn(client=client) == 1):
                await asyncio.sleep(0.5)
                # print('waiting')
            postState(client=client, state=0)
            await asyncio.sleep(2)

        case _:
            raise InputERROR

    return