import copy, random, sys, time

WIDTH = 79
HEIGHT = 20
ALIVE = "O"
DEAD = " "

nextCells = {}

# Initial random grid
for x in range(WIDTH):
    for y in range(HEIGHT):
        nextCells[(x, y)] = ALIVE if random.randint(0, 1) == 0 else DEAD

while True:
    print("\n" * 50)
    cells = copy.deepcopy(nextCells)

    # Draw current generation
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(cells[(x, y)], end=" ")
        print()
    print("Press Ctrl-C to quit")

    # Compute next generation
    for x in range(WIDTH):
        for y in range(HEIGHT):
            left = (x - 1) % WIDTH
            right = (x + 1) % WIDTH
            above = (y - 1) % HEIGHT
            below = (y + 1) % HEIGHT

            # Count live neighbors
            numNeighbors = 0
            if cells[(left, above)] == ALIVE:
                numNeighbors += 1
            if cells[(x, above)] == ALIVE:
                numNeighbors += 1
            if cells[(right, above)] == ALIVE:
                numNeighbors += 1
            if cells[(left, y)] == ALIVE:
                numNeighbors += 1
            if cells[(right, y)] == ALIVE:
                numNeighbors += 1
            if cells[(left, below)] == ALIVE:
                numNeighbors += 1
            if cells[(x, below)] == ALIVE:
                numNeighbors += 1
            if cells[(right, below)] == ALIVE:
                numNeighbors += 1

            # Apply Conway's rules
            if cells[(x, y)] == ALIVE:
                if numNeighbors == 2 or numNeighbors == 3:
                    nextCells[(x, y)] = ALIVE
                else:
                    nextCells[(x, y)] = DEAD
            else:  # dead cell
                if numNeighbors == 3:
                    nextCells[(x, y)] = ALIVE
                else:
                    nextCells[(x, y)] = DEAD

    try:
        time.sleep(0.01)  # faster animation
    except KeyboardInterrupt:
        print("GAME OF LIFE")
        sys.exit()
