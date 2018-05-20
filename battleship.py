import os
import time
import sys
import random
from operator import itemgetter
import pickle

# Following two lists are used to translate the letter in the coordinates back into numbers.
letToNum = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9}
numToLet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Graphics for ships
shipPart = "■"
shipHit = "□"

# The following are values for the shooting artificial intelligence
aiDidHit = False
aiHitsInRow = 0
aiNextCoordinates = ""
deltaAxis = ""
difficulty = "easy"

# List of player's ships
playerTable = []
aiTable = []
playerShips = []
aiShips = []
score = 0
name = "Beta Tester"




def initializeGame():
    global playerTable
    global aiTable
    global playerShips
    global aiShips
    global score

    score = 0
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
    # {'id': 'playerShip2', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    # {'id': 'playerShip3', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    # {'id': 'playerShip4', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    # {'id': 'playerShip5', 'name':'patrol boat', 'model': '■ ■', 'length': 2, 'damage': 0, 'coords':[]},
    ]

    # List of computer's ships
    aiShips = [
    # {'id': 'aiShip1', 'name':'battleship', 'model': '■ ■ ■ ■', 'length': 4, 'damage': 0, 'coords':[]},
    # {'id': 'aiShip2', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    # {'id': 'aiShip3', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    # {'id': 'aiShip4', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
    {'id': 'aiShip5', 'name':'patrol boat', 'model': '■ ■', 'length': 2, 'damage': 0, 'coords':[]}
    ]


def printTable():
    '''Print the play field'''
    os.system('cls' if os.name == 'nt' else 'clear')
    rownum = 0

    print("##################   ##################")
    print("#   YOUR SHIPS   #   #   THEIR SHIPS  #")
    print("##################   ##################")
    print("# A B C D E F G H#   # A B C D E F G H#")
    for item_plr, item_ai in zip(playerTable, aiTable):
        print(rownum, end='')
        for i in item_plr:
            print(" "+i, end='', flush=True)
        print("#   "+str(rownum), end="")
        for j in item_ai:
            if j == shipPart:
                j = "■" #Change this to "■" when you wanna see enemy ships
            print(" "+j, end='', flush=True)
        print("#")
        rownum += 1
    print("##################   ##################")
    print("■ = Ship section: intact")
    print("□ = Ship section: hit")
    print("x = Missed shot")
    print(". = Open sea")
    print("Score:", score)
    print("")


def checkShip(posX, posY, shipNum, direction, who):
    '''Check for collisions while placing'''
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
    '''Check if all ships have been destroyed'''
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

def endGame(who):
    if who == "player":
        print("The computer sunk all your ships!")
        print("The computer wins!")
        time.sleep(3)
    elif who == "ai":
        print("You sunk all the computer's ships!")
        print("You win!")
        time.sleep(2)
    saveHiScore()
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
                if direction == "r":
                    drawShipPart(startPosX, startPosY)
                    # Update ships coordinates
                    shipNum['coords'].append(str(startPosX)+str(startPosY))
                    startPosX += 1
                elif direction == "d":
                    drawShipPart(startPosX, startPosY)
                    # Update ships coordinates
                    shipNum['coords'].append(str(startPosX)+str(startPosY))
                    startPosY += 1
            return
        except IndexError:
            print("Invalid coordinates")
            time.sleep(1.5)
        except KeyError:
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
    for i in aiShips:
        aiPlaceShip(i)
    printTable()

def aiDrawShipPart(posX, posY):
    aiTable[posY][posX] = shipPart

def drawShipPart(posX, posY):
    playerTable[posY][posX] = shipPart
    printTable()

def explosion(table, posX, posY, hit = False):
    global score
    ships = []

    if table == aiTable:
        ships = aiShips
    elif table == playerTable:
        ships = playerShips

    # If the tile is already a destroyed ship part
    if table[posY][posX] == shipHit:
        table[posY][posX] = "*"
        time.sleep(.2)
        printTable()
        table[posY][posX] = "¤"
        time.sleep(.2)
        printTable()
        table[posY][posX] = shipHit
        printTable()
        return

    # Else lets blow it up!
    table[posY][posX] = "*"
    time.sleep(.2)
    printTable()
    table[posY][posX] = "¤"
    time.sleep(.2)
    printTable()

    if hit:
        table[posY][posX] = shipHit
        printTable()

        if table == playerTable:
            print("Computer's turn")
            time.sleep(1)
            print("Computer fires at " +numToLet[posX] + str(posY)+".")
            time.sleep(1)

        if table == aiTable:
            print("You fire at " +numToLet[posX] + str(posY)+".")
            time.sleep(1)
            print("That's a hit!")
            time.sleep(1)

        for i in ships:
            if str(posX)+str(posY) in i['coords']:
                if table == playerTable:
                    print("... and hits your "+i['name']+"!")
                time.sleep(1)

                i['damage'] += 1
                if i['length'] == i['damage']:
                    if table == aiTable:
                        print("Ship Destroyed! You sunk the " +i['name']+".")
                        score += 200
                        time.sleep(1)
                    elif table == playerTable:
                        print("Ship Destroyed! Computer sunk your " +i['name']+".")
                        score -= 50
                        time.sleep(1)

    else:
        if table == playerTable:
            print("Computer's turn")
            time.sleep(1)
            print("Computer fires at " +numToLet[posX] + str(posY)+".")
            time.sleep(1)
            print("... and misses!")
            time.sleep(1)

        if table == aiTable:
            print("You fire at " +numToLet[posX] + str(posY)+".")
            time.sleep(1)
            print("... you miss.")
            time.sleep(1)
            if table[posY][posX] == shipHit:
                pass
            else:
                print(table[posY][posX])
                table[posY][posX] = "x"
    printTable()



