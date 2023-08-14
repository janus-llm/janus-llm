def PSSDEE1():
    # BIR/WRT - PDM match routine
    # 09/01/98
    # 1.0;PHARMACY DATA MANAGEMENT;**15,20,34,38,68,90,208,220,243**;9/30/97;Build 3
    # Reference to $$PSJDF^PSNAPIS(P1,P3) supported by DBIA #2531
    FLGMTH = 0
    if "ND" in ^PSDRUG[DA] and ^PSDRUG[DA]["ND"][2]:
        print("\n", " "*5, "points to ", ^PSDRUG[DA]["ND"][2], " in the National Drug file.", "\n")
        NDE = ^PSDRUG[DA]["ND"]
        PC1 = NDE[1]
        PC3 = NDE[3]
        FLGMTH = 1
        GETDF()
    if ^PSDRUG[DA][2] and ^PSDRUG[DA][2][1]:
        PSSOITM = ^PSDRUG[DA][2][1]
        if ^PS[50.7][PSSOITM][0]:
            PTR = ^PS[50.7][PSSOITM][0][2]
            OLDDF = ^PS[50.606][PTR][0][1]

def GETDF():
    DA = PC1
    K = PC3
    X = $$PSJDF^PSNAPIS(DA, K)
    OLDDF = X[2]
    DA = DISPDRG

def MESSAGE():
    # REMATCH PROMPT
    if "ND" in ^PSDRUG[DA] and ^PSDRUG[DA]["ND"][2]:
        print("\n", " "*5, "This drug has already been matched and classified with the National Drug", "\n", "file.")
    if ^PSDRUG[DA][3] and ^PSDRUG[DA][3][1] == 1:
        print("This drug has also been marked to transmit to CMOP.", "\n", "If you choose to rematch it, the drug will be marked NOT TO TRANSMIT to CMOP.", "\n")
    if "ND" in ^PSDRUG[DA] and not ^PSDRUG[DA]["ND"][2]:
        print("\n", " "*5, "This drug has been manually classed but not matched (merged with NDF).")

def RSET():
    if "ND" in ^PSDRUG[DA]:
        PSNID = ^PSDRUG[DA]["ND"][10]
    PSNP = ^PSDRUG[DA]["I"]
    if PSNP and PSNP < DT:
        print("\n", " "*5, "This drug cannot be matched because it has an INACTIVE date.", "\n")
        if not ^PSDRUG[DA]["I"]:
            DA = DISPDRG
            UNMDRUG^PSSUTIL(DA)
            if ^PSDRUG[DA][3]:
                ^PSDRUG[DA][3][1] = 0
            if ^PSDRUG["AQ"][DA]:
                ^PSDRUG["AQ"][DA] = None
            if PSNID and PSNID != "":
                PSNID = None
            ^PSSREF()

def PART2():
    if "ND" in ^PSDRUG[DA] and ^PSDRUG[DA]["ND"][2]:
        print(" In addition, if the dosage form changes as a result of rematching,", "\n", "you will have to match/rematch to Orderable Item.")

def ORDITM():
    if FLGKY != 1 and ^PSDRUG[DISPDRG][2]:
        APU = ^PSDRUG[DISPDRG][2][3]
        if APU in ["O", "I", "U", "X"]:
            OICK()

def OICK():
    if ^XMB["NETNAME"] not in "CMOP-" and ^PS[59.7][1][80] and ^PS[59.7][1][80][2] > 1:
        OIMESS()
        PSIEN = DISPDRG
        PSNAME = ^PSDRUG[DISPDRG][0][1]
        PSMASTER = 1
        MAS^PSSPOIMN()
        PSIEN = None
        PSNAME = None
        PSMASTER = None

def OIKILL():
    if "ND" in ^PSDRUG[DISPDRG] and FLGNDF == 1 and ^PSDRUG[DISPDRG][2] and ^PSDRUG[DISPDRG][2][1]:
        KMTCH()

def KMTCH():
    DIE = "^PSDRUG("
    DR = "2.1///" + "@"
    ^DIE
    CKIV()
    PSSINSTX = $O(^PS[59.7][0])
    if ^PS[59.7][PSSINSTX][80] and ^PS[59.7][PSSINSTX][80][3] < 2:
        PSSINSTX = None
    print("\n", " "*5, "Deleting Local Possible Dosages..")
    ^PSDRUG[DISPDRG]["DOS2"]

def OIMESS():
    print("\n", "** You are NOW in the ORDERABLE ITEM matching for the dispense drug. **", "\n")

