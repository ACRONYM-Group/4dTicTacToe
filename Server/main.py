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

def checkVictory():
    bx = 0
    while bx < width:
        by = 0
        while by < width:
            sx = 0
            while sx < width:
                sy = 0
                while sy < width:
                    hasWrittenAnything = False
                    returnData = checkIfInCenterOfLine(bx, by, sx, sy, hasWrittenAnything)
                    foundWinCondition = returnData[0]
                    winner = returnData[1]
                    sy += 1
                sx += 1

            by += 1
        bx += 1 
    
    return [foundWinCondition, winner]

hasWrittenAnything = False
def checkIfInCenterOfLine(bx, by, sx, sy, hasWrittenAnything):
    foundWinCondition = False
    adjacentCells = []
    focusbx = -1
    while focusbx > -2 and focusbx < 2:
        focusby = -1
        while focusby > -2 and focusby < 2:
            focussx = -1
            while focussx > -2 and focussx < 2:
                focussy = -1
                while focussy > -2 and focussy < 2:
                    if (bx+focusbx > -1 and bx+focusbx < width and by+focusby > -1 and by+focusby < width and sx+focussx > -1 and sx+focussx < width and sy+focussy > -1 and sy+focussy < width and (abs(focusbx) + abs(focusby) + abs(focussx) + abs(focussy) != 0)):
                        if (boardState[bx+focusbx][by+focusby][sx+focussx][sy+focussy] == boardState[bx][by][sx][sy]):
                            adjacentCells.append([focusbx, focusby, focussx, focussy, boardState[bx+focusbx][by+focusby][sx+focussx][sy+focussy]])
                    focussy += 1

                focussx += 1
            focusby +=1
        focusbx += 1
    
    
    hasWrittenAnything = False
    for i in adjacentCells:
        for k in adjacentCells:
            if i[0] == -k[0] and i[1] == -k[1] and i[2] == -k[2] and i[3] == -k[3] and i[4] != 0 and i[4] != 1:
                foundWinCondition = True
                print(i)
                winner = i[4]
                return [foundWinCondition, winner]
                hasWrittenAnything = True
    if (hasWrittenAnything):
        print("----")

    return [False, 0]

async def commandHandler(msg, websocket):
    print(msg["cmdtype"])

    if msg["cmdtype"] == "login":
        print("Player is loging in.")
        await websocket.send(json.dumps({"cmdtype":"loginResponse", "team":"X", "turn":"X"}))

    if msg["cmdtype"] == "setCell":
        setCell(msg["coords"], msg["val"])
        victory = checkVictory()
        if victory[0]:
            print(str(victory[1]) + " HAS WON THE MATCH!")

    if (msg["cmdtype"] == "getCell"):
        await websocket.send(json.dumps({"cmdtype":"getCellResponse", "coords":msg["coords"], "val":getCell(msg["coords"])}))



async def echo(websocket, path):
    async for message in websocket:
        print(message)
        await commandHandler(json.loads(message), websocket)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8000))
asyncio.get_event_loop().run_forever()





