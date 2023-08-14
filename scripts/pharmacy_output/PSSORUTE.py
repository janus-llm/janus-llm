# PSSORUTE ;OIFO BAY PINES/ELR-CONTINUATION OF PSSORUTL ;07/20/04
# 1.0;PHARMACY DATA MANAGEMENT;**83,93,187**;9/30/97;Build 27
#
# Reference to ^PS(52.41 is supported by DBIA # 2844.
# Reference to ^PSRX is supported by DBIA # 2845.
# Reference to ^PS(53.1 is supported by DBIA # 2140.

def NU():
    global PSONDU, PSONDS
    PSONDU = ''
    if PSONDS and PSONDU:
        PSONDU = "^" + str(PSONDU)
    return

def SETU():
    global PSSUNITX, PSIEN
    PSSUNITX = ""
    PSSUNITX = "^" + str(PSSUNITX)
    return

def STATUS(PSSDFN, PSSON):
    global PSSUNITX, PSIEN
    ST = ""
    TYPE = ""
    LEN = 0
    PKG = ""
    A = ""
    STO = ""
    RX2 = ""
    STA = ""
    Y = ""
    NOW = ""
    LEN = len(PSSON.split(";")[0])
    PKG = PSSON.split(";")[1]
    if PSSON.isdigit():
        TYPE = "O"
    else:
        TYPE = PSSON[LEN]
        PSSON = PSSON[:LEN-1]
    if PKG == "I":
        if TYPE == "P":
            A = (^PS(53.1,PSSON,0))["^",9]
            ST = CODES(A,53.1,28)
        elif TYPE == "V":
            A = (^PS(55,PSSDFN,"IV",PSSON,0))["^",17]
            ST = CODES(A,55.01,100)
        elif TYPE == "U":
            A = (^PS(55,PSSDFN,5,PSSON,0))["^",9]
            ST = CODES(A,55.06,28)
    elif PKG == "O":
        if TYPE == "P" or TYPE == "S":
            A = (^PS(52.41,PSSON,0))["^",3]
            ST = ""
            if A:
                ST = "PENDING"
        elif TYPE == "N":
            A = (^PS(55,PSSDFN,"NVA",PSSON,0))["^",7]
            ST = "ACTIVE" if not A else "DISCONTINUED"
        elif TYPE == "R" or TYPE == "O":
            RX2 = (^PSRX,PSSON,2)
            STA = (^PSRX,PSSON,"STA")
            STO = 11 if STA < 12 and RX2["^",6 < NOW else STA
            ST = "^" + STO + 2
            if ST == "ACTIVE" and (^PSRX,PSSON,"PARK"):
                ST = "ACTIVE/PARKED"   # ADDED PAPI CODE
    return ST

def CODES(PSSCD, PSSF, PSSFLD):
    global PSSDD, Y
    PSSDD = ""
    Y = ""
    PSSDD["POINTER"] = ""
    FIELD(PSSF, PSSFLD, "", "POINTER", PSSDD)
    Y = PSSDD["POINTER"]
    PSSDD = ""
    Y = "^" + Y
    Y = Y.split(";" + PSSCD + ":")[1].split(";")[0]
    return Y