def CKIV():
    ^TMP[$J]["SOL"] = None
    ^TMP[$J]["ADD"] = None

def SOLIO():
    if DISPDRG in ^PS[52.7]["AC"]:
        BBC = 0
        while True:
            BBC = $O(^PS[52.7]["AC"][DISPDRG][BBC])
            if not BBC:
                break
            SOLITM = ^PS[52.7][BBC][0][11]
            if SOLITM and ^PS[52.7]["AOI"][SOLITM][BBC]:
                SOLIO1()

def SOLIO1():
    IVDFPTR = ^PS[50.7][SOLITM][0][2]
    IVDF = ^PS[50.606][IVDFPTR][0][1]
    SOLNM = ^PS[52.7][BBC][0][1]
    CP()

def CP():
    if IVDF != NEWDF:
        ^TMP[$J]["SOL"][BBC] = SOLNM
        if ^PS[52.7][BBC][0][11]:
            DA = BBC
            DIE = "^PS[52.7,"
            DR = "9///" + "@"
            ^DIE

def SOLMESS():
    if FLG3 == 1 and "I" not in PSSANS and ^TMP[$J]["SOL"]:
        print("\n", " "*5, "You have SOLUTIONS that need to rematched to ORDERABLE ITEM.")
        NUM = 0
        while True:
            NUM = $O(^TMP[$J]["SOL"][NUM])
            if not NUM:
                break
            ENTRY = NUM
            SOI^PSSVIDRG()
            ^TMP[$J]["SOL"][NUM] = None

def ADDIO():
    if DISPDRG in ^PS[52.6]["AC"]:
        BBC = 0
        while True:
            BBC = $O(^PS[52.6]["AC"][DISPDRG][BBC])
            if not BBC:
                break
            ADDITM = ^PS[52.6][BBC][0][11]
            if ADDITM and ^PS[52.6]["AOI"][ADDITM][BBC]:
                ADDIO1()

def ADDIO1():
    IVDFPTR = ^PS[50.7][ADDITM][0][2]
    IVDF = ^PS[50.606][IVDFPTR][0][1]
    ADDNM = ^PS[52.6][BBC][0][1]
    CP1()

def CP1():
    if IVDF != NEWDF:
        ^TMP[$J]["ADD"][BBC] = ADDNM
        if ^PS[52.6][BBC][0][11]:
            DA = BBC
            DIE = "^PS[52.6,"
            DR = "15///" + "@"
            ^DIE

def ADDMESS():
    if FLG3 == 1 and "I" not in PSSANS and ^TMP[$J]["ADD"]:
        print("\n", " "*5, "You have ADDITIVES that need to rematched to ORDERABLE ITEM.")
        NUM = 0
        while True:
            NUM = $O(^TMP[$J]["ADD"][NUM])
            if not NUM:
                break
            ENTRY = NUM
            ADDOI^PSSVIDRG()
            ^TMP[$J]["ADD"][NUM] = None

def ADDMESS1():
    if FLG3 == 0 and ^TMP[$J]["ADD"]:
        print("\n", " "*5, "The following ADDITIVES need to rematched to ORDERABLE ITEM, however you do", "\n", "not have the ""PSJI MGR"" IV key. These must be matched before they made be used.", "\n")
        MESSA()

def MESSA():
    NUM = 0
    while True:
        NUM = $O(^TMP[$J]["ADD"][NUM])
        if not NUM:
            break
        print(" "*3, ^TMP[$J]["ADD"][NUM])

def SOLMESS1():
    if FLG3 == 0 and ^TMP[$J]["SOL"]:
        print("\n", " "*5, "The following SOLUTIONS need to rematched to ORDERABLE ITEM, however you do", "\n", "not have the ""PSJI MGR"" IV key. These must be matched before they may be used.", "\n")
        MESSS()

def MESSS():
    NUM = 0
    while True:
        NUM = $O(^TMP[$J]["SOL"][NUM])
        if not NUM:
            break
        print(" "*3, ^TMP[$J]["SOL"][NUM])

def ADDMESS2():
    if FLG3 == 1 and "I" in PSSANS and ^TMP[$J]["ADD"]:
        print("\n", " "*5, "The following ADDITIVES need to rematched to ORDERABLE ITEM.", "\n", "These must be matched before they made be used.", "\n")
        MESSA()

def SOLMESS2():
    if FLG3 == 1 and "I" in PSSANS and ^TMP[$J]["SOL"]:
        print("\n", " "*5, "The following SOLUTIONS need to rematched to ORDERABLE ITEM.", "\n", "These must be matched before they may be used.", "\n")
        MESSS()