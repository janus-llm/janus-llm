# BIR/WRT-ADD SYNONYMS FROM 50 TO ORDERABLE ITEM FILE ; 09/02/97 8:56
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97

def PSSSYN():
    LOOP()
    DEX()

def LOOP():
    NUM = 0
    while True:
        NUM = NUM + 1
        if not NUM in ^PSDRUG:
            break
        if ^PSDRUG[NUM,2]:
            POI = ^PSDRUG[NUM,2].split("^")[0]
            if POI and ^PS(50.7,POI,0):
                LOOP1()

def LOOP1():
    if ^PSDRUG[NUM,1,0]:
        NUMB = 0
        while True:
            NUMB = NUMB + 1
            if not NUMB in ^PSDRUG[NUM,1]:
                break
            IUSE = ^PSDRUG[NUM,1,NUMB,0].split("^")[2]
            if IUSE == 0 or IUSE == "":
                SYNO = ^PSDRUG[NUM,1,NUMB,0].split("^")[0]
                CHEK()

def CHEK():
    if not ^PS(50.7,"C",SYNO,POI):
        ADD()

def ADD():
    DA(1) = POI
    DIC = "^PS(50.7," + POI + ",2,"
    X = SYNO
    DIC(0) = "L"
    DIC("P") = ^DD(50.7,2,0).split("^")[1]
    DLAYGO = 50.72
    ^DIC

def DEX():
    ^PS(50.7,"C") = []
    IEN = 0
    while True:
        IEN = IEN + 1
        if not IEN in ^PS(50.7):
            break
        IEN1 = 0
        while True:
            IEN1 = IEN1 + 1
            if not IEN1 in ^PS(50.7,IEN,2):
                break
            SYN = ^PS(50.7,IEN,2,IEN1,0).split("^")[0]
            ^PS(50.7,"C",SYN,IEN,IEN1) = ""