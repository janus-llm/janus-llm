# BIR/RTR/WRT-Initial Solution and Additive matching
# 10/09/97 13:08

# 1.0;PHARMACY DATA MANAGEMENT;**2**;9/30/97

PSSSSS1 = 0
PSOOOUT = 0
PSSSSS = 1

X1 = DT
X2 = -365
PSXDATE = X

print("\nMATCHING IV ADDITIVES!\n")
BBBBB = ""
while BBBBB:
    BBBBB = next(iter(filter(lambda x: x != "", BBBBB)))
    PSOOOUT = False
    for AAAA in range(len(BBBBB)):
        AAAA = next(iter(filter(lambda x: x != "", AAAA)))
        if not AAAA or not AAAA in ^PS(52.6,"B",BBBBB):
            continue
        if not AAAA or not ^PS(52.6,AAAA,0) or ^("$P(^PS(52.6,AAAA,0),"^",11)") or not ^("$P(^PS(52.6,AAAA,0),"^",2)"):
            continue
        BBBB = +^PS(52.6,AAAA,0)^("$P(^PS(52.6,AAAA,0),"^",2)")
        if not BBBB or not ^PSDRUG(BBBB,0):
            continue
        PSXADATE = +$P(^PS(52.6,AAAA,"I")^("$P($G(^PS(52.6,AAAA,"I")),"^")")
        if PSXADATE and PSXADATE < PSXDATE:
            continue
        PSSSSS1 = True
        PSAIEN = AAAA
        PSANAME = ^PS(52.6,PSAIEN,0)^("$P(^PS(52.6,PSAIEN,0),"^")")
        PSDISP = ^PS(52.6,PSAIEN,0)^("$P(^PS(52.6,PSAIEN,0),"^",2)")
        PSPOI = ^PS(52.6,PSAIEN,0)^("$P(^PS(52.6,PSAIEN,0),"^",11)")
        print("\nIV Additive -> ", PSANAME)
        PSSSSS = 1
        ENTER^PSSADDIT()
        print()
        DIR(0) = "Y"
        DIR("A") = "Continue matching IV Additives"
        DIR("B") = "YES"
        ^DIR()
        print()
        if Y != 1:
            PSOOOUT = 1
    if not PSSSSS1:
        print("\nIV Additives are all matched!\n")
    if PSOOOUT:
        break

PSPOI = None

PSSSSS1 = 0
PSSSSS = 1

print("\nMATCHING IV SOLUTIONS!\n")
AAAAA = ""
while AAAAA:
    AAAAA = next(iter(filter(lambda x: x != "", AAAAA)))
    PSOOOUT = False
    for AAAA in range(len(AAAAA)):
        AAAA = next(iter(filter(lambda x: x != "", AAAA)))
        if not AAAA or not AAAA in ^PS(52.7,"B",AAAAA):
            continue
        if not AAAA or not ^PS(52.7,AAAA,0) or ^("$P(^PS(52.7,AAAA,0),"^",11)") or not ^("$P(^PS(52.7,AAAA,0),"^",2)"):
            continue
        BBBB = +^PS(52.7,AAAA,0)^("$P(^PS(52.7,AAAA,0),"^",2)")
        if not BBBB or not ^PSDRUG(BBBB,0):
            continue
        PSXSDATE = +$P(^PS(52.7,AAAA,"I")^("$P($G(^PS(52.7,AAAA,"I")),"^")")
        if PSXSDATE and PSXSDATE < PSXDATE:
            continue
        PSSSSS1 = True
        PSSIEN = AAAA
        PSSNAME = ^PS(52.7,PSSIEN,0)^("$P(^PS(52.7,PSSIEN,0),"^")")
        PSDISP = ^PS(52.7,PSSIEN,0)^("$P(^PS(52.7,PSSIEN,0),"^",2)")
        PSSOI = ^PS(52.7,PSSIEN,0)^("$P(^PS(52.7,PSSIEN,0),"^",11)")
        PSSVOL = ^PS(52.7,PSSIEN,0)^("$P(^PS(52.7,PSSIEN,0),"^",3)")
        print("\nIV Solution -> ", PSSNAME, "   ", PSSVOL)
        PSSSSS = 1
        ENTER^PSSSOLIT()
        print()
        DIR(0) = "Y"
        DIR("B") = "YES"
        DIR("A") = "Continue matching IV Solutions"
        ^DIR()
        print()
        if Y != 1:
            PSOOOUT = 1
    if not PSSSSS1:
        print("\nIV Solutions are all matched!\n")
    if PSOOOUT:
        break

PSSSSS1 = 0
AAAA = ""
BBBB = ""
CCCC = None

def DIR():
    if PSOIEN and ^PS(50.7,PSOIEN) and ^("$P(^PS(50.7,PSOIEN,0),"^",4)") != "":
        print("\nThis Orderable Item is Inactive.   ***")
        Y = ^("$P(^PS(50.7,PSOIEN,0),"^",4)")
        X = ^DD("DD")
        print(" "*43, Y)
    if PSSOI and ^PS(50.7,PSSOI) and ^("$P(^PS(50.7,PSSOI,0),"^",4)") != "":
        print("\nThis Orderable Item is Inactive.   ***")
        Y = ^("$P(^PS(50.7,PSSOI,0),"^",4)")
        X = ^DD("DD")
        print(" "*43, Y)
    if PSPOI and ^PS(50.7,PSPOI) and ^("$P(^PS(50.7,PSPOI,0),"^",4)") != "":
        print("\nThis Orderable Item is Inactive.   ***")
        Y = ^("$P(^PS(50.7,PSPOI,0),"^",4)")
        X = ^DD("DD")
        print(" "*43, Y)
    DIR(0) = "Y"
    DIR("B") = "NO"
    DIR("A") = "Edit Orderable Item"
    ^DIR()
    if Y == 1:
        PSSDIR = 1

END = None