import re


def matching_letters(word1, word2):
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def filter_words(words, guess, match_count):
    possible = []

    for word in words:
        if matching_letters(word, guess) == match_count:
            possible.append(word)

    return possible


def extract_words(memory_text):
    # Extract all 7-letter uppercase words
    return list(set(re.findall(r"\b[A-Z]{7}\b", memory_text)))


print("Paste the game screen below.")
print("When finished, type END on a new line.\n")

lines = []

while True:
    line = input()
    if line == "END":
        break
    lines.append(line)

memory_dump = "\n".join(lines)

words = extract_words(memory_dump)

print("\nPossible words found:")
for word in words:
    print(word)

while len(words) > 1:
    guess = input("\nEnter the word you guessed in game: ").upper()
    matches = int(input("How many letters matched? "))

    words = filter_words(words, guess, matches)

    print("\nRemaining possible passwords:")
    for word in words:
        print(word)

    if len(words) == 1:
        print("\nPASSWORD FOUND:", words[0])
        break

if len(words) == 0:
    print("\nNo possible passwords remain.")
