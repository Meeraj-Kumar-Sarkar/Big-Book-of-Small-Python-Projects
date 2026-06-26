import time, random, sys

SUSPECTS = [
    "DUKE HAUTDOG",
    "MAXIMUM POWERS",
    "BILL MONOPOLIS",
    "SENATOR SCHMEAR",
    "MRS. FEATHERTOSS",
    "DR. JEAN SPLICER",
    "RAFFLES THE CLOWN",
    "ESPRESSA TOFFEEPOT",
    "CECIL EDGAR VANDERTON",
]
ITEMS = [
    "FLASHLIGHT",
    "CANDLESTICK",
    "RAINBOW FLAG",
    "HAMSTER WHEEL",
    "ANIME VHS TAPE",
    "JAAR OF PICKLES",
    "ANE COWBOY BOOT",
    "CLEAN UNDERPANT",
    "5 DOLLAR GIFT CARD",
]
PLACES = [
    "ZOO",
    "OLD BARN",
    "DUCK POND",
    "CITY HALL",
    "HIPSTER CAFE",
    "BOWLING ALLEY",
    "VIDEO GAME MUSEUM",
    "UNIVERSITY LIBRARY",
    "ALBINO ALLIGATOR PIT",
]
TIME_TO_SOLVE = 300

PLACE_FIRST_LETTERS = {}
LONGEST_PLACE_NAME_LENGTH = 0
for place in PLACES:
    PLACE_FIRST_LETTERS[place[0]] = place
    if len(place) > LONGEST_PLACE_NAME_LENGTH:
        LONGEST_PLACE_NAME_LENGTH = len(place)

assert len(SUSPECTS) == 9
assert len(ITEMS) == 9
assert len(PLACES) == 9
assert len(PLACE_FIRST_LETTERS.keys()) == len(PLACES)

knownSuspectsAndItems = []
visitedPlaces = {}
currentLocation = "TAXI"
accusedSuspects = []
liars = random.sample(SUSPECTS, random.randint(3, 4))
accusationsLeft = 3
culprit = random.choice(SUSPECTS)

# Fix: compute culprit index for later
culpritIndex = SUSPECTS.index(culprit)

random.shuffle(SUSPECTS)
random.shuffle(ITEMS)
random.shuffle(PLACES)

clues = {}
for i, interviewee in enumerate(SUSPECTS):
    if interviewee in liars:
        continue
    clues[interviewee] = {}
    clues[interviewee]["debug_liar"] = False
    for item in ITEMS:
        if random.randint(0, 1) == 0:
            clues[interviewee][item] = PLACES[ITEMS.index(item)]
        else:
            clues[interviewee][item] = SUSPECTS[ITEMS.index(item)]
    for suspect in SUSPECTS:
        if random.randint(0, 1) == 0:
            clues[interviewee][suspect] = PLACES[SUSPECTS.index(suspect)]
        else:
            clues[interviewee][suspect] = ITEMS[SUSPECTS.index(suspect)]

for i, interviewee in enumerate(SUSPECTS):
    if interviewee not in liars:
        continue
    clues[interviewee] = {}
    clues[interviewee]["debug_liar"] = True
    for item in ITEMS:
        if random.randint(0, 1) == 0:
            while True:
                clues[interviewee][item] = random.choice(PLACES)
                if clues[interviewee][item] != PLACES[ITEMS.index(item)]:
                    break
        else:
            while True:
                clues[interviewee][item] = random.choice(SUSPECTS)
                if clues[interviewee][item] != SUSPECTS[ITEMS.index(item)]:
                    break
    for suspect in SUSPECTS:
        if random.randint(0, 1) == 0:
            while True:
                clues[interviewee][suspect] = random.choice(PLACES)
                # Fix: use the suspect's correct place, not a stale 'item'
                if clues[interviewee][suspect] != PLACES[SUSPECTS.index(suspect)]:
                    break
        else:
            while True:
                clues[interviewee][suspect] = random.choice(ITEMS)
                if clues[interviewee][suspect] != ITEMS[SUSPECTS.index(suspect)]:
                    break

