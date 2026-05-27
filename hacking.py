import random, sys

GARBAGE_CHARS = "~!@#$%^&*()_+-={}[]|;:,.<>?/"

with open("sevenletterwords.txt") as wordListFile:
    WORDS = wordListFile.readlines()
for i in range(len(WORDS)):
    WORDS[i] = WORDS[i].strip().upper()


def main():
    input("Press Enter to begin...")

    gameWords = getWords()
    computerMemory = getComputerMemoryString(gameWords)
    secretPassword = random.choice(gameWords)

    print(computerMemory)

    for triesRemaining in range(4, 0, -1):
        playerMove = askForPlayerGuess(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print("A C C E S S   G R A N T E D")
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print("Access Denied ({}/7 correct)".format(numMatches))
    print("Out of tries. Secret password was {}".format(secretPassword))


def getWords():
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    for i in range(500):
        if len(words) == 5:
            break

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    for i in range(500):
        if len(words) == 12:
            break

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    while len(words) < 12:
        randomWord = getOneWordExcept(words)
        words.append(randomWord)

    assert len(words) == 12
    return words


def getOneWordExcept(blocklist=None):
    if blocklist == None:
        blocklist = []

    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def numMatchingLetters(word1, word2):
    matches = 0

    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def getComputerMemoryString(words):
    linesWithWords = random.sample(range(16 * 2), len(words))

    memoryAddress = 16 * random.randint(0, 4000)

    computerMemory = []
    nextWord = 0
    for lineNum in range(16):
        leftHalf = ""
        rightHalf = ""
        for j in range(16):
            leftHalf += random.choice(GARBAGE_CHARS)
            rightHalf += random.choice(GARBAGE_CHARS)

        if lineNum in linesWithWords:
            insertionIndex = random.randint(0, 9)

            leftHalf = (
                leftHalf[:insertionIndex]
                + words[nextWord]
                + leftHalf[insertionIndex + 7 :]
            )
            nextWord += 1

        if lineNum + 16 in linesWithWords:
            insertionIndex = random.randint(0, 9)

            rightHalf = (
                rightHalf[:insertionIndex]
                + words[nextWord]
                + rightHalf[insertionIndex + 7 :]
            )
            nextWord += 1

        computerMemory.append(
            "0x"
            + hex(memoryAddress)[2:].zfill(4)
            + " "
            + leftHalf
            + "   "
            + "0x"
            + hex(memoryAddress + (16 * 16))[2:].zfill(4)
            + "  "
            + rightHalf
        )
        memoryAddress += 16

    return "\n".join(computerMemory)


def askForPlayerGuess(words, tries):
    while True:
        print("Enter password: ({} tries remaining)".format(tries))
        guess = input("> ").upper()
        if guess in words:
            return guess
        print("That is not one of the possible passwords listed above.")
        print("""Try entering "{}" or "{}".""".format(words[0], words[1]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
