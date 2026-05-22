import random


def askForGuess():
    while True:
        guess = input("> ")
        if guess.isdecimal():
            return int(guess)
        print("Please enter an Integer")


secretNumber = random.randint(1, 100)
print(
    "You got 3 chances to determine the value of the random number generated on between 1 to 100"
)
for i in range(3):
    guess = askForGuess()
    if secretNumber == guess:
        break
    else:
        print("Hint:")
        error = abs(guess - secretNumber)
        miss_pct = (error / secretNumber) * 100
        print("You miss the mark by {:.2f}%".format(miss_pct))

if secretNumber == guess:
    print("You did it")
else:
    print(f"Better luck next time. The number was {secretNumber}.")
