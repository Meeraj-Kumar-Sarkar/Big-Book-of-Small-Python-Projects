import sys, time
import sevseg

secondsleft = 320

try:
    while True:
        print("\n" * 60)
        hours = str(secondsleft // 3600)
        minutes = str((secondsleft % 3600) // 60)
        seconds = str(secondsleft % 60)

        hDigits = sevseg.getSevSrgStr(hours, 2)
        hTopRow, hMiddleRow, hButtomRow = hDigits.splitlines()

        mDigits = sevseg.getSevSrgStr(minutes, 2)
        mTopRow, mMiddleRow, mButtomRow = mDigits.splitlines()

        sDigits = sevseg.getSevSrgStr(seconds, 2)
        sTopRow, sMiddleRow, sButtomRow = sDigits.splitlines()

        print(hTopRow + "     " + mTopRow + "     " + sTopRow)
        print(hMiddleRow + "  *  " + mMiddleRow + "  *  " + sMiddleRow)
        print(hButtomRow + "  *  " + mButtomRow + "  *  " + sButtomRow)

        if secondsleft == 0:
            print()
            print("    * * * * BOOM * * * *")
            break
        print()
        print("Press Ctrl-C to quit.")

        time.sleep(1)
        secondsleft -= 1
except KeyboardInterrupt:
    sys.exit()
