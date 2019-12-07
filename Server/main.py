import asyncio
import websockets
import ssl
import pathlib
import json

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
                dimension[len(dimension)] = {0:{0:int(not emptyState), 1:int(not emptyState), 2:int(not emptyState)}, 1:{0:int(not emptyState), 1:int(not emptyState), 2:int(not emptyState)}, 2:{0:int(not emptyState), 1:int(not emptyState), 2:int(not emptyState)}}
                k += 1
            outerArray[len(outerArray)] = dimension
            i += 1

        dimension = outerArray
        itNum += 1

    return dimension

boardState = createDimension()

print(boardState)

def getCell(coords):
    return boardState[coords[0]][coords[1]][coords[2]][coords[3]]

def setCell(coords, val, i=0):
    #[0, 1, 1]
    subArrayString = "boardState"
    while i < len(coords):
        subArrayString += "[" + str(coords[i]) + "]"
        i += 1

    exec(str(subArrayString) + " = val")

async def commandHandler(msg, websocket):
    print(msg["cmdtype"])

    if msg["cmdtype"] == "login":
        print("Player is loging in.")
        await websocket.send(json.dumps({"cmdtype":"loginResponse", "team":"X", "turn":"X"}))

    if msg["cmdtype"] == "setCell":
        print(msg["coords"])
        setCell(msg["coords"], msg["val"])

    if (msg["cmdtype"] == "getCell"):
        await websocket.send(json.dumps({"cmdtype":"getCellResponse", "coords":msg["coords"], "val":getCell(msg["coords"])}))



async def echo(websocket, path):
    async for message in websocket:
        print(message)
        await commandHandler(json.loads(message), websocket)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8000))
asyncio.get_event_loop().run_forever()





