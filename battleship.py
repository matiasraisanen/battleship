import os
import time
import sys
import random

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

letToNum = {
    'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9
}

numToLet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

shipPart = "■"
shipHit = "□"

playerShips = [
{'id': 'playerShip1', 'name':'battleship', 'model': '■ ■ ■ ■', 'length': 4, 'damage': 0, 'coords':[]},
{'id': 'playerShip2', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
{'id': 'playerShip3', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
{'id': 'playerShip4', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
{'id': 'playerShip5', 'name':'patrol boat', 'model': '■ ■', 'length': 2, 'damage': 0, 'coords':[]},
]

aiShips = [
{'id': 'aiShip1', 'name':'battleship', 'model': '■ ■ ■ ■', 'length': 4, 'damage': 0, 'coords':[]},
{'id': 'aiShip2', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
{'id': 'aiShip3', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
{'id': 'aiShip4', 'name':'cruiser', 'model': '■ ■ ■', 'length': 3, 'damage': 0, 'coords':[]},
{'id': 'aiShip5', 'name':'patrol boat', 'model': '■ ■', 'length': 2, 'damage': 0, 'coords':[]}
]

def printTable():
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
                j = "■" #Change this to "." when done
            print(" "+j, end='', flush=True)
        print("#")
        rownum += 1
    print("##################   ##################")
    print("■ = Ship section: intact")
    print("□ = Ship section: destroyed")
    print("x = Missed shot")
    print(". = Open sea")
    print("")


def checkShip(posX, posY, shipNum, direction, who):
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
    totalHealth = 0
    totalDamage = 0
    if who == "player":
        table = playerShips
    elif who == "ai":
        table = aiShips

    for i in table:
        totalHealth = totalHealth + i['length']
        totalDamage = totalDamage + i['damage']
    if totalHealth == totalHealth:
        endGame(who)

def endGame(who):
    if who == "player":
        input("AI wins!")
    elif who == "ai":
        input("Player wins!")
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
                input("Invalid direction (Press ENTER)")
                continue

            if direction == "r" and (startPosX + shipNum['length']) > 8:
                input("Does not fit: Out of bounds (Press ENTER)")
                continue
            if direction == "d" and (startPosY + shipNum['length']) > 8:
                input("Does not fit: Out of bounds (Press ENTER)")
                continue

            # Check for collisions
            if checkShip(startPosX, startPosY, shipNum, direction, "player") == True:
                input("Does not fit: Collides with another ship. (Press ENTER)")
                continue

            # Place the ship part
            for i in range(shipNum['length']):
                if direction == "r":
                    drawShipPart(startPosX, startPosY)
                    startPosX += 1
                elif direction == "d":
                    drawShipPart(startPosX, startPosY)
                    startPosY += 1
            return
        except IndexError:
            input("Invalid coordinates (Press ENTER)")
        except KeyError:
            input("Invalid coordinates (Press ENTER)")
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
    # for i in aiShips:
    #     aiPlaceShip(i)
    aiPlaceShip(aiShips[0])
    printTable()

def aiDrawShipPart(posX, posY):
    aiTable[posY][posX] = shipPart

def drawShipPart(posX, posY):
    playerTable[posY][posX] = shipPart
    printTable()

def explosion(table, posX, posY, hit = False):
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
        for i in aiShips:
            if str(posX)+str(posY) in i['coords']:
                i['damage'] += 1
                if i['length'] == i['damage']:
                    print("Ship Destroyed! You sunk the " +i['name']+".")
                    input("(Press ENTER)")
                    checkDamage("ai")
    else:
        if table[posY][posX] == shipHit:
            pass
        else:
            print(table[posY][posX])
            table[posY][posX] = "x"
        printTable()


def playerFire():
    while True:
        try:
            printTable()
            coords = input("Enter coordinates to fire at: ")
            posX = letToNum[coords[0].lower()]
            posY = int(coords[1])

            if aiTable[posY][posX] == shipPart:
                explosion(aiTable, posX, posY, hit = True)
                input("Hit! (Press ENTER to continue.)")


            else:
                explosion(aiTable, posX, posY, hit = False)
                input("Miss! (Press ENTER to continue.)")

            break
        except IndexError:
            input("Give proper coordinates! Range: a0 to h7 (Press ENTER)")

def aiFire():
    printTable()
    posX = random.randint(0, 7)
    posY = random.randint(0, 7)

    if playerTable[posY][posX] == shipPart:

        explosion(playerTable, posX, posY, hit = True)
        print("Ai fires at " +numToLet[posX] + str(posY)+".")
        input("Hit! (Press ENTER to continue.)")

    else:
        explosion(playerTable, posX, posY, hit = False)
        print("Ai fires at " +numToLet[posX] + str(posY)+".")
        input("Miss! (Press ENTER to continue.)")

def playerPlacement():
    input("Placement phase begins! (Press ENTER to continue)")
    for i in playerShips:
        placeShip(i)
    print("Placement phase complete.")

def firingPhase():
    input("Starting firing phase! (Press ENTER to continue)")
    while True:
        playerFire()
        aiFire()

def mainMenu():
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
    (2) How to play\n\
    (3) About\n\
    (4) Quit\n\
    Make a selection: ")

    if selection == "1":
        newGame()
    elif selection == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("--Placement phase")
        print("Place your ships. First, set the coordinates where you want your ship's stern to be.")
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
        input("(Press ENTER to continue)")
        mainMenu()
    elif selection == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("A game of Battleship.")
        print("Made by Matias Räisänen in 2018.")
        print("Programmed in Python.")
        print("")
        input("(Press ENTER to continue)")
        mainMenu()
    elif selection == "4":
        sys.exit()
    else:
        print("Invalid selection.")
        time.sleep(1)
        mainMenu()


def newGame():
        printTable()
        aiPlacement()
        playerPlacement()
        firingPhase()

if __name__ == '__main__':
    mainMenu()