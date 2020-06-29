import asyncio
import ssl
import pathlib
import json
import random
import sys
import time
import ACI
import threading
print(sys.executable)
conn = 0



import websockets

print("Server online. ")

numDimensions = 3
width = 3
winLocation = []
nextTeamToAssign = "X"
boards = {}

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
    return boards[boardID].boardState[coords[0]][coords[1]][coords[2]][coords[3]]

def setCell(coords, val, boardID):
    
    i = 0
    #[0, 1, 1]
    subArrayString = "boards[" + str(boardID) + "]" + ".boardState"
    while i < len(coords):
        subArrayString += "[" + str(coords[i]) + "]"
        i += 1

    exec(str(subArrayString) + " = val")

    boards[boardID].lastInteract = time.time()

class board:
    def __init__(self):
        self.id = self.generateBoardID()
        self.boardState = createDimension()
        self.turn = "X"
        self.players = []
        self.gameState = "inProgress"
        self.visibility = "Public"
        self.lastInteract = time.time()
    
    def generateBoardID(self):
        genID = random.randint(1,10000)
        for i in boards:
            if boards[i].id == genID:
                genID = self.generateBoardID()

        return genID

    async def updatePlayerList(self):
        for token in self.players:
            usernames = []
            for token in self.players:
                usernames.append(users[token]["username"])
            for token in self.players: 
                data = json.dumps({"cmdtype":"loginResponse", "board":boards[users[token]["board"]].id, "team":users[token]["team"], "turn":boards[users[token]["board"]].turn, "token":token, "users":usernames, "stats":{"numGames": await conn["TicTac"]["numGames"], "numMoves": await conn["TicTac"]["numMoves"], "numXWins": await conn["TicTac"]["numXWins"], "numOWins": await conn["TicTac"]["numOWins"], "avgMovesPerGame": await conn["TicTac"]["avgMovesPerGame"], "numPageLoads": await conn["TicTac"]["numPageLoads"]}})
                asyncio.create_task(self.sendMSG(data, token))

    async def sendMSG(self, data, token):
        try:
            await users[token]["socket"].send(data)
        except:
            print("Player no longer active")

async def generateBoard():
    async with conn["TicTac"] as interface:
        interface["numGames"] = int(await conn["TicTac"]["numGames"]) + 1
    temp = board()
    boards[temp.id] = temp
    return temp.id
    del temp

async def generateToken(websocket, joinConfig):
    global nextTeamToAssign
    token = random.randint(1,10000)
    if token in users:
        token = generateToken()

    boardID = "NOTFOUND"

    if joinConfig["type"] == "existing":
        if joinConfig["ID"] == "AVALIABLE":
            boardsToDelete = []
            for i in boards:
                if len(boards[i].players) < 2 and boardID == "NOTFOUND" and boards[i].visibility != "Private":
                    if boards[i].lastInteract < time.time() - 25:
                        boardsToDelete.append(i)
                    else:
                        boardID = i
                        boards[i].players.append(token)
                        boards[i].lastInteract = time.time()
            
            for i in boardsToDelete:
                del boards[i]
            if boardID == "NOTFOUND":
                boardID = await generateBoard()
                boards[boardID].players.append(token)
        else:
            if int(joinConfig["ID"]) in boards:
                boardID = int(joinConfig["ID"])
                print(boards)
                boards[boardID].players.append(token)
                boards[boardID].lastInteract = time.time()
            else:
                return "ERR-Board Does Not Exist"
    elif joinConfig["type"] == "new":
        boardID = generateBoard()
        boards[boardID].players.append(token)
        boards[boardID].visibility = "Private"
            

    print("Assiging Team" + nextTeamToAssign)
    users[token] = {"token":token, "team":nextTeamToAssign, "board":boardID, "socket":websocket, "username":"None", "heartbeat":time.time()}
    if (nextTeamToAssign == "X"):
        nextTeamToAssign = "O"
    elif (nextTeamToAssign == "O"):
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
                        
                        if (boards[boardID].boardState[bx+focusbx][by+focusby][sx+focussx][sy+focussy] == boards[boardID].boardState[bx][by][sx][sy]):
                            #print("Adjacent Found " + str([bx+focusbx, by+focusby, sx+focussx, sy+focussy]))
                            testVar = [focusbx, focusby, focussx, focussy, boards[boardID].boardState[bx+focusbx][by+focusby][sx+focussx][sy+focussy], bx, by, sx, sy]
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
            if i[0] == -k[0] and i[1] == -k[1] and i[2] == -k[2] and i[3] == -k[3] and i[4] == boards[boardID].boardState[i[5]][i[6]][i[7]][i[8]] and i[4] != 0 and i[4] != 1:
                print(i)
                foundWinCondition = True
                winner = i[4]
                hasWrittenAnything = True
                winLocation = [i[5], i[6], i[7], i[8]]
                print(str(winLocation) + " " + str(i))
    if (hasWrittenAnything):
        print("----")
    if (not foundWinCondition):
        return [False, 15]
    else:
        return [foundWinCondition, winner]

def checkHeartbeats():
    tokensToRemove = []
    for token in users:
        if users[token]["heartbeat"] < time.time() - 15:
            tokensToRemove.append(token)

    for token in tokensToRemove:
        print(token)
        print(users[token]["board"])
        if users[token]["board"] in boards:
            for index, player in enumerate(boards[users[token]["board"]].players):
                if player == token:
                    boardID = users[token]["board"]
                    boards[users[token]["board"]].players.remove(player)
                    users.pop(player)
                    boards[boardID].updatePlayerList()
        else:
            users.pop(token)


async def commandHandler(msg, websocket):

    checkHeartbeats()

    if msg["cmdtype"] == "login":
        print("Player is loging in.")
        newToken = await generateToken(websocket, msg["joinConfig"])
        if isinstance(newToken, str):
            await websocket.send(json.dumps({"cmdtype":"loginError", "errMsg":newToken}))
        else:
            users[newToken]["username"] = msg["joinConfig"]["username"]
            await boards[users[newToken]["board"]].updatePlayerList()

        for bx in boards[users[newToken]["board"]].boardState:
            for by in boards[users[newToken]["board"]].boardState[bx]:
                for sx in boards[users[newToken]["board"]].boardState[bx][by]:
                    for sy in boards[users[newToken]["board"]].boardState[bx][by][sx]:
                        if boards[users[newToken]["board"]].boardState[bx][by][sx][sy] == "X" or boards[users[newToken]["board"]].boardState[bx][by][sx][sy] == "O":
                            print("Sending BoardState to new User")
                            await websocket.send(json.dumps({"cmdtype":"stateChange", "coords":[bx, by, sx, sy], "val":boards[users[newToken]["board"]].boardState[bx][by][sx][sy], "turn":boards[users[newToken]["board"]].turn, "team":users[newToken]["team"]}))

    if msg["cmdtype"] == "setCell":
        boardID = users[msg["token"]]["board"]
        if boardID in boards:
            if boards[boardID].turn == users[msg["token"]]["team"] and boards[boardID].gameState == "inProgress":
                if getCell(msg["coords"], boardID) != "X" and getCell(msg["coords"], boardID) != "O":
                    setCell(msg["coords"], msg["val"], users[msg["token"]]["board"])
                    print(msg["val"])
                    victory = checkVictory(users[msg["token"]]["board"])
                
                    if boards[boardID].turn == "X":
                        boards[boardID].turn = "O"
                    else:
                        boards[boardID].turn = "X"
                    await websocket.send(json.dumps({"cmdtype":"stateChange", "coords":msg["coords"], "val":msg["val"], "turn":boards[boardID].turn, "team":users[msg["token"]]["team"]}))
                    async with conn["TicTac"] as interface:
                        interface["numMoves"] = int(await conn["TicTac"]["numMoves"]) + 1
                    async with conn["TicTac"] as interface:
                        interface["avgMovesPerGame"] = round(int(await conn["TicTac"]["numMoves"])/int(await conn["TicTac"]["numGames"]),1)
                    
                    for u in users:
                        if users[u]["board"] == boardID:
                            await users[u]["socket"].send(json.dumps({"cmdtype":"stateChange", "coords":msg["coords"], "val":msg["val"], "turn":boards[boardID].turn, "team":users[msg["token"]]["team"]}))
                            if victory[0]:
                                await users[u]["socket"].send(json.dumps({"cmdtype":"victoryEvent", "winner":victory[1]}))

                    if victory[0]:
                        async with conn["TicTac"] as interface:
                            interface["num" + victory[1] + "Wins"] = int(await conn["TicTac"]["num" + victory[1] + "Wins"]) + 1
                        print(str(victory[1]) + " HAS WON MATCH " + str(users[msg["token"]]["board"]) + "! at " + str(winLocation))
                        boards[boardID].gameState = "Ended"
                        del boards[boardID]
        else:
            await websocket.send(json.dumps({"cmdtype":"victoryEvent", "winner":"Timeout"}))

    if (msg["cmdtype"] == "getCell"):
        if users[msg["token"]]["board"] in boards:
            await websocket.send(json.dumps({"cmdtype":"getCellResponse", "coords":msg["coords"], "val":getCell(msg["coords"], users[msg["token"]]["board"])}))
        else:
            await websocket.send(json.dumps({"cmdtype":"victoryEvent", "winner":"Timeout"}))
    
    if (msg["cmdtype"] == "heartbeat"):
        users[msg["token"]]["heartbeat"] = time.time()

async def echo(websocket, path):
    global conn
    print(websocket)
    conn = await ACI.async_create(ACI.Client, 8765, "127.0.0.1", "main")
    time.sleep(0.5)
    async with conn["TicTac"] as interface:
        interface["numPageLoads"] = int(await conn["TicTac"]["numPageLoads"]) + 1
        ACITokenfile = open("/home/tokens/tictac.txt", 'r')
        ACIToken = ACITokenfile.read()
        ACITokenfile.close()
        conn.authenticate("bots.tictac", ACIToken)

    time.sleep(0.5)

    await websocket.send(json.dumps({"cmdtype":"stats", "stats":{"numGames": await conn["TicTac"]["numGames"], "numMoves": await conn["TicTac"]["numMoves"], "numXWins": await conn["TicTac"]["numXWins"], "numOWins": await conn["TicTac"]["numOWins"], "avgMovesPerGame": await conn["TicTac"]["avgMovesPerGame"], "numPageLoads": await conn["TicTac"]["numPageLoads"]}}))
    try:
        async for message in websocket:
            print(message)
            #getNumGames()
            await commandHandler(json.loads(message), websocket)
    except websockets.exceptions.ConnectionClosedError:
        print("Client Disconnecting.")



asyncio.set_event_loop(asyncio.new_event_loop())
asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, port=8000))
print("Listening")
asyncio.get_event_loop().run_forever()





