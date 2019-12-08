import asyncio
import websockets
import ssl
import pathlib
import json
import random

numDimensions = 3
width = 3
winLocation = []
nextTeamToAssign = "X"
boards = []
boardsData = []

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

#boards.append(createDimension())
users = {}

def getCell(coords, boardID):
    return boards[boardID][coords[0]][coords[1]][coords[2]][coords[3]]

def setCell(coords, val, boardID):
    
    i = 0
    #[0, 1, 1]
    subArrayString = "boards[" + str(boardID) + "]"
    while i < len(coords):
        subArrayString += "[" + str(coords[i]) + "]"
        i += 1

    exec(str(subArrayString) + " = val")
    

def generateBoard():
    boards.append(createDimension())
    boardsData.append({"turn":"X"})
    print("BoardData " + str(boardsData))

def generateToken(nextTeamToAssign):
    token = random.randint(1,10000)
    if token in users:
        token = generateToken(nextTeamToAssign)

    if len(boards) == len(users)/2:
        nextAvaliableBoard = len(boards)
        generateBoard()
    else:
        nextAvaliableBoard = len(boards)-1

    users[token] = {"token":token, "team":nextTeamToAssign, "board":nextAvaliableBoard}
    if (nextTeamToAssign == "X"):
        nextTeamToAssign = "O"
    if (nextTeamToAssign == "O"):
        nextTeamToAssign = "X"
    return token
    

def checkVictory(boardID):
    foundWinCondition = False
    winner = 15
    bx = 0
    while bx < width:
        by = 0
        while by < width:
            sx = 0
            while sx < width:
                sy = 0
                while sy < width:
                    hasWrittenAnything = False
                    returnData = checkIfInCenterOfLine(bx, by, sx, sy, hasWrittenAnything, boardID)
                    if (returnData[0] == True):
                        foundWinCondition = returnData[0]
                        winner = returnData[1]
                    sy += 1
                sx += 1

            by += 1
        bx += 1 
    
    return [foundWinCondition, winner]

hasWrittenAnything = False
def checkIfInCenterOfLine(bx, by, sx, sy, hasWrittenAnything, boardID):
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
                        
                        if (boards[boardID][bx+focusbx][by+focusby][sx+focussx][sy+focussy] == boards[boardID][bx][by][sx][sy]):
                            #print("Adjacent Found " + str([bx+focusbx, by+focusby, sx+focussx, sy+focussy]))
                            testVar = [focusbx, focusby, focussx, focussy, boards[boardID][bx+focusbx][by+focusby][sx+focussx][sy+focussy], bx, by, sx, sy]
                            #print(testVar)
                            adjacentCells.append(testVar)
                    focussy += 1

                focussx += 1
            focusby +=1
        focusbx += 1


    
    
    hasWrittenAnything = False
    foundWinCondition = False
    winner = 0
    for i in adjacentCells:
        for k in adjacentCells:
            if i[0] == -k[0] and i[1] == -k[1] and i[2] == -k[2] and i[3] == -k[3] and i[4] == boards[boardID][i[5]][i[6]][i[7]][i[8]] and i[4] != 0 and i[4] != 1:
                print(i)
                foundWinCondition = True
                winner = i[4]
                hasWrittenAnything = True
                winLocation = [i[5], i[6], i[7], i[8]]
                print("WIN")
                print(str(winLocation) + " " + str(i))
    if (hasWrittenAnything):
        print("----")
    if (not foundWinCondition):
        return [False, 15]
    else:
        return [foundWinCondition, winner]

async def commandHandler(msg, websocket):

    if msg["cmdtype"] == "login":
        print("Player is loging in.")
        await websocket.send(json.dumps({"cmdtype":"loginResponse", "team":"X", "turn":"X", "token":generateToken(nextTeamToAssign)}))

    if msg["cmdtype"] == "setCell":
        print(msg)
        boardID = users[msg["token"]]["board"]
        if boardsData[boardID]["turn"] == users[msg["token"]]["team"]:
            setCell(msg["coords"], msg["val"], users[msg["token"]]["board"])
            print(msg["val"])
            victory = checkVictory(users[msg["token"]]["board"])
            if victory[0]:
                print(str(victory[1]) + " HAS WON MATCH " + str(users[msg["token"]]["board"]) + "! at " + str(winLocation))
                await websocket.send(json.dumps({"cmdtype":"victoryEvent", "winner":victory[1]}))
        
            if boardsData[boardID]["turn"] == "X":
                boardsData[boardID]["turn"] = "O"
            else:
                boardsData[boardID]["turn"] = "X"
            print("aoaasda")
            print(msg["val"])
            await websocket.send(json.dumps({"cmdtype":"stateChange", "coords":msg["coords"], "val":msg["val"], "turn":boardsData[boardID]["turn"], "team":users[msg["token"]]["team"]}))

    if (msg["cmdtype"] == "getCell"):
        await websocket.send(json.dumps({"cmdtype":"getCellResponse", "coords":msg["coords"], "val":getCell(msg["coords"], users[msg["token"]]["board"])}))


# setCell([2, 1, 1, 1], "X")
# setCell([1, 1, 1, 1], "X")
# setCell([0, 1, 1, 1], "X")
#checkIfInCenterOfLine(1, 1, 1, 1, False)

async def echo(websocket, path):
    async for message in websocket:
        await commandHandler(json.loads(message), websocket)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8000))
asyncio.get_event_loop().run_forever()





