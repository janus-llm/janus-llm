# BIR/RTR-Orderable Item status
# 09/02/97 8:41

# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97

PSSITE = int(+$O(^PS(59.7, 0)))
if $P($G(^PS(59.7, PSSITE, 80)), "^", 2) != 2:
    print("\n", "?3,$S($P($G(^(80)),""^"",2)<2:""Orderable Item Auto-Create has not been completed!"",1:""Manual Matching process complete!"")", "\n")
    K PSSITE
    EXIT

print("\n", "This option looks at the 3 files that must be matched to the Orderable Item")
print("File, and tells you how many more need to be matched. The 3 files are:")
print("\n", "?5,""IV ADDITIVES File"",", "?5,""IV SOLUTIONS File"",", "?5,""DRUG File""")
print("\n", "(Lists will not include drugs that do not require matching.)")
print("\n")
%ZIS = "QM"
^%ZIS
if POP:
    EXIT

if $D(IO("Q")):
    ZTRTN = "BEG^PSSOICT"
    ZTDESC = "Pharmacy Orderable Item Status Report"
    ^%ZTLOAD
    K IO("Q")
    print("\n", "Report queued to print!", "\n")

BEG U IO
QFLAG = 0
X1 = DT
X2 = -365
C^%DTC
PDATE = X

if $E(IOST) == "C":
    print("\n", "Finding IV ADDITIVES that aren't matched, hold on:")
    for II in range(1, 4):
        print(".")
        H 1

if $E(IOST) != "C":
    ADDHEAD

MM = 0

if $E(IOST) == "C":
    print("\n")

AA = 0
while True:
    AA = int($O(^PS(52.6, AA)))
    if not AA or QFLAG:
        break
    if not $P($G(^PS(52.6, AA, 0)), "^", 11):
        DD = $P($G(^PS(52.6, AA, 0)), "^", 2)
        if not DD:
            continue
        FFFF = $P($G(^PS(52.6, AA, "I")), "^")
        if FFFF and FFFF < PDATE:
            continue
        if MM == 0:
            print("\n")
        print($P($G(^PS(52.6, AA, 0)), "^"), "?41,""Still needs to be matched."")
        MM += 1
        if ($Y + 4) > IOSL:
            if $E(IOST) == "C":
                DIRX
            if $E(IOST) != "C":
                ADDHEAD
            if $G(Y) != 1 and $E(IOST) == "C":
                QFLAG = 1
            if not QFLAG and $E(IOST) == "C":
                @IOF

if QFLAG:
    EXIT

if not MM:
    print("\n", "All IV ADDITIVES are matched that should be matched!", "\n")
if MM:
    print($C(7), "\n", "?3,MM,"" IV ADDITIVE(S) still need to be matched!"",", "\n")
    H 1

if $E(IOST) == "C":
    DIRX
    if $G(Y) != 1:
        EXIT

G ^PSSOICT1

EXIT
^%ZISC
if $D(ZTQUEUED):
    ZTREQ = "@"
K ^TMP($J, "PSSLIST")