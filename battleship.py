import os
import time
import sys
import random
from operator import itemgetter
import pickle
import requests

# Following two lists are used with coordinates to translate letters to numbers
letToNum = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9}
numToLet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Graphics for ships
shipPart = "■"
shipHit = "□"

difficulty = "Medium"
scoreMultiplier = 1
name = "Beta Tester"
name = name.center(16)


def initializeGame():
    global playerTable
    global aiTable
    global playerShips
    global aiShips
    global score
    global turnCounter

    global aiSearching
    global aiHitsInRow
    global aiNextCoordinates
    global aiHitCoordinates
    global deltaAxis

    # Values for medium difficulty's shooting logic
    aiSearching = False
    aiHitsInRow = 0
    aiNextCoordinates = []
    aiHitCoordinates = []
    deltaAxis = ""

    score = 0
    turnCounter = 0
    playerTable = [
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
    ]

    aiTable = [
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
        ['.', '.', '.', '.', '.', '.', '.', '.', ],
    ]

    playerShips = [
    {'id': 'playerShip1', 'name':'battleship', 'model': '■ ■ ■ ■', 'length': 4, 'damage': 0, 'coords':[]},
    {'id': 'playerShip2', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    {'id': 'playerShip3', 'name':'submarine', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    {'id': 'playerShip4', 'name':'corvette', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    {'id': 'playerShip5', 'name':'patrol boat', 'model': '■ ■', 'length': 2, 'damage': 0, 'coords':[]},
    ]

    # List of computer's ships
    aiShips = [
    {'id': 'aiShip1', 'name':'battleship', 'model': '■ ■ ■ ■', 'length': 4, 'damage': 0, 'coords':[]},
    {'id': 'aiShip2', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    {'id': 'aiShip3', 'name':'submarine', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    {'id': 'aiShip4', 'name':'corvette', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    {'id': 'aiShip5', 'name':'patrol boat', 'model': '■ ■', 'length': 2, 'damage': 0, 'coords':[]}
    ]

def setName():
    global name

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        name = input("Insert your name: ")

        if len(name) < 1:
            print("Please enter a name")
            time.sleep(1)
            continue
        if len(name) > 16:
            name = name[0:16]
        if len(name) < 16:
            name = name.center(16)
        break

def printTable():
    """Print the play field"""
    os.system('cls' if os.name == 'nt' else 'clear')
    rownum = 0
    global name

    print("╔════════════════╗   ╔════════════════╗")
    print("║"+name.upper()+"║   ║    COMPUTER    ║")
    print("╚════════════════╝   ╚════════════════╝")
    print("╔═A═B═C═D═E═F═G═H╗   ╔═A═B═C═D═E═F═G═H╗")
    for item_plr, item_ai in zip(playerTable, aiTable):
        print(rownum, end='')
        for i in item_plr:
            print(" "+i, end='', flush=True)
        print("║   "+str(rownum), end="")
        for j in item_ai:
            if j == shipPart:
                j = "." #Change this to "■" when you want to see enemy ships
            print(" "+j, end='', flush=True)
        print("║")
        rownum += 1
    print("╚════════════════╝   ╚════════════════╝")
    scoretext = "Score: "+str(int(score))
    textbox("■ = Ship section: intact", "□ = Ship section: hit","x = Missed shot", scoretext)

def textbox(*args):
    rowLengths = []

    for arg in args:
        arg = str(arg)
        rowLengths.append(len(arg))

    try:
        boxWidth = max(rowLengths) * "═"
    except ValueError:
        boxWidth = ""

    print("╔═"+boxWidth+"═╗")
    for arg in args:
        arg = str(arg)
        while len(arg)<max(rowLengths):
            arg = arg +" "
        print("║ "+arg+" ║")
    print("╚═"+boxWidth+"═╝")


def checkShip(posX, posY, shipNum, direction, who):
    """Check for collisions while placing"""
    if who == "player":
        table = playerTable
    elif who == "ai":
        table = aiTable
    shipRange = []
    global shipPart
    for i in range(shipNum['length']):
        if direction == "r":
            shipRange.append(table[posY][posX])
            posX += 1
        if direction == "d":
            shipRange.append(table[posY][posX])
            posY += 1
    if shipPart in shipRange:
        return True
    if shipPart not in shipRange:
        return False

def checkDamage(who):
    """Check if all ships have been destroyed"""
    totalHealth = 0
    totalDamage = 0
    if who == "player":
        table = playerShips
    elif who == "ai":
        table = aiShips

    for i in table:
        totalHealth = totalHealth + i['length']
        totalDamage = totalDamage + i['damage']
    if totalHealth == totalDamage:
        endGame(who)

def endGame(loser):
    global score
    if loser == "player":
        row1 = "The computer sunk all your ships!"
        row2 = "The computer wins!"
        score -= 500

    elif loser == "ai":
        row1 = "You sunk all the computer's ships!"
        row2 = "You win!"
        score += 500

    textbox(row1, row2)
    time.sleep(2)
    print("")
    input("(Press ENTER to continue)")
    saveHiScoreOnline(loser)
    mainMenu()


def placeShip(shipNum):
    while True:
        try:
            printTable()
            coords = input("Enter start coordinates for your "+shipNum['name']+" ("+shipNum['model']+") : ")
            startPosX = letToNum[coords[0].lower()]
            startPosY = int(coords[1])
            direction = input("Set direction (r)ight/(d)own): ")
            if not (direction=="r" or direction=="d"):
                print("Invalid direction")
                time.sleep(1.5)
                continue

            if direction == "r" and (startPosX + shipNum['length']) > 8:
                print("Does not fit: Out of bounds")
                time.sleep(1.5)
                continue
            if direction == "d" and (startPosY + shipNum['length']) > 8:
                print("Does not fit: Out of bounds")
                time.sleep(1.5)
                continue

            # Check for collisions
            if checkShip(startPosX, startPosY, shipNum, direction, "player") == True:
                print("Does not fit: Collides with another ship")
                time.sleep(1.5)
                continue

            # Place the ship part
            for i in range(shipNum['length']):
                if direction.lower() == "r":
                    drawShipPart(startPosX, startPosY)
                    # Update ships coordinates
                    shipNum['coords'].append(str(startPosX)+str(startPosY))
                    startPosX += 1
                elif direction.lower() == "d":
                    drawShipPart(startPosX, startPosY)
                    # Update ships coordinates
                    shipNum['coords'].append(str(startPosX)+str(startPosY))
                    startPosY += 1
            return
        except:
            print("Invalid coordinates")
            time.sleep(1.5)
        printTable()

def aiPlaceShip(shipNum):
    while True:
        startPosX = random.randint(0, 7)
        startPosY = random.randint(0, 7)
        direction = random.randint(0, 1)
        if direction == 0:
            direction = "r"
        elif direction == 1:
            direction = "d"

        if direction == "r" and (startPosX + shipNum['length']) > 8:
            continue
        if direction == "d" and (startPosY + shipNum['length']) > 8:
            continue

        # Check for collisions
        if checkShip(startPosX, startPosY, shipNum, direction, "ai") == True:
            continue

        # Place the ship part
        for i in range(shipNum['length']):
            if direction == "r":
                aiDrawShipPart(startPosX, startPosY)
                # Update ships coordinates
                shipNum['coords'].append(str(startPosX)+str(startPosY))
                startPosX += 1
            elif direction == "d":
                aiDrawShipPart(startPosX, startPosY)
                # Update ships coordinates
                shipNum['coords'].append(str(startPosX)+str(startPosY))
                startPosY += 1
        return


def aiPlacement():
    """AI placement phase"""
    for i in aiShips:
        aiPlaceShip(i)
    printTable()

def aiDrawShipPart(posX, posY):
    """Draw a ship piece in AI area"""
    aiTable[posY][posX] = shipPart

def drawShipPart(posX, posY):
    """Draw a ship piece in player area"""
    playerTable[posY][posX] = shipPart
    printTable()

def explosion(table, posX, posY, hit = False):
    """Hit logic"""
    global score
    global scoreMultiplier
    global aiSearching
    global aiHitCoordinates
    ships = []

    if table == aiTable:
        ships = aiShips
    elif table == playerTable:
        ships = playerShips

    # If the tile is already a destroyed ship part
    if table[posY][posX] == shipHit:
        table[posY][posX] = shipHit
        printTable()
        return

    if hit:
        table[posY][posX] = shipHit
        printTable()

        if table == playerTable:
            row1 = "Computer's turn"
            row2 = "Computer fires at " +numToLet[posX] + str(posY)+"."
            textbox(row1)
            time.sleep(1.5)
            printTable()
            textbox(row1, row2)
            time.sleep(1.5)
            printTable()

        if table == aiTable:
            row1 = "Your turn"
            row2 = "You fire at " +numToLet[posX] + str(posY)+"."
            row3 = "That's a hit!"
            textbox(row1, row2)
            time.sleep(1.5)
            printTable()
            textbox(row1, row2, row3)
            time.sleep(1.5)
            printTable()

        for i in ships:
            if str(posX)+str(posY) in i['coords']:
                if table == playerTable:
                    row3 = "... and hits your "+i['name']+"!"
                    textbox(row1, row2, row3)
                    time.sleep(1.5)

                i['damage'] += 1
                if i['length'] == i['damage']:
                    if table == aiTable:
                        row4 = "Ship Destroyed! You sunk the " +i['name']+"."
                        score += (100*scoreMultiplier)

                    elif table == playerTable:
                        row4 = "Ship Destroyed! Computer sunk your " +i['name']+"."
                        score -= (50*scoreMultiplier)
                        aiSearching = False # Stop searching the proximity for ship parts
                        aiHitsInRow = 0 # Reset hits in row
                        aiHitCoordinates = []   # Reset the first hit coordinates
                    printTable()
                    textbox(row1, row2, row3, row4)
                    time.sleep(2)

    else:
        if table == playerTable:
            row1 = "Computer's turn"
            row2 = "Computer fires at " +numToLet[posX] + str(posY)+"."
            row3 = "... and misses."
            table[posY][posX] = "x"
            textbox(row1)
            time.sleep(1.5)
            printTable()
            textbox(row1, row2)
            time.sleep(1.5)
            printTable()
            textbox(row1, row2, row3)
            time.sleep(1.5)


        if table == aiTable:
            row1 = "Your turn"
            row2 = "You fire at " +numToLet[posX] + str(posY)+"."
            row3 = "... you miss."
            if table[posY][posX] == shipHit:
                pass
            else:
                table[posY][posX] = "x"
            textbox(row1, row2)
            time.sleep(1.5)
            printTable()
            textbox(row1, row2, row3)
            time.sleep(1.5)

    printTable()



def playerFire():
    global score
    while True:
        try:
            printTable()
            print("Your turn")
            coords = input("Enter coordinates to fire at: ")
            printTable()
            posX = letToNum[coords[0].lower()]
            posY = int(coords[1])

            if aiTable[posY][posX] == shipPart:
                score += (100*scoreMultiplier)
                explosion(aiTable, posX, posY, hit = True)
                checkDamage("ai")

            else:
                explosion(aiTable, posX, posY, hit = False)
            break
        except IndexError:
            print("Give proper coordinates! Range: a0 to h7")
            time.sleep(1)
        except KeyError:
            print("Give proper coordinates! Range: a0 to h7")
            time.sleep(1)
        except ValueError:
            print("Give proper coordinates! Range: a0 to h7")
            time.sleep(1)

def aiFire():
    global difficulty
    global score
    global aiHitCoordinates
    global aiSearching
    global aiHitsInRow
    printTable()
    if difficulty == "Easy":
        while True:
            posX = random.randint(0, 7)
            posY = random.randint(0, 7)
            # Do not fire again at broken ships or earlier misses
            if playerTable[posY][posX] == shipHit:
                continue
            if playerTable[posY][posX] == "x":
                continue

            # Fire at a ship part
            if playerTable[posY][posX] == shipPart:
                score -= (50*scoreMultiplier)
                explosion(playerTable, posX, posY, hit = True)
                checkDamage("player")

            # Missed shot
            else:
                explosion(playerTable, posX, posY, hit = False)
            return

    if difficulty == "Medium":
        while True:
            if aiSearching == False:    # If AI hasn't hit, just randomize next shot
                posX = random.randint(0, 7)
                posY = random.randint(0, 7)
            elif aiSearching == True:   # If AI has hit, next shot is determined by randomdirection
                posX, posY = randomDirection()
                # print("randomdir result:", numToLet[posX], posY)
                # input("ok")

            # Do not fire again at broken ships or earlier misses
            if playerTable[posY][posX] == "x":
                # print("That would be a miss. let's find new coordinates")
                continue



            # Fire at a ship part
            if playerTable[posY][posX] == shipPart:
                aiSearching = True
                aiHitsInRow += 1
                aiHitCoordinates.append([posX, posY])
                score -= (50*scoreMultiplier)
                explosion(playerTable, posX, posY, hit = True)
                checkDamage("player")

            # Missed shot
            else:
                aiHitsInRow = 0
                explosion(playerTable, posX, posY, hit = False)
            return


    if difficulty == "Impossible":
        for i in playerTable:
            for j in i:
                if j == shipPart:
                    posY = playerTable.index(i)
                    posX = i.index(shipPart)
                    explosion(playerTable, posX, posY, hit = True)
                    checkDamage("player")
                    score -= (50*scoreMultiplier)
                    return


def randomDirection():
    """Sweet artificial intelligence. Figures out where to fire next."""
    global aiHitsInRow
    global deltaAxis
    newPosX = aiHitCoordinates[len(aiHitCoordinates)-1][0]
    newPosY = aiHitCoordinates[len(aiHitCoordinates)-1][1]
    hangPreventer = 0

    # DEBUG PRINTS
    # print("aiHitCoordinates[0][0] X:",numToLet[aiHitCoordinates[0][0]])
    # print("aiHitCoordinates[0][0] Y:",aiHitCoordinates[0][1])
    # print("newposX aiHitCoordinates[len(aiHitCoordinates)-1][0]:",numToLet[newPosX])
    # print("newposY aiHitCoordinates[len(aiHitCoordinates)-1][1]:",newPosY)
    # print("deltaAxis:",deltaAxis)
    # print("aiHitsInRow:",aiHitsInRow)
    # print("len(aiHitCoordinates):",len(aiHitCoordinates))
    # print("")

    while True:

        hangPreventer += 1
        # print(hangPreventer)
        if hangPreventer >7 and hangPreventer < 30:
            # print("HANG PREVENTER ACTIVATED")
            if deltaAxis == "negativeX" or deltaAxis == "positiveX":
                selectPolarity = random.randint(0,1)
                if selectPolarity == 0:
                    deltaAxis = "negativeY"
                elif selectPolarity == 1:
                    deltaAxis = "positiveY"

            if deltaAxis == "negativeY" or deltaAxis == "positiveY":
                selectPolarity = random.randint(0,1)
                if selectPolarity == 0:
                    deltaAxis = "negativeX"
                elif selectPolarity == 1:
                    deltaAxis = "positiveX"
        elif hangPreventer >= 30:
            # print("cannot undo hang. resetting")
            # input("ok")
            aiSearching = False
            aiHitsInRow = 0

            while True:
                newPosY = random.randint(0, 7)
                newPosY = random.randint(0, 7)
                if playerTable[newPosY][newPosX]=="x" or playerTable[newPosY][newPosX]==shipHit:
                    continue
                else:
                    return(newPosX, newPosY)
            # END HANG HANGPREVENTER


        newPosX = aiHitCoordinates[len(aiHitCoordinates)-1][0]
        newPosY = aiHitCoordinates[len(aiHitCoordinates)-1][1]

        if aiHitsInRow == 1 and len(aiHitCoordinates) == 1:
            selectAxis = random.randint(0,1)
            selectPolarity = random.randint(0,1)
            # print("Newaxis:", selectAxis)
            # print("newpolarity:",selectPolarity)

            if selectAxis == 0:
                if selectPolarity == 0:
                    newPosX -= 1
                    deltaAxis = "negativeX"
                    # print("negativeX")
                elif selectPolarity == 1:
                    newPosX += 1
                    deltaAxis = "positiveX"
                    # print("positiveX")
            elif selectAxis == 1:
                if selectPolarity == 0:
                    newPosY -= 1
                    deltaAxis = "negativeY"
                    # print("negativeY")
                elif selectPolarity == 1:
                    newPosY += 1
                    deltaAxis = "positiveY"
                    # print("positiveY")
            if newPosX < 0 or newPosX > 7 or newPosY < 0 or newPosY > 7:
                # print("overflow, redo")
                continue

        if aiHitsInRow == 0 or playerTable[newPosY][newPosX]=="x":
            aiNextCoordinates = aiHitCoordinates[0]
            if deltaAxis == "negativeX":
                deltaAxis = "positiveX"
                newPosX = aiHitCoordinates[0][0] + 1
            elif deltaAxis == "positiveX":
                deltaAxis = "negativeX"
                newPosX = aiHitCoordinates[0][0] - 1
            elif deltaAxis == "negativeY":
                deltaAxis = "positiveY"
                newPosY = aiHitCoordinates[0][1] + 1
            elif deltaAxis == "positiveY":
                deltaAxis = "negativeY"
                newPosY = aiHitCoordinates[0][1] - 1

            if newPosX < 0 or newPosY < 0 or newPosX > 7 or newPosY > 7:
                aiNextCoordinates = aiHitCoordinates[0]
                if deltaAxis == "negativeX":
                    deltaAxis = "positiveX"
                    newPosX = aiHitCoordinates[0][0] + 1
                elif deltaAxis == "positiveX":
                    deltaAxis = "negativeX"
                    newPosX = aiHitCoordinates[0][0] - 1
                elif deltaAxis == "negativeY":
                    deltaAxis = "positiveY"
                    newPosY = aiHitCoordinates[0][1] + 1
                elif deltaAxis == "positiveY":
                    deltaAxis = "negativeY"
                    newPosY = aiHitCoordinates[0][1] - 1



        elif aiHitsInRow >= 1 and len(aiHitCoordinates) > 1:
            if deltaAxis == "negativeX":
                newPosX -= 1
            elif deltaAxis == "positiveX":
                newPosX += 1
            elif deltaAxis == "negativeY":
                newPosY -= 1
            elif deltaAxis == "positiveY":
                newPosY += 1

            if newPosX < 0 or newPosY < 0 or newPosX > 7 or newPosY > 7 or playerTable[newPosY][newPosX]=="x":
                aiNextCoordinates = aiHitCoordinates[0]
                if deltaAxis == "negativeX":
                    deltaAxis = "positiveX"
                    newPosX = aiHitCoordinates[0][0] + 1
                elif deltaAxis == "positiveX":
                    deltaAxis = "negativeX"
                    newPosX = aiHitCoordinates[0][0] - 1
                elif deltaAxis == "negativeY":
                    deltaAxis = "positiveY"
                    newPosY = aiHitCoordinates[0][1] + 1
                elif deltaAxis == "positiveY":
                    deltaAxis = "negativeY"
                    newPosY = aiHitCoordinates[0][1] - 1

        try:
            if playerTable[newPosY][newPosX]==shipHit:
                if deltaAxis == "negativeX":
                    newPosX -= 1
                elif deltaAxis == "positiveX":
                    newPosX += 1
                elif deltaAxis == "negativeY":
                    newPosY -= 1
                elif deltaAxis == "positiveY":
                    newPosY += 1
            if playerTable[newPosY][newPosX] == "x":
                # print("It is miss, lets redo")
                continue
            if playerTable[newPosY][newPosX] == shipHit:
                # print("It is shiphit, lets redo")
                continue


        except:
            # print("oopsie. lets continue")
            continue




        #input("ok")
        return newPosX, newPosY



def playerPlacement():
    print("Placement phase begins!")
    print("You have five ships to place!")
    input("(Press ENTER to continue)")
    for i in playerShips:
        placeShip(i)
    print("Placement phase complete.")
    time.sleep(1)

def firingPhase():
    global turnCounter
    print("Starting firing phase!")
    time.sleep(1)
    while True:
        turnCounter += 1
        playerFire()
        aiFire()

def setDifficulty():
    global difficulty
    global scoreMultiplier
    os.system('cls' if os.name == 'nt' else 'clear')


    print("SET DIFFICULTY")
    print("")
    textbox("1. Easy")
    print(" -The computer fires at random coordinates. 50% score.")
    textbox("2. Normal")
    print(" -Default difficulty. The computer is a bit more clever. 100% score.")
    textbox("3. Impossible")
    print(" -The computer has radar, sonar and homing missiles. 200% score.")
    print("")


    diffSetting = input("Make a selection: ")

    if diffSetting == "1":
        difficulty = "Easy"
        scoreMultiplier = 0.5
    elif diffSetting == "2":
       difficulty = "Normal"
       scoreMultiplier = 1
    elif diffSetting == "3":
        difficulty = "Impossible"
        scoreMultiplier = 2
    else:
        print("\tInvalid selection!")
        time.sleep(1)
        setDifficulty()

def hiScoreExists():
    """Check if the high score file exists, and create one if there is no file."""
    emptylist = []
    try:
        hiscore = open("hiscore.file", 'rb')
        hiscore.close()
    except IOError:
        hiscore = open("hiscore.file", 'wb')
        pickle.dump(emptylist, hiscore)
        hiscore.close()

def saveHiScore(loser):
    """Save the current score as a tuple. High Score list contains 10 best scores. If list is longer, the lowest score is discarded"""
    high_scores = []
    global score
    global name
    global difficulty
    global turnCounter
    hiScoreExists()

    if loser == "ai":
        outcome = "Game WON in "+str(turnCounter)+" turns"
    elif loser == "player":
        outcome = "Game LOST in "+str(turnCounter)+" turns"

    try:

        with open('hiscore.file', 'rb') as hs:
            high_scores = pickle.load(hs)

        high_scores.append((name.strip(), int(score), difficulty, outcome))

        high_scores = sorted(high_scores, key=itemgetter(1),reverse=True)[:10]

        with  open("hiscore.file","wb") as hiscore:
            pickle.dump(high_scores, hiscore)
    except:
        print("Error saving hiscore")
        time.sleep(1)

def saveHiScoreOnline(loser):
    """Save the highscore in MySQL database"""
    global score
    global name
    global difficulty
    global turnCounter

    if loser == "ai":
        outcome = "WON"
    elif loser == "player":
        outcome = "LOST"

    try:
        r = requests.post("http://renki.dy.fi/battleship/addscore.php", data={'playername':name.strip(), 'score':score, 'difficulty':difficulty, 'outcome':outcome, 'turns':turnCounter})

    except:
        print("Error saving hiscore")
        print("Using local hiscore list instead")
        input("ok")
        saveHiScore(loser)


def readHiScore():
    """Displays the current high scores"""
    os.system('cls' if os.name == 'nt' else 'clear')
    high_scores = []
    hiScoreExists()
    print("=======================================================================================")
    print("|  ██╗  ██╗██╗ ██████╗ ██╗  ██╗    ███████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗  |")
    print("|  ██║  ██║██║██╔════╝ ██║  ██║    ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝  |")
    print("|  ███████║██║██║  ███╗███████║    ███████╗██║     ██║   ██║██████╔╝█████╗  ███████╗  |")
    print("|  ██╔══██║██║██║   ██║██╔══██║    ╚════██║██║     ██║   ██║██╔══██╗██╔══╝  ╚════██║  |")
    print("|  ██║  ██║██║╚██████╔╝██║  ██║    ███████║╚██████╗╚██████╔╝██║  ██║███████╗███████║  |")
    print("|  ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝  |")
    print("=10=BEST=SCORES========================================================================")
    rowNum = 1

    try:
        with open('hiscore.file', 'rb') as hs:
            high_scores = pickle.load(hs)

        for i in high_scores:
            name, score, difficulty, outcome = i

            print(str(rowNum).rjust(2)+". ",\
                name.ljust(16,'.'),\
                "| Score:....",str(score).rjust(4, '.'),\
                "| Difficulty:..",difficulty.rjust(10, '.'),\
                "| ",outcome,\
                 sep='')
            rowNum += 1

        if len(high_scores) == 0:
            print("No high scores yet!")
        print("=======================================================================================")
        print("\n")
    except:
        print("Error: High score file corrupted.")
    usrInput = input("(Press ENTER to continue) ")

    if usrInput == "clear":
        os.remove("hiscore.file")

def readHiScoreOnline():
    """Displays the current high scores from online"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=======================================================================================")
    print("|  ██╗  ██╗██╗ ██████╗ ██╗  ██╗    ███████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗  |")
    print("|  ██║  ██║██║██╔════╝ ██║  ██║    ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝  |")
    print("|  ███████║██║██║  ███╗███████║    ███████╗██║     ██║   ██║██████╔╝█████╗  ███████╗  |")
    print("|  ██╔══██║██║██║   ██║██╔══██║    ╚════██║██║     ██║   ██║██╔══██╗██╔══╝  ╚════██║  |")
    print("|  ██║  ██║██║╚██████╔╝██║  ██║    ███████║╚██████╗╚██████╔╝██║  ██║███████╗███████║  |")
    print("|  ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝  |")
    print("=10=BEST=SCORES================================================================ONLINE!=")
    rowNum = 1

    try:
        r = requests.get("http://renki.dy.fi/battleship/getscore.php")
        high_scores = r.json()

        for i in high_scores['scores']:
            print(str(rowNum).rjust(2)+". ",\
            i['playername'].ljust(16,'.'),\
            "| Score:....",str(i['score']).rjust(4, '.'),\
            "| Difficulty:..",i['difficulty'].rjust(10, '.'),\
            "| ",i['outcome'], " in ", i['turns'], " turns",\
            sep='')
            rowNum += 1

        if len(high_scores) == 0:
            print("No high scores yet!")
        print("===============================================================================ONLINE!=")
        print("\n")
    except:
        print("Error reading hiscore.")
        print("Using local hiscore list instead.")
        time.sleep(1)
        readHiScore()
    usrInput = input("(Press ENTER to continue) ")

    if usrInput == "clear":
        os.remove("hiscore.file")




def mainMenu():
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("==By=Matias=Räisänen=============================================================")
            print("| ██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗  |")
            print("| ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗ |")
            print("| ██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝ |")
            print("| ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝  |")
            print("| ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║      |")
            print("| ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝      |")
            print("=========================================================================v.=1.1==")


            row1 = "(1) New game"
            row2 = "(2) Set difficulty"
            row3 = "(3) How to play"
            row4 = "(4) Show high scores"
            row5 = "(5) About"
            row6 = "(6) Quit"
            textbox(row1, row2, row3, row4, row5, row6)

            selection = input("Make a selection: ")

            if selection == "1":
                newGame()
            elif selection =="2":
                setDifficulty()

            elif selection == "3":
                """How to play"""
                os.system('cls' if os.name == 'nt' else 'clear')
                print("HOW TO PLAY")
                print("")
                textbox("Placement phase")
                print("Place your ships. First, set the coordinates where you want your ship's starting point to be.")
                print("Next, choose the direction to extend your ship to.")
                print("Make sure you stay withing the boundaries of the coordinates from a0 to h7.")
                print("")
                textbox("Firing phase")
                print("Take turns firing with the computer.")
                print("The first one to sink each of the opponent's ships is the winner.")
                print("")
                textbox("Scoring")
                print("Enemy ship hit = 100pts")
                print("Enemy ship sunk = 200pts")
                print("You win = 500pts")
                print("Player ship hit = -50pts")
                print("Player ship sunk = -100pts")
                print("Computer wins = -500pts")
                input("(Press ENTER to continue)")
                continue
            elif selection == "5":
                """About"""
                os.system('cls' if os.name == 'nt' else 'clear')
                print("ABOUT")
                print("")
                textbox("A game of Battleship.", "Made by Matias Räisänen in 2018.", "Programmed in Python.")
                print("")
                input("(Press ENTER to continue)")
                continue
            elif selection == "6":
                """Quit"""
                print("\nThanks for playing!")
                sys.exit()
            elif selection == "4":
                readHiScoreOnline()
            else:
                print("Invalid selection.")
                time.sleep(1)
                continue
    except KeyboardInterrupt:
        print("\nThanks for playing!")


def newGame():
    initializeGame()
    setName()
    printTable()
    aiPlacement()
    playerPlacement()
    firingPhase()


if __name__ == '__main__':
    mainMenu()
