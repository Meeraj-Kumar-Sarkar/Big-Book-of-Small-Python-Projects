import random, shutil, sys, time

PAUSE = 0.2
DENSITY = 0.10

DUCKLING_WIDTH = 5
LEFT = "left"
RIGHT = "right"
BEADY = "beady"
WIDE = "wide"
HAPPY = "happy"
ALOOF = "aloof"
CHUBBY = "chubby"
VERY_CHUBBY = "very chubby"
OPEN = "open"
CLOSE = "close"
OUT = "out"
DOWN = "down"
UP = "up"
HEAD = "head"
BODY = "body"
FEET = "feet"

WIDTH = shutil.get_terminal_size()[0]
WIDTH -= 1


def main():
    print("Duckling Screensaver")
    print("Press Ctrl-C to quit...")
    time.sleep(2)

    ducklingLanes = [None] * (WIDTH // DUCKLING_WIDTH)

    while True:
        for laneNum, ducklingObj in enumerate(ducklingLanes):
            if ducklingObj is None and random.random() <= DENSITY:
                ducklingObj = Duckling()
                ducklingLanes[laneNum] = ducklingObj

            if ducklingObj is not None:
                part = ducklingObj.getNextBodyPart()
                if part is None:
                    ducklingLanes[laneNum] = None
                    print(" " * DUCKLING_WIDTH, end="")
                else:
                    print(part, end="")
            else:
                print(" " * DUCKLING_WIDTH, end="")

        print()
        sys.stdout.flush()
        time.sleep(PAUSE)


class Duckling:
    def __init__(self):
        self.direction = random.choice([LEFT, RIGHT])
        self.body = random.choice([CHUBBY, VERY_CHUBBY])
        self.mouth = random.choice([OPEN, CLOSE])
        self.wing = random.choice([OUT, UP, DOWN])

        if self.body == CHUBBY:
            self.eyes = BEADY
        else:
            self.eyes = random.choice([BEADY, WIDE, HAPPY, ALOOF])

        self.partToDisplayNext = HEAD

    def getHeadStr(self):
        # Determine eyes string based on type
        if self.eyes == BEADY:
            if self.body == CHUBBY:
                eyes_str = '"'  # 1 char
            else:  # VERY_CHUBBY
                eyes_str = '" '  # 2 chars
        elif self.eyes == WIDE:
            eyes_str = "''"  # 2 chars
        elif self.eyes == HAPPY:
            eyes_str = "^^"  # 2 chars
        elif self.eyes == ALOOF:
            eyes_str = "``"  # 2 chars
        else:
            eyes_str = "  "  # fallback (shouldn't happen)

        # Build head exactly 5 characters wide for either direction
        if self.direction == LEFT:
            mouth_char = ">" if self.mouth == OPEN else "="
            # Template: mouth(1) + eyes + ")" + padding to 5
            headStr = mouth_char + eyes_str + ")"
            # Pad with spaces to make length 5
            headStr = headStr.ljust(DUCKLING_WIDTH)
        else:  # RIGHT
            mouth_char = "<" if self.mouth == OPEN else "="
            # Template: "(" + eyes + mouth(1) + padding
            headStr = "(" + eyes_str + mouth_char
            headStr = headStr.ljust(DUCKLING_WIDTH)

        return headStr

    def getBodyStr(self):
        bodyStr = "("
        if self.direction == LEFT:
            if self.body == CHUBBY:
                bodyStr += " "
            elif self.body == VERY_CHUBBY:
                bodyStr += "  "

            if self.wing == OUT:
                bodyStr += ">"
            elif self.wing == UP:
                bodyStr += "^"
            elif self.wing == DOWN:
                bodyStr += "v"

        if self.direction == RIGHT:
            if self.wing == OUT:
                bodyStr += ">"
            elif self.wing == UP:
                bodyStr += "^"
            elif self.wing == DOWN:
                bodyStr += "v"

            if self.body == CHUBBY:
                bodyStr += " "
            elif self.body == VERY_CHUBBY:
                bodyStr += "  "

        bodyStr += ")"

        if self.body == CHUBBY:
            bodyStr += " "

        return bodyStr

    def getFeetStr(self):
        # Ensure exactly 5 characters
        if self.body == CHUBBY:
            return " ^^  "  # was " ^^ " (only 4 chars)
        elif self.body == VERY_CHUBBY:
            return " ^ ^ "
        return "     "  # fallback

    def getNextBodyPart(self):
        if self.partToDisplayNext == HEAD:
            self.partToDisplayNext = BODY
            return self.getHeadStr()
        elif self.partToDisplayNext == BODY:
            self.partToDisplayNext = FEET
            return self.getBodyStr()
        elif self.partToDisplayNext == FEET:
            self.partToDisplayNext = None
            return self.getFeetStr()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
