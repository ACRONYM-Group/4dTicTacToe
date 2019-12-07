import asyncio
import websockets

numDimensions = 3
width = 3

def createDimension(itNum=0):
    dimension = {}
    i = 0
    if itNum == 0:
        while i < width:
            dimension[len(dimension)] = i
            i += 1

    while itNum < numDimensions-1:
        outerArray = {}
        i = 0
        emptyState = False
        while i < numDimensions:
            dimension = {}
            k = 0
            emptyState = not emptyState
            while k < width:
                dimension[len(dimension)] = int(not emptyState)
                k += 1
            outerArray[len(outerArray)] = dimension
            i += 1

        dimension = outerArray
        itNum += 1

    return dimension

boardState = createDimension()

print(boardState)

def getCell(coords):
    return boardState[coords[1]][coords[2]][coords[3]][coords[4]]

def setCell(coords, val, i=0):
    #[0, 1, 1]
    subArrayString = "boardState"
    while i < len(coords):
        subArrayString += "[" + str(coords[i]) + "]"
        i += 1

    exec(str(subArrayString) + " = val")



async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)
        print(message)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8000))
asyncio.get_event_loop().run_forever()




