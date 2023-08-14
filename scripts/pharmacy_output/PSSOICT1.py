# PSSOICT1 ;BIR/RTR-ORDERABLE ITEM STATUS continued ; 09/02/97 8:41
# ;;1.0;PHARMACY DATA MANAGEMENT;;9/30/97
import datetime

# Calculate the previous date
X1 = datetime.date.today()
X2 = datetime.timedelta(days=-365)
PDATE = X1 + X2

QFLAG = 0

if input("Finding IV SOLUTIONS that aren't matched, hold on:") == "":
    for II in range(1, 4):
        print(".")
        time.sleep(1)
else:
    SOLHEAD()

MM = 0

if input():
    print()

for AA in range(0, len(^PS(52.7))):
    if not AA or QFLAG:
        break
    if not ^PS(52.7, AA, 0)["^", 11:
        DD = ^PS(52.7, AA, 0)["^", 2]
        if not DD:
            continue
        FFFF = ^PS(52.7, AA, "I")["^"
        if FFFF and FFFF < PDATE:
            continue
        if MM == 0:
            ...
            print()
        print(^PS(52.7, AA, 0)["^"], " " * (35 - len(^PS(52.7, AA, 0)["^"])), ^PS(52.7, AA, 0)["^", 3], " " * (55 - len(^PS(52.7, AA, 0)["^", 3)), "Still needs matched.")
        MM += 1
        if ($Y + 4) > IOST:
            if IOST == "C":
                DIRX^PSSOICT()
            elif IOST != "C":
                SOLHEAD()
            if Y != 1 and IOST == "C":
                QFLAG = 1
            if not QFLAG and IOST == "C":
                print(IOF)
            print(IOF)
            print(" " * 5, "IV SOLUTION(S) that need matched:")
        if QFLAG:
            EXIT^PSSOICT()
        if not MM:
            print("All IV SOLUTIONS are matched that should be matched!")
        if MM:
            print(chr(7))
            print(" " * 3, MM, " IV SOLUTION(S) still need to be matched!")
            time.sleep(1)
        if IOST == "C":
            DIRX^PSSOICT()
        if Y != 1:
            EXIT^PSSOICT()
        if IOST == "C":
            print()
            print("Finding DISPENSE Drug(s) that aren't matched, hold on:")
            print()
            for II in range(1, 5):
                print(".")
                time.sleep(1)
        A = 1
        B = 0
        del ^TMP($J, "PSSLIST")
        ZZZ = ""
        while ZZZ:
            ZZ = ^PSDRUG("B", ZZZ, 0)
            if ZZ:
                if ^PSDRUG(ZZ, 0):
                    if not ^PSDRUG(ZZ, 2)["^":
                        APP = ^PSDRUG(ZZ, 2)["^", 3]
                        if APP["O" or APP["I" or APP["U":
                            SS = ^PSDRUG(ZZ, "I")["^"]
                            if SS and SS < PDATE:
                                continue
                            if IOST == "C" and ZZ > 99 and ZZ[($L(ZZ) - 1):($L(ZZ))] == "00":
                                print(".")
                            if not ^PSDRUG(ZZ, "ND")["^"]:
                                B += 1
                            ^TMP($J, "PSSLIST", A) = ^PSDRUG(ZZ, 0)["^"]
                            A += 1
                            if IOST == "C":
                                print(".")
            if not QFLAG:
                if A == 1:
                    print("All DISPENSE Drugs are matched that should be matched!")
                    time.sleep(2)
                    print()
                    EXIT^PSSOICT()
                print()
                print((A - 1), " DISPENSE drugs still need to be matched!")
                time.sleep(1)
            if B:
                print(B, " because Drug is not matched to National Drug File")
                time.sleep(1)
            if IOST == "C":
                DIR(0) = "Y"
                DIR("B") = "Y"
                DIR("A") = "Do you want to see these Drugs"
                DIR()
                if Y != 1:
                    EXIT^PSSOICT()
            if IOST == "C":
                print(IOF)
            if IOST != "C":
                DH()
            for XXX in range(0, len(^TMP($J, "PSSLIST"))):
                if not XXX or QFLAG:
                    break
                print(^TMP($J, "PSSLIST", XXX), " " * (43 - len(^TMP($J, "PSSLIST", XXX))), "Still needs to be matched.")
                if ($Y + 4) > IOST:
                    if IOST == "C":
                        DIRX^PSSOICT()
                    if IOST != "C":
                        DH()
                    if Y != 1 and IOST == "C":
                        QFLAG = 1
                    if not QFLAG and IOST == "C":
                        print(IOF)
                    print(IOF)
                    print("END OF LIST")
        EXIT^PSSOICT()

SOLHEAD()
    print(IOF)
    print("IV SOLUTION(S) THAT AREN'T MATCHED")
    print("________________________________")

DH()
    print(IOF)
    print("DISPENSE DRUG(S) THAT AREN'T MATCHED")
    print("__________________________________")