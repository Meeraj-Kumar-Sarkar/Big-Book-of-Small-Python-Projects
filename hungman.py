import random, sys

HANGMAN_PICS = [
    r"""
                +--+
                |  |
                   |
                   |
                   |
                   |
               =====""",
    r"""
                +--+
                |  |
                0  |
                   |
                   |
                   |
               =====""",
    r"""
                +--+
                |  |
                0  |
                |  |
                   |
                   |
               =====""",
    r"""
                +--+
                |  |
                0  |
               /|  |
                   |
                   |
               =====""",
    r"""
                +--+
                |  |
                0  |
               /|\ |
                   |
                   |
               =====""",
    r"""
                +--+
                |  |
                0  |
               /|\ |
               /   |
                   |
               =====""",
    r"""
                +--+
                |  |
                0  |
               /|\ |
               / \ |
                   |
               =====""",
]

CATEGORY = "Animals"
WORDS = "ANT BABOON BADGER BAT BEAR BEAVER CAMEL CAT CLAM COBRA COUGAR COYOTEE CROW DEEP DOG DONKEY DUCK EAGLE FERRET FOX FROG GOAT GOOSE HAWK LION LIZARD LLAMA MOLE MONKEYMOOSE MOUSE MULE NEWT OTTER OWL PANDA PARROT PIGEON PYTHON RABBIT RAM RAT RAVEN RHINO SALMON SEAL SHARK SHEEP SKUNK SLOTH SNAKE SPIDER STORK SWAN TIGER TOAD TROUT TURKEY TRUTLE WEASEL WHALE WOLF WOMBAT ZEBRA".split()


def main():
    missedLetters = []
    correctLetters = []
    secretWord = random.choice(WORDS)

    while True:
        drawHungman(missedLetters, correctLetters, secretWord)

        guess = getPlayerGuess(missedLetters + correctLetters)

        if guess in secretWord:
            correctLetters.append(guess)

            foundAllLetters = True
            for secretWordLetter in secretWord:
                if secretWordLetter not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print("Yes! The secret word is:", secretWord)
                print("You have won!")
                break

        else:
            missedLetters.append(guess)

            if len(missedLetters) == len(HANGMAN_PICS) - 1:
                drawHungman(missedLetters, correctLetters, secretWord)
                print("You have run out of guesses!")
                print('The word was "{}"'.format(secretWord))
                break


def drawHungman(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[(len(missedLetters))])
    print("The category is:", CATEGORY)
    print()

    print("Missed letters: ", end="")
    for letter in missedLetters:
        print(letter, end=" ")
    if len(missedLetters) == 0:
        print("No missed letters yet.")
    print()

    blanks = ["_"] * len(secretWord)

    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks[i] = secretWord[i]

    print(" ".join(blanks))


def getPlayerGuess(alreadyGuessed):
    while True:
        print("Guess a letter.")
        guess = input("> ").upper()
        if len(guess) != 1:
            print("Please enter a single letter.")
        elif guess in alreadyGuessed:
            print("You have already guesses that letter, Choose again.")
        elif not guess.isalpha():
            print("Please enter a LETTER.")
        else:
            return guess


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
