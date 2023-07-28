# PSSPOIMN ;BIR/RTR/WRT - Orderable Item manual create ;09/01/98
# 1.0;PHARMACY DATA MANAGEMENT;**15,32,34,38,51,57,82,125,189,220**;9/30/97;Build 4

# Reference to ^PS(59 supported by DBIA #1976
# Reference to $$PSJDF^PSNAPIS(P1,P3) supported by DBIA #2531
# Reference to $$VAGN^PSNAPIS(P1) supported by DBIA #2531

PSSDONE = None
PSSITE = int(next(iter(^PS(59.7,0))))
if int(next(iter(^PS(59.7,PSSITE,80)).split("^")[1])) < 2:
    print("\nOrderable Item Auto-Create has not been completed yet!\n")
    PSSITE = None
    DIR = input("Press RETURN to continue")
    DIR = None
PSIEN = None
PSNAME = None

def MESS():
    pass

def BEG():
    global PSIEN, PSNAME
    if PSIEN is not None:
        PSIEN = None
    PSSCROSS = None
    DOSEFV = None
    DOSEFORM = None
    POINT = None
    SPHOLD = None
    NEWSP = None
    PSVAR1 = None
    PSITEM = None
    PSTOP = None
    PSMASTER = None
    DIC["S"] = None
    PSOUT = 0
    print("\n")
    DIC(0) = "QEAM"
    DIC = "^PSDRUG("
    DIC("A") = "Select DISPENSE DRUG: "
    DIC = None
    if DTOUT:
        BEG = None
        return
    if DUOUT:
        BEG = None
        return
    if int(next(iter(Y.split("^")))) < 1:
        BEG = None
        return
    PSIEN = int(next(iter(Y.split("^"))))
    PSNAME = next(iter(^PSDRUG(PSIEN,0).split("^")))
    if PSIEN:
        try:
            ^PSDRUG(PSIEN)
        except:
            print("\nAnother person is editing this one.")
            return
    MAS()

def MAS():
    global PSOUT, DOSEFV, DOSEFORM, POINT, SPHOLD, NEWSP, PSVAR1, PSITEM, PSTOP
    NODE = ^PSDRUG(PSIEN,"ND")
    DOSEPTR = 0
    DA = next(iter(^PSDRUG(PSIEN,"ND").split("^")))
    X = $$VAGN^PSNAPIS(DA)
    VAGEN = X
    if int(next(iter(^PSDRUG(PSIEN,"ND").split("^")))) and int(next(iter(^PSDRUG(PSIEN,"ND").split("^")))) and VAGEN != 0:
        K = int(next(iter(^PSDRUG(PSIEN,"ND").split("^", 3))))
        X = $$PSJDF^PSNAPIS(DA,K)
        DOSEFV = X
        if DOSEFV != 0:
            DOSEPTR = next(iter(X.split("^")))
            DOSEFORM = next(iter(X.split("^", 2)))
    TMP()
    if int(next(iter(^PSDRUG(PSIEN,2).split("^")))):
        POINT = int(next(iter(^PSDRUG(PSIEN,2).split("^"))))
        PSITEM = POINT
        print("\n", PSNAME, " is already matched to", "\n", "     ", next(iter(^PS(50.7,POINT,0).split("^"))), "_", next(iter(^PS(50.606,int(next(iter(^PS(50.7,POINT,0).split("^", 2)).split("^")[0]),0).split("^")))), "\n")
    if POINT:
        PSSIAD = next(iter(^PS(50.7,POINT,0).split("^", 4)))
        if PSSIAD:
            print("This Orderable Item has an Inactive Date.  *** ", Y, "\n", "To modify the Orderable Item, use the 'Edit Orderable Item' option.")
        input("Do you want to match to a different Orderable Item")

def TMP():
    global PSCNT
    ^TMP($J,"PSSOO") = None
    PSCNT = 0
    if int(next(iter(NODE.split("^")))) and int(next(iter(NODE.split("^", 3)))):
        ZZ = 0
        while ZZ:
            ZZ = next(iter(^PSDRUG("AND",int(next(iter(NODE.split("^")))),ZZ.split("^"))))
            if int(next(iter(^PSDRUG(ZZ,2).split("^")))) and next(iter(^PSDRUG(ZZ,2).split("^")))) != next(iter(POINT.split("^"))) and next(iter(^PS(50.7, next(iter(^PSDRUG(ZZ,2).split("^")),0).split("^")))):
                OTH = ^PSDRUG(ZZ,"ND")
                if int(next(iter(OTH.split("^")))) and int(next(iter(OTH.split("^", 3)))) and DOSEFV != 0:
                    DA = next(iter(OTH.split("^")))
                    K = next(iter(OTH.split("^", 3)))
                    X = $$PSJDF^PSNAPIS(DA,K)
                    DOSA = X
                    if DOSA != 0 and DOSEFV == DOSA:
                        NOFLAG = 0
                        TMPTR = next(iter(^PSDRUG(ZZ,2).split("^")))
                        FFF = 0
                        while FFF:
                            FFF = next(iter(^TMP($J,"PSSOO",FFF).split("^")))
                            if next(iter(^TMP($J,"PSSOO",FFF).split("^"))) == TMPTR:
                                NOFLAG = 1
                        if not NOFLAG:
                            PSCNT = PSCNT + 1
                            ^TMP($J,"PSSOO",PSCNT) = next(iter(^PSDRUG(ZZ,2).split("^"))) + "^" + ZZ

