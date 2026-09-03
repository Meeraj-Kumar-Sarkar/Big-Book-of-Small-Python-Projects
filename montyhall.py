import random
import sys
from importlib import reload

ALL_CLOSED = """
+------+  +------+  +------+
|      |  |      |  |      |
|   1  |  |   2  |  |   3  |
|      |  |      |  |      |
|      |  |      |  |      |
|      |  |      |  |      |
+------+  +------+  +------+"""

FIRST_GOAT = """
+------+  +------+  +------+
|  ((  |  |      |  |      |
|  oo  |  |   2  |  |   3  |
| /_/|_|  |      |  |      |
|    | |  |      |  |      |
|GOAT|||  |      |  |      |
+------+  +------+  +------+"""

SECOND_GOAT = """
+------+  +------+  +------+
|      |  |  ((  |  |      |
|   1  |  |  oo  |  |   3  |
|      |  | /_/|_|  |      |
|      |  |    | |  |      |
|      |  |GOAT|||  |      |
+------+  +------+  +------+"""

THIRD_GOAT = """
+------+  +------+  +------+
|      |  |      |  |  ((  |
|   1  |  |   2  |  |  oo  |
|      |  |      |  | /_/|_|
|      |  |      |  |    | |
|      |  |      |  |GOAT|||
+------+  +------+  +------+"""

FIRST_CAR_OTHER_GOATS = """
+------+  +------+  +------+
| CAR! |  |  ((  |  |  ((  |
|    __|  |  oo  |  |  oo  |
|  _/  |  | /_/|_|  | /_/|_|
| /_ __|  |    | |  |    | |
|   0  |  |GOAT|||  |GOAT|||
+------+  +------+  +------+"""

SECOND_CAR_OTHER_GOATS = """
+------+  +------+  +------+
|  ((  |  | CAR! |  |  ((  |
|  oo  |  |    __|  |  oo  |
| /_/|_|  |  _/  |  | /_/|_|
|    | |  | /_ __|  |    | |
|GOAT|||  |   0  |  |GOAT|||
+------+  +------+  +------+
"""

THIRD_CAR_OTHER_GOATS = """
+------+  +------+  +------+
|  ((  |  |  ((  |  | CAR! |
|  oo  |  |  oo  |  |    __|
| /_/|_|  | /_/|_|  |  _/  |
|    | |  |    | |  | /_ __|
|GOAT|||  |GOAT|||  |   0  |
+------+  +------+  +------+
"""

input("Press Enter to start...")

swapWins = 0
swapLosses = 0
stayWins = 0
stayLosses = 0
while True:
    doorThatHasCar = random.randint(1, 3)

    print(ALL_CLOSED)
    while True:
        print("""Pick a door 1, 2, or 3 (or "quit" to stop):""")
        response = input("> ").upper()
        if response == "QUIT":
            print("Thanks for playing!")
            sys.exit()

        if response == "1" or response == "2" or response == "3":
            break
    doorPick = int(response)

    while True:
        showGoatDoor = random.randint(1, 3)
        if showGoatDoor != doorPick and showGoatDoor != doorThatHasCar:
            break

    if showGoatDoor == 1:
        print(FIRST_GOAT)
    elif showGoatDoor == 2:
        print(SECOND_GOAT)
    elif showGoatDoor == 3:
        print(THIRD_GOAT)

    print(f"Door {showGoatDoor} contains a goat!")

    while True:
        print("Do you want to swap doors? Y/N")
        swap = input("> ").upper()
        if swap == "Y" or swap == "N":
            break

    if swap == "Y":
        if doorPick == 1 and showGoatDoor == 2:
            doorPick = 3
        elif doorPick == 1 and showGoatDoor == 3:
            doorPick = 2
        elif doorPick == 2 and showGoatDoor == 1:
            doorPick = 3
        elif doorPick == 2 and showGoatDoor == 3:
            doorPick = 1
        elif doorPick == 3 and showGoatDoor == 1:
            doorPick = 2
        elif doorPick == 3 and showGoatDoor == 2:
            doorPick = 1

    if doorThatHasCar == 1:
        print(FIRST_CAR_OTHER_GOATS)
    elif doorThatHasCar == 2:
        print(SECOND_CAR_OTHER_GOATS)
    elif doorThatHasCar == 3:
        print(THIRD_CAR_OTHER_GOATS)

    print(f"Door {doorThatHasCar} has the car!")

    if doorPick == doorThatHasCar:
        print("You won!")
        if swap == "Y":
            swapWins += 1
        elif swap == "N":
            stayWins += 1
    else:
        print("Sorry, you lost.")
        if swap == "Y":
            swapLosses += 1
        elif swap == "N":
            stayLosses += 1

    totalSwaps = swapWins + swapLosses
    if totalSwaps != 0:
        swapSuccess = round(swapWins / totalSwaps * 100, 1)
    else:
        swapSuccess = 0.0

    totalStays = stayWins + stayLosses
    if (stayWins + stayLosses) != 0:
        staySuccess = round(stayWins / totalStays * 100, 1)
    else:
        staySuccess = 0.0

    print()
    print("Swapping:     ", end="")
    print(f"{swapWins} wins, {swapLosses} losses,", end="")
    print(f"success rate {swapSuccess}%")
    print("Not Swapping: ", end="")
    print(f"{stayWins} wins, {stayLosses} losses,", end="")
    print(f"success rate {staySuccess}%")
    print()
    input("Press Enter to repeat the experiment...")
