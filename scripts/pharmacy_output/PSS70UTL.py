# BIR/SJA-POST INSTALL ROUTINE FOR PSS*1*70 ; 01/21/00 13:30
# 1.0;PHARMACY DATA MANAGEMENT;**70**;09/30/97

def PSS70UTL():
    print("...Re-building the Synonym Multiple for GTIN barcode...")
    PSSD, CNT = 0, 0
    while PSSD:
        PSSD = getNextPSSD(PSSD)
        B = 0
        while B:
            B = getNextB(PSSD, B)
            PSSY = getPSDRUG(PSSD, B)
            if getPSSX(PSSY):
                PSSX = getPSSX(PSSY)
                CHK(PSSX)

def getNextPSSD(PSSD):
    return PSSD + 1

def getNextB(PSSD, B):
    return B + 1

def getPSDRUG(PSSD, B):
    return "^PSDRUG(PSSD,1,B)"

def getPSSX(PSSY):
    return $P(PSSY,"^")

def CHK(PSSX):
    if PSSX.isnumeric() and (len(PSSX) == 16 or len(PSSX) == 27):
        if PSSX[:2] != "01":
            return
        if len(PSSX) > 26 and PSSX[16:18] != "17":
            return
        if PSSX[4] == "3":
            PSSX = PSSX[5:15]
            CNT += 1
            if CNT % 10 == 0:
                print(".")
            FILE(PSSD, PSSX)

def FILE(PSSD, PSSX):
    DIC = "^PSDRUG(PSSD,1,"
    DIC(0) = "L"
    DLAYGO = 50.1
    DA(1) = PSSD
    X = PSSX
    FILE^DICN

PSS70UTL()