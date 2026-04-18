import sys, time, math
import sevseg

secondsleft = 10.0

try:
    while True:
        print("\n" * 60)

        whole = int(secondsleft)
        hours = str(whole // 3600).zfill(2)
        minutes = str((whole % 3600) // 60).zfill(2)
        seconds = str(whole % 60).zfill(2)
        milli = str(int((secondsleft - whole) * 100))  # tenths

        hDigits = sevseg.getSevSrgStr(hours, 2)
        hTopRow, hMiddleRow, hButtomRow = hDigits.splitlines()

        mDigits = sevseg.getSevSrgStr(minutes, 2)
        mTopRow, mMiddleRow, mButtomRow = mDigits.splitlines()

        sDigits = sevseg.getSevSrgStr(seconds, 2)
        sTopRow, sMiddleRow, sButtomRow = sDigits.splitlines()

        milDigits = sevseg.getSevSrgStr(milli, 2)
        milTopRow, milMiddleRow, milButtomRow = milDigits.splitlines()

        print(hTopRow + "     " + mTopRow + "     " + sTopRow + "     " + milTopRow)
        print(
            hMiddleRow
            + "  *  "
            + mMiddleRow
            + "  *  "
            + sMiddleRow
            + "     "
            + milMiddleRow
        )
        print(
            hButtomRow
            + "  *  "
            + mButtomRow
            + "  *  "
            + sButtomRow
            + "  .  "
            + milButtomRow
        )

        if secondsleft <= 0:
            print()
            print("    * * * * BOOM * * * *")
            break
        print()
        print("Press Ctrl-C to quit.")

        time.sleep(0.01)
        secondsleft -= 0.01
except KeyboardInterrupt:
    sys.exit()
