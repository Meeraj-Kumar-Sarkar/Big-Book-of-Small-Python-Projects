import random, shutil, sys, time

MIN_STREAM_LENGTH = 6
MAX_STREAM_LENGTH = 14
PAUSE = 0.035
ALPHA = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
NUMS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SPECIALS = [
    "<",
    ">",
    "[",
    "]",
    "{",
    "}",
    "(",
    ")",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "-",
    "+",
    "/",
    "_",
    "|",
    "'",
]
STREAM_CHARS = ALPHA + NUMS + SPECIALS

DENSITY = 0.025

WIDTH = shutil.get_terminal_size()[0]

WIDTH -= 1

print("Press Ctrl-C to quit.")
time.sleep(2)

try:
    columns = [0] * WIDTH
    sys.stdout.flush()
    while True:
        for i in range(WIDTH):
            if columns[i] <= 0:
                if random.random() <= DENSITY:
                    columns[i] = random.randint(MIN_STREAM_LENGTH, MAX_STREAM_LENGTH)

            if columns[i] > 0:
                print(random.choice(STREAM_CHARS), end="")
                columns[i] -= 1
            else:
                print(" ", end="")
        print()
        sys.stdout.flush()
        time.sleep(PAUSE)
except KeyboardInterrupt:
    sys.exit()
