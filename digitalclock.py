import sys, time
import sevseg

try:
    while True:
        print("\n" * 60)

        currentTime = time.localtime()
        hours = str(currentTime.tm_hour % 12)
        if hours == "0":
            hours = "12"
        minutes = str(currentTime.tm_min)
        seconds = str(currentTime.tm_sec)

        hDigits = sevseg.getSevSrgStr(hours, 2)
        hTopRow, hMiddleRow, hButtomRow = hDigits.splitlines()

        mDigits = sevseg.getSevSrgStr(minutes, 2)
        mTopRow, mMiddleRow, mButtomRow = mDigits.splitlines()

        sDigits = sevseg.getSevSrgStr(seconds, 2)
        sTopRow, sMiddleRow, sButtomRow = sDigits.splitlines()

        print(hTopRow + "     " + mTopRow + "     " + sTopRow)
        print(hMiddleRow + "  *  " + mMiddleRow + "  *  " + sMiddleRow)
        print(hButtomRow + "  *  " + mButtomRow + "  *  " + sButtomRow)
        print()
        print("Press Ctrl-C to quit.")

        while True:
            time.sleep(0.01)
            if time.localtime().tm_sec != currentTime.tm_sec:
                break
except KeyboardInterrupt:
    print("Digital Clock")
    sys.exit()