zophieClues = {}
for interviewee in random.sample(SUSPECTS, random.randint(3, 4)):
    kindOfClue = random.randint(1, 3)
    if kindOfClue == 1:
        if interviewee not in liars:
            # Truthful: reveal a random suspect (could be culprit)
            zophieClues[interviewee] = random.choice(SUSPECTS)
        else:
            # Liar: give any suspect except the culprit
            while True:
                zophieClues[interviewee] = random.choice(SUSPECTS)
                if zophieClues[interviewee] != culprit:
                    break
    elif kindOfClue == 2:
        if interviewee not in liars:
            # Fix: use culprit, not an undefined 'item'
            zophieClues[interviewee] = PLACES[culpritIndex]
        else:
            while True:
                zophieClues[interviewee] = random.choice(PLACES)
                if zophieClues[interviewee] != PLACES[culpritIndex]:
                    break
    elif kindOfClue == 3:
        if interviewee not in liars:
            zophieClues[interviewee] = ITEMS[culpritIndex]
        else:
            while True:
                zophieClues[interviewee] = random.choice(ITEMS)
                if zophieClues[interviewee] != ITEMS[culpritIndex]:
                    break

startTime = time.time()
endTime = startTime + TIME_TO_SOLVE
print(
    "{} was at the {} with the {} who catnapped ZOPHIE THE CAT!".format(
        culprit, PLACES[culpritIndex], ITEMS[culpritIndex]
    )
)

