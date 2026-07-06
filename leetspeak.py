import random

try:
    import pyperclip
except ImportError:
    pass


def main():
    print("""L3375P34]< (leetspeak)
          
          Enter your leet message:""")
    english = input("> ")
    print()
    leetspeak = englishToLeetspeak(english)
    print(leetspeak)

    try:
        pyperclip.copy(leetspeak)
        print("(Copied leetspeak to clipboard.)")
    except NameError:
        pass


def englishToLeetspeak(message):
    charMapping = {
        "a": ["4", "@", "/-\\"],
        "c": ["("],
        "d": ["|)"],
        "e": ["3"],
        "f": ["ph"],
        "h": ["]-[", "|-|"],
        "i": ["1", "!", "|"],
        "k": ["]<"],
        "o": ["O"],
        "s": ["$", "5"],
        "t": ["7", "+"],
        "u": ["|_|"],
        "v": ["\\/"],
    }

    leetspeak = ""

    for char in message:
        if char.lower() in charMapping and random.random() <= 0.70:
            possibleLeetReplacements = charMapping[char.lower()]
            leetReplacement = random.choice(possibleLeetReplacements)
            leetspeak += leetReplacement
        else:
            leetspeak += char

    return leetspeak


if __name__ == "__main__":
    main()
