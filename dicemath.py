import random, time, sys

DICE_WIDTH = 9
DICE_HEIGHT = 5
CANVAS_WIDTH = 79
CANVAS_HEIGHT = 24 - 3

QUIZ_DURATION = 30
MIN_DICE = 2
MAX_DICE = 6

REWARD = 4
PENALTY = 1

assert MAX_DICE <= 14

D1 = (["+-------+", "|       |", "|   O   |", "|       |", "+-------+"], 1)

D2a = (["+-------+", "| O     |", "|       |", "|     O |", "+-------+"], 2)

D2b = (["+-------+", "|     O |", "|       |", "| O     |", "+-------+"], 2)

D3a = (["+-------+", "| O     |", "|   O   |", "|     O |", "+-------+"], 3)

D3b = (["+-------+", "|     O |", "|   O   |", "| O     |", "+-------+"], 3)

D4 = (["+-------+", "| O   O |", "|       |", "| O   O |", "+-------+"], 4)

D5 = (["+-------+", "| O   O |", "|   O   |", "| O   O |", "+-------+"], 5)

D6a = (["+-------+", "| O   O |", "| O   O |", "| O   O |", "+-------+"], 6)

D6b = (["+-------+", "| O O O |", "|       |", "| O O O |", "+-------+"], 6)

ALL_DICE = [D1, D2a, D2b, D3a, D3b, D4, D5, D6a, D6b]

print(
    """Dice Math
      
Add up the sides of all the dice displayed on the screen. You have
{} seconds to answer as many as possible. You get {} points for each
correct answer and lose {} point for each incorrect answer.""".format(
        QUIZ_DURATION, REWARD, PENALTY
    )
)
try:
    input("Press Enter to begin...")

    correctAnswers = 0
    incorrectAnswers = 0
    startTime = time.time()

    while time.time() < startTime + QUIZ_DURATION:
        sumAnswer = 0
        diceFaces = []

        for _ in range(random.randint(MIN_DICE, MAX_DICE)):
            die = random.choice(ALL_DICE)
            diceFaces.append(die[0])
            sumAnswer += die[1]

        topLeftDiceCorners = []

        for _ in range(len(diceFaces)):
            while True:
                left = random.randint(0, CANVAS_WIDTH - DICE_WIDTH)
                top = random.randint(0, CANVAS_HEIGHT - DICE_HEIGHT)

                new_left = left
                new_right = left + DICE_WIDTH
                new_top = top
                new_bottom = top + DICE_HEIGHT

                overlaps = False
                for prev_left, prev_top in topLeftDiceCorners:
                    prev_right = prev_left + DICE_WIDTH
                    prev_bottom = prev_top + DICE_HEIGHT

                    if not (
                        new_right <= prev_left
                        or new_left >= prev_right
                        or new_bottom <= prev_top
                        or new_top >= prev_bottom
                    ):
                        overlaps = True
                        break

                if not overlaps:
                    topLeftDiceCorners.append((left, top))
                    break

        canvas = {}

        for i, (dieLeft, dieTop) in enumerate(topLeftDiceCorners):
            dieFace = diceFaces[i]
            for dy in range(DICE_HEIGHT):
                for dx in range(DICE_WIDTH):
                    canvasX = dieLeft + dx
                    canvasY = dieTop + dy
                    canvas[(canvasX, canvasY)] = dieFace[dy][dx]

        for cy in range(CANVAS_HEIGHT):
            for cx in range(CANVAS_WIDTH):
                print(canvas.get((cx, cy), " "), end="")
            print()

        response = input("Enter the sum: ").strip()

        if response.isdecimal() and int(response) == sumAnswer:
            correctAnswers += 1
        else:
            print("Incorrect, the answer is", sumAnswer)
            time.sleep(2)
            incorrectAnswers += 1

    score = (correctAnswers * REWARD) - (incorrectAnswers * PENALTY)

    print("Correct:", correctAnswers)
    print("Incorrect:", incorrectAnswers)
    print("Score:", score)
except KeyboardInterrupt:
    print("Execution terminated!")
    sys.exit()
