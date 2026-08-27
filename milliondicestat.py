import random
import time

print("Milloin Dice Roll Statistics Simulator")
print("Enter how many six-sided dice you want to roll:")
numberOfDice = int(input("> "))

results = {}
for i in range(numberOfDice, (numberOfDice * 6) + 1):
    results[i] = 0

print(f"Simulating 1,000,000 rolls of {numberOfDice} dice...")
lastPrintTime = time.time()
for i in range(1000000):
    if time.time() > lastPrintTime + 1:
        print(f"{round(i / 10000, 1)}% done...")
        lastPrintTime = time.time()
    total = 0
    for j in range(numberOfDice):
        total += random.randint(1, 6)
    results[total] = results[total] + 1

print("TOTAL - ROLLS - PERCENTAGE")
for i in range(numberOfDice, (numberOfDice * 6) + 1):
    roll = results[i]
    percentage = round(results[i] / 10000, 1)
    print(f"  {i} - {roll} rolls - {percentage}%")
