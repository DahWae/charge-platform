import arm


if __name__ == '__main__':
    c = arm.openClient(host='192.168.0.29', port=502)
    coords=[0,0,0,0,0,0]
    arm.postCoord(client=c, coords=coords)
    arm.postState(client=c, state=0)