while True:
    # Check game-over conditions
    if time.time() > endTime or accusationsLeft == 0:
        if time.time() > endTime:
            print("You have run out of time!")
        elif accusationsLeft == 0:
            print("You have accused too many innocent people!")
        culpritIndex = SUSPECTS.index(culprit)
        print(
            "It was {} at the {} with the {} who catnapped her!".format(
                culprit, PLACES[culpritIndex], ITEMS[culpritIndex]
            )
        )
        print("Better luck next time, Detective.")
        sys.exit()

    print()
    minutesLeft = int(endTime - time.time()) // 60
    secondsLeft = int(endTime - time.time()) % 60
    print("Time left: {} min, {} sec".format(minutesLeft, secondsLeft))

    # TAXI mode: only travel
    if currentLocation == "TAXI":
        print("  You are in your TAXI. Where do you want to go?")
        for place in sorted(PLACES):
            placeInfo = ""
            if place in visitedPlaces:
                placeInfo = visitedPlaces[place]
            nameLabel = "(" + place[0] + ")" + place[1:]
            spacing = " " * (LONGEST_PLACE_NAME_LENGTH - len(place))
            print("{} {}{}".format(nameLabel, spacing, placeInfo))
        print("(Q)UIT GAME")
        while True:
            response = input("> ").upper()
            if response == "":
                continue
            if response == "Q":
                print("Thanks for playing!")
                sys.exit()
            if response in PLACE_FIRST_LETTERS.keys():
                break
        currentLocation = PLACE_FIRST_LETTERS[response]
        continue

    # Interview mode at a location
    print("  You are at the {}.".format(currentLocation))
    currentLocationIndex = PLACES.index(currentLocation)
    thePersonHere = SUSPECTS[currentLocationIndex]
    theItemHere = ITEMS[currentLocationIndex]
    print("  {} with the {} is here.".format(thePersonHere, theItemHere))

    # Remember this person and item
    if thePersonHere not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(thePersonHere)
    if theItemHere not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(theItemHere)
    if currentLocation not in visitedPlaces:
        visitedPlaces[currentLocation] = "({}, {})".format(
            thePersonHere.lower(), theItemHere.lower()
        )

    # If this person has already been accused, refuse to help
    if thePersonHere in accusedSuspects:
        print("They are offended that you accused them,")
        print("and will not help with your investigation.")
        print("You go back to your TAXI.")
        print()
        input("Press Enter to continue...")
        currentLocation = "TAXI"
        continue

    print()
    print('(J) "J\'ACCUSE!" ({} accusations left)'.format(accusationsLeft))
    print("(Z) Ask if they know where ZOPHIE THE CAT is.")
    print("(T) Go back to the TAXI.")
    for i, suspectOrItem in enumerate(knownSuspectsAndItems):
        print("({}) Ask about {}".format(i + 1, suspectOrItem))

    # Get valid command
    while True:
        response = input("> ").upper()
        if response in "JZT" or (
            response.isdecimal() and 0 < int(response) <= len(knownSuspectsAndItems)
        ):
            break

    # --- Accuse ---------------------------------------------------------------
    if response == "J":
        # Choose suspect
        print("\nAccuse which suspect?")
        for i, s in enumerate(SUSPECTS):
            print("  ({}) {}".format(i + 1, s))
        while True:
            choice = input("Enter number: ").strip()
            if choice.isdecimal() and 1 <= int(choice) <= 9:
                accused = SUSPECTS[int(choice) - 1]
                break

        # Choose item
        print("\nWith what item?")
        for i, it in enumerate(ITEMS):
            print("  ({}) {}".format(i + 1, it))
        while True:
            choice = input("Enter number: ").strip()
            if choice.isdecimal() and 1 <= int(choice) <= 9:
                itemAccused = ITEMS[int(choice) - 1]
                break

        # Choose place
        print("\nAt what place?")
        for i, pl in enumerate(PLACES):
            print("  ({}) {}".format(i + 1, pl))
        while True:
            choice = input("Enter number: ").strip()
            if choice.isdecimal() and 1 <= int(choice) <= 9:
                placeAccused = PLACES[int(choice) - 1]
                break

        # Check accusation
        if (
            accused == culprit
            and itemAccused == ITEMS[culpritIndex]
            and placeAccused == PLACES[culpritIndex]
        ):
            print("You have cracked the case!")
            print(
                "{} was at the {} with the {} who catnapped ZOPHIE THE CAT!".format(
                    culprit, PLACES[culpritIndex], ITEMS[culpritIndex]
                )
            )
            print("Congratulations, Detective!")
            sys.exit()
        else:
            accusationsLeft -= 1
            print("That is incorrect.")
            accusedSuspects.append(accused)
            print("You have {} accusation(s) left.".format(accusationsLeft))
            input("Press Enter to continue...")
            currentLocation = "TAXI"
            continue

    # --- Ask about Zophie ----------------------------------------------------
    elif response == "Z":
        if thePersonHere in zophieClues:
            clue = zophieClues[thePersonHere]
            # Determine what type of clue it is (suspect/place/item)
            if clue in SUSPECTS:
                print('  "I think Zophie is with {}."'.format(clue))
            elif clue in PLACES:
                print('  "I saw her near the {}."'.format(clue))
            elif clue in ITEMS:
                print('  "She was playing with the {}."'.format(clue))
        else:
            print('  "I have no idea where that cat is."')
        input("Press Enter to continue...")
        currentLocation = "TAXI"

    # --- Return to taxi ------------------------------------------------------
    elif response == "T":
        currentLocation = "TAXI"

    # --- Ask about a known suspect or item -----------------------------------
    else:
        idx = int(response) - 1
        askedAbout = knownSuspectsAndItems[idx]

        # Retrieve the clue from the current interviewee
        clue = clues[thePersonHere].get(askedAbout, None)

        if clue is None:
            print('  "I don\'t know anything about that."')
        else:
            # Format the clue depending on what we asked and what the value is
            if askedAbout in SUSPECTS:
                if clue in PLACES:
                    print('  "{} is at the {}."'.format(askedAbout, clue))
                elif clue in ITEMS:
                    print('  "{} has the {}."'.format(askedAbout, clue))
                else:
                    print('  "{} is with {}."'.format(askedAbout, clue))  # fallback
            else:  # askedAbout is an item
                if clue in PLACES:
                    print('  "The {} is at the {}."'.format(askedAbout, clue))
                elif clue in SUSPECTS:
                    print('  "{} has the {}."'.format(clue, askedAbout))
                else:
                    print('  "The {} is with {}."'.format(askedAbout, clue))  # fallback

        # Stay at the location to ask more questions (loop repeats)
        input("Press Enter to continue...")