def DISP():
    global MATCH, TT, SPT, Y
    MATCH = 0
    TT = 0
    while TT:
        TT = next(iter(^TMP($J,"PSSOO",TT).split("^")))
        SPT = next(iter(^TMP($J,"PSSOO",TT).split("^")))
        print("\n", TT, "  ", next(iter(^PS(50.7,SPT,0).split("^"))), "_", next(iter(^PS(50.606,int(next(iter(^PS(50.7,SPT,0).split("^", 2)).split("^")[0]), 0).split("^")))), end="")
        if Y + 5 > IOSL:
            if input() == 0:
                Y = 0
            if input() == "":
                PSOUT = 1
    DISPO()

def DISPO():
    global Y, MATCH
    if PSOUT:
        return
    Y = input()
    if Y == "":
        PSOUT = 1
        return
    if "^" in Y:
        return
    if int(Y) < 1 or int(Y) > len(^TMP($J,"PSSOO")):
        print("\n", "INVALID NUMBER", "\n")
    MATCH = next(iter(^TMP($J,"PSSOO",int(Y)).split("^")))
    return

def MCH():
    global PSOUT
    if not PSOUT:
        OTHER()
        DISP()
    if PSOUT:
        return
    PSSDONE = 0
    if not PSOUT and MATCH:
        PSSP = MATCH
        PSSPOIM1()
        if PSNO:
            return
        if CKDUPVOL(int(MATCH), PSIEN):
            PSOUT = 1
            return
        DIE = "^PSDRUG("
        DA = PSIEN
        DR = "2.1////" + str(MATCH)
        ^DIE
        PSITEM = MATCH
        COM()
        PSSDONE = 1
    MCHA()

def REM():
    TMP()
    if len(^TMP($J,"PSSOO")):
        time.sleep(1)
        OTHER()
        DISP()
    if PSOUT:
        return
    PSSDONE = 0
    if len(^TMP($J,"PSSOO")) and MATCH:
        PSSP = MATCH
        PSSPOIM1()
        if PSOUT or PSNO:
            return
        if CKDUPVOL(int(MATCH), PSIEN):
            PSOUT = 1
            return
        DIE = "^PSDRUG("
        DA = PSIEN
        DR = "2.1////" + str(MATCH)
        ^DIE
        PSITEM = MATCH
        COM()
        PSSDONE = 1

def COM():
    print("\nMatch Complete!", "\n")
    PSSPOIM1()

def SET():
    PSSDXLF = 1
    PSSDXL = int(next(iter(^PS(50.7,next(iter(POINT.split("^"))),0).split("^"))[1]))
    return

def SETX():
    if PSSDXLF and PSSDXL and PSITEM and PSSDXL != int(next(iter(^PS(50.7,next(iter(PSITEM.split("^"))),0).split("^"))[1])):
        ^PSDRUG(PSIEN, "DOS2") = None
    if PSIEN:
        ^PSDRUG(PSIEN)
    PSSDXL = None
    PSSDXLF = None
    return

def MORE():
    global PSSDONE
    if PSIEN:
        PSSMORA = len(^PS(52.6,"AC",PSIEN))
        PSSMORS = len(^PS(52.7,"AC",PSIEN))
        if not PSSMORA and not PSSMORS:
            return
        print("\n")
        if PSSMORA:
            PSSMZ = 0
            while PSSMZ:
                PSSMZ = next(iter(^PS(52.6,"AC",PSIEN,PSSMZ).split("^")))
                if Y + 5 > IOSL:
                    if input() == 0:
                        Y = 0
                    if input() == "":
                        return
                print(next(iter(^PS(52.6,PSSMZ,0).split("^"))), " " * (42 - len(next(iter(^PS(52.6,PSSMZ,0).split("^"))))), "(A)")
                PSSMODT = next(iter(^PS(52.6,PSSMZ,"I").split("^")))
                if PSSMODT:
                    MODT()
        if PSSMORS:
            PSSMZ = 0
            while PSSMZ:
                PSSMZ = next(iter(^PS(52.7,"AC",PSIEN,PSSMZ).split("^")))
                if Y + 5 > IOSL:
                    if input() == 0:
                        Y = 0
                    if input() == "":
                        return
                print(next(iter(^PS(52.7,PSSMZ,0).split("^"))), " " * (31 - len(next(iter(^PS(52.7,PSSMZ,0).split("^"))))), next(iter(^PS(52.7,PSSMZ,0).split("^", 3))), " " * (42 - len(next(iter(^PS(52.7,PSSMZ,0).split("^", 3))))), "(S)")
                PSSMODT = next(iter(^PS(52.7,PSSMZ,"I").split("^")))
                if PSSMODT:
                    MODT()

def MODT():
    Y = next(iter(PSSMODT))
    if Y:
        DT()
        print(" " * (50 - len(str(Y))), next(iter(Y.split("^"))))

def CKDUPVOL(OIIEN,DRUGIEN):
    DUPVOL = 0
    IVSOL = 0
    PSSQUIT = None
    while IVSOL:
        IVSOL = next(iter(^PS(52.7,"AC",DRUGIEN,IVSOL).split("^")))
        if not $$GET1^DIQ(52.7,IVSOL,17,"I"):
            continue
        if $$GET1^DIQ(52.7,IVSOL,8,"I") and $$GET1^DIQ(52.7,IVSOL,8,"I") <= DT:
            continue
        if CKDUPSOL^PSSDDUT2(OIIEN,IVSOL,$$GET1^DIQ(52.7,IVSOL,2),0):
            print("\nMatching ", $$GET1^DIQ(50,DRUGIEN,.01), " to ", $$GET1^DIQ(50.7,OIIEN,.01), " would cause the")
            print("orderable item to have more than one Active IV Solution with the same volume")
            print("marked to be used in the IV FLUID ORDER ENTRY, which is not allowed.")
            print("\nPlease, review the IV Solutions associated with this drug before matching it")
            print("to this orderable item or match it to a different orderable item.")
            DUPVOL = 1
            break
    return DUPVOL