def playerFire():
    global score
    while True:
        try:
            printTable()
            print("Your turn")
            coords = input("Enter coordinates to fire at: ")
            posX = letToNum[coords[0].lower()]
            posY = int(coords[1])

            if aiTable[posY][posX] == shipPart:
                score += 100
                explosion(aiTable, posX, posY, hit = True)
                checkDamage("ai")

            else:
                explosion(aiTable, posX, posY, hit = False)
            break
        except IndexError:
            print("Give proper coordinates! Range: a0 to h7")
            time.sleep(1.5)
        except KeyError:
            print("Give proper coordinates! Range: a0 to h7")
            time.sleep(1.5)
        except ValueError:
            print("Give proper coordinates! Range: a0 to h7")
            time.sleep(1.5)

# def aiFire():
#     global score
#     global aiDidHit
#     global aiNextCoordinates
#     global aiHitsInRow
#     printTable()
#     while True:
#         if aiDidHit == False:
#             posX = random.randint(0, 7)
#             posY = random.randint(0, 7)
#         elif aiDidHit == True:
#             posX = int(aiNextCoordinates[0])
#             posY = int(aiNextCoordinates[1])
#             print(posX, posY)
#
#         # Do not fire again at broken ships or earlier misses
#         if playerTable[posY][posX] == shipHit and aiDidHit == False:
#             continue
#         # Just one way of getting out from a loop if a ship is hit and the next tile is also a shiphit...
#         if playerTable[posY][posX] == shipHit and aiDidHit == True:
#             aiNextCoordinates = randomDirection(posX, posY)
#         if playerTable[posY][posX] == "x":
#             continue
#
#         # Fire at a ship part
#         if playerTable[posY][posX] == shipPart:
#
#             explosion(playerTable, posX, posY, hit = True)
#             aiDidHit = True
#             aiHitsInRow += 1
#             print("Ai fires at " +numToLet[posX] + str(posY)+".")
#             print("Coords before: ", posX, posY)
#             aiNextCoordinates = randomDirection(posX, posY)
#             print("Coords after: ", aiNextCoordinates)
#             input("OK")
#
#
#             input("Hit! (Press ENTER to continue.)")
#             score -=10
#             checkDamage("ai")
#
#         # Missed shot
#         else:
#             explosion(playerTable, posX, posY, hit = False)
#             print("Ai fires at " +numToLet[posX] + str(posY)+".")
#             aiDidHit = False
#             aiHitsInRow = 0
#             input("Miss! (Press ENTER to continue.)")
#         return

def aiFire():
    global difficulty
    global score
    printTable()
    if difficulty == "easy":
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
                score -=10
                explosion(playerTable, posX, posY, hit = True)
                checkDamage("player")

            # Missed shot
            else:
                explosion(playerTable, posX, posY, hit = False)
            return

    if difficulty == "impossible":
        for i in playerTable:
            for j in i:
                if j == shipPart:
                    posY = playerTable.index(i)
                    posX = i.index(shipPart)
                    explosion(playerTable, posX, posY, hit = True)
                    checkDamage("player")
                    score -=10
                    return


def randomDirection(posX, posY):
    '''Sweet artificial intelligence. Figures out where to fire next.'''
    global aiHitsInRow
    global deltaAxis
    newPosX = posX
    newPosY = posY

    while True:

        if aiHitsInRow == 1:
            selectAxis = random.randint(0,1)
            selectPolarity = random.randint(0,1)
            print("Newaxis:", selectAxis)
            print("newpolarity:",selectPolarity)

            if selectAxis == 0:
                if selectPolarity == 0:
                    newPosX -= 1
                    deltaAxis = "negativeX"
                    print("negativeX")
                elif selectPolarity == 1:
                    newPosX += 1
                    deltaAxis = "positiveX"
                    print("positiveX")
            elif selectAxis == 1:
                if selectPolarity == 0:
                    newPosY -= 1
                    deltaAxis = "negativeY"
                    print("negativeY")
                elif selectPolarity == 1:
                    newPosY += 1
                    deltaAxis = "positiveY"
                    print("positiveY")
            if newPosX < 0 or newPosX > 7 or newPosY < 0 or newPosY > 7:
                continue


        elif aiHitsInRow > 1:
            if deltaAxis == "negativeX":
                posX -= 1
            elif deltaAxis == "positiveX":
                posX += 1
            elif deltaAxis == "negativeY":
                posY -= 1
            elif deltaAxis == "positiveY":
                posY += 1

        return newPosX, newPosY



