import amr
import asyncio


def contains(list, filter):
    for x in list:
        if filter(x):
            return x
    return None

async def test():
    amr.annulment()
    amr.stopMagnetic()

    allPoint = amr.currentAllGoalPoint()
    # match target to Base
    matchedPoint = contains(allPoint, lambda x: x['name'] == 'Base')
    print(matchedPoint)
    if matchedPoint is None:
        print('ERR, Point not found')
        exit()
    amr.moveToGoal(matchedPoint)

    await asyncio.sleep(1)
    while(amr.currentStatus() == 'running'):
        await asyncio.sleep(2)

    amr.annulment()
    amr.stopMagnetic()

if __name__ == '__main__':
    asyncio.run(test())