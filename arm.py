from numpy import empty
from pyModbusTCP.client import ModbusClient


def openClient(host, port):
    c = ModbusClient(host=host,port=port,unit_id=1,auto_open=True)    #192.168.1.116為UR的IP位置
    return c

def postCoord(client, x, y, z, rx, ry, rz):
    client.write_single_register(129, int(x+1000))
    client.write_single_register(130, int(y+1000))
    client.write_single_register(131, int(z+1000))
    client.write_single_register(132, int((rx+360)*100))
    client.write_single_register(133, int((ry+360)*100))
    client.write_single_register(134, int((rz+360)*100))
    return

def postState(client, state):
    client.write_single_register(135, state)
    return

def getCoord(client):
    in_regs=[]
    in_regs.append(client.read_holding_registers(141, 6))
    return in_regs

def getReturn(client):
    return client.read_holding_registers(141,1)[0]