def playerPlacement():
    print("Placement phase begins!")
    print("You have five ships to place!")
    input("(Press ENTER to continue)")
    for i in playerShips:
        placeShip(i)
    print("Placement phase complete.")

def firingPhase():
    input("Starting firing phase! (Press ENTER to continue)")
    while True:
        playerFire()
        aiFire()
def setDifficulty():
    global difficulty
    os.system('cls' if os.name == 'nt' else 'clear')
    print("SET DIFFICULTY")
    diffSetting = input("\n\
    (1) Easy\n\
    (2) Normal\n\
    (3) Impossible\n\n\
    Make a selection: ")

    if diffSetting == "1":
        difficulty = "easy"
    elif diffSetting == "2":
        difficulty = "easy" #Change to NORMAL later
    elif diffSetting == "3":
        difficulty = "impossible"
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

def saveHiScore():
    """Save the current score as a tuple. High Score list contains 10 best scores. If list is longer, the lowest score is discarded"""
    high_scores = []
    global score
    global name
    global difficulty
    hiScoreExists()

    with open('hiscore.file', 'rb') as hs:
        high_scores = pickle.load(hs)

    high_scores.append((name, score, difficulty))

    high_scores = sorted(high_scores, key=itemgetter(1),reverse=True)[:10]

    with  open("hiscore.file","wb") as hiscore:
        pickle.dump(high_scores, hiscore)

def readHiScore():
    """Displays the current high scores"""
    os.system('cls' if os.name == 'nt' else 'clear')
    high_scores = []
    hiScoreExists()
    print("==================================================================================")
    print(" ██╗  ██╗██╗ ██████╗ ██╗  ██╗    ███████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗")
    print(" ██║  ██║██║██╔════╝ ██║  ██║    ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝")
    print(" ███████║██║██║  ███╗███████║    ███████╗██║     ██║   ██║██████╔╝█████╗  ███████╗")
    print(" ██╔══██║██║██║   ██║██╔══██║    ╚════██║██║     ██║   ██║██╔══██╗██╔══╝  ╚════██║")
    print(" ██║  ██║██║╚██████╔╝██║  ██║    ███████║╚██████╗╚██████╔╝██║  ██║███████╗███████║")
    print(" ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝")
    print("==================================================================================")
    rowNum = 1
    with open('hiscore.file', 'rb') as hs:
        high_scores = pickle.load(hs)

    for i in high_scores:
        name, score, difficulty = i
        print(str(rowNum)+".",name,"| Difficulty:",difficulty," | Score:",score)
        rowNum += 1
    print("==================================================================================")
    print("\n")
    input("(Press ENTER to continue)")




def mainMenu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==By=Matias=Räisänen=============================================================")
        print("  ██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ ")
        print("  ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗")
        print("  ██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝")
        print("  ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ ")
        print("  ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     ")
        print("  ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ")
        print("=========================================================================v.=0.8=")

        selection = input("\
        (1) New game\n\
        (2) Set difficulty\n\
        (3) How to play\n\
        (4) About\n\
        (5) Quit\n\n\
        Make a selection: ")

        if selection == "1":
            newGame()
        elif selection =="2":
            setDifficulty()

        elif selection == "3":
            '''How to play'''
            os.system('cls' if os.name == 'nt' else 'clear')
            print("HOW TO PLAY")
            print("")
            print("--Placement phase")
            print("Place your ships. First, set the coordinates where you want your ship's starting point to be.")
            print("Next, choose the direction to extend your ship to.")
            print("Make sure you stay withing the boundaries of the coordinates from a0 to h7.")
            print("")
            print("--Firing phase")
            print("Take turns firing with the computer.")
            print("The first one to sink each of the opponent's ships is the winner.")
            print("")
            print("--Scoring")
            print("Enemy ship hit = 100pts")
            print("Enemy ship sunk = 200pts")
            print("Player ship hit = -10pts")
            print("Player ship sunk = -50pts")
            print("")
            print("--Difficulty")
            print("The game has three difficulty settings")
            print("  1. Easy")
            print("   The computer fires at random coordinates")
            print("  2. Normal")
            print("   Default difficulty. The computer is a bit more clever. (Not yet implemented)")
            print("  3. Impossible")
            print("   The computer has radar, sonar and homing missiles.")
            print("")
            input("(Press ENTER to continue)")
            continue
        elif selection == "4":
            '''About'''
            os.system('cls' if os.name == 'nt' else 'clear')
            print("")
            print("A game of Battleship.")
            print("Made by Matias Räisänen in 2018.")
            print("Programmed in Python.")
            print("")
            input("(Press ENTER to continue)")
            continue
        elif selection == "5":
            '''Quit'''
            sys.exit()
        elif selection == "6":
            readHiScore()
        else:
            print("Invalid selection.")
            time.sleep(1)
            continue


def newGame():
    initializeGame()
    printTable()
    aiPlacement()
    playerPlacement()
    firingPhase()

if __name__ == '__main__':
    mainMenu()
