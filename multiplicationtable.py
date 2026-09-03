print("Multiplication Table")

print(
    "  |  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20"
)
print(
    "==+==================================================================================="
)

for number1 in range(0, 21):
    print(str(number1).rjust(2), end="")

    print("|", end="")

    for number2 in range(0, 21):
        print(str(number1 * number2).rjust(3), end=" ")
    print()
