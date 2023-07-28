# BIR/JMB,WRT ; 09/02/97 7:57; 5/6/94
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
def EDIT():
    # Mark/unmark drugs to print on profile
    IEN50 = DISPDRG
    if LMFLAG == 1:
        UNMRK()
    if NFLAG or DTOUT or DIRUT or DUOUT:
        return
    if int(^PSDRUG(IEN50,"I")):
        Y = ^PSDRUG(IEN50,"I")
        print("** Drug inactivated " + str(Y) + ".")
    if ^PSDRUG(IEN50,"CLOZ1") == "PSOCLO1":
        print("\a\a")
        print("\nThis drug is marked for Clozapine monitoring. To print the most")
        print("recent lab result on the profile, the drug must be unmarked")
        print("for Clozapine monitoring.")
        REASK()
    if CLFLAG or NFLAG or DIRUT or DTOUT or DUOUT:
        return
    LIEN = int(^PSDRUG(IEN50,"CLOZ"))
    print("** You are NOW editing LAB MONITOR fields. **")
    DIC(0) = "QEAM"
    DIC("A") = "Select LAB TEST MONITOR: "
    DIC = "^LAB(60,"
    DIC("B") = ^LAB(60,LIEN,0)
    DIC(^DIC)
    if Y < 0 or DIRUT:
        EXIT()
    LIEN = +Y
    if ^$P(^LAB(60,LIEN,0),"^",5),";",2) == "":
        print("\n\aMissing DATA NAME Probably a panel test.  Please select another.")
        ED()
    DIE = "^PSDRUG("
    DA = IEN50
    DR = "17.2////^S X=LIEN"
    DIE(^DIE)
    print("\n\nNow editing:\n")
    DIE = "^PSDRUG("
    DA = IEN50
    DR = "17.2;17.4;17.3"
    DIE(^DIE)
    ^PSDRUG(IEN50,"CLOZ1") = 1
    LMFLAG = 1
    NFLAG = 1
    if DTOUT or DUOUT:
        EXIT()
    if ^PSDRUG(DA,"CLOZ") == "" and ^("CLOZ",2) == "" and ^("CLOZ",3) == "":
        ^PSDRUG(IEN50,"CLOZ1") = ""
        EDIT()
    if ^PSDRUG(DA,"CLOZ") == "" or ^("CLOZ",2) == "" or ^("CLOZ",3) == "":
        ^PSDRUG(IEN50,"CLOZ1") = ""
        print("\n\aInsufficient data.")
        print("All fields must have an entry or all fields must be blank.")
        LMFLAG = 0
        ED()
    EXIT()
    IEN50 = LIEN
    LIEN = ""
    return

def PRINT():
    if not ^DPT(DFN,"LR"):
        print("*** NO LAB DATA ON FILE ***")
        return
    LRDFN = ^DPT(DFN,"LR")
    if not LRDFN:
        return
    MDRUG = ^RX0(6)
    TST = ^PSDRUG(MDRUG,"CLOZ")
    MDAYS = ^("CLOZ",2)
    TSTSP = ^("CLOZ",3)
    if not TST or not MDAYS or not TSTSP:
        CLEAN()
        return
    TSTN = ^LAB(60,TST,0)
    LDN = ^(.2) if ^LAB(60,TST,.2) else ^($P(^LAB(60,TST,0),"^",5),";",2)
    if ^LAB(60,TST,.2) == "" and $P($P(^LAB(60,TST,0),"^",5),";",2) == "":
        print("*** RESULTS FOR A PANEL CANNOT BE PRINTED! ONLY A LAB TEST RESULT CAN BE PRINTED FOR MARKED DRUGS.")
        CLEAN()
        return
    X = "T-" + MDAYS
    %DT(^%DT)
    EDT = Y
    EDL = (9999999-EDT) + ".999999"
    INDIC = 0
    BDL = 0
    while BDL <= 0:
        BDL = ^LR(LRDFN,"CH",BDL)
        if BDL == "" or BDL > EDL:
            break
        if not ^LR(LRDFN,"CH",BDL,LDN) or not ^LR(LRDFN,"CH",0):
            continue
        if $P(^LR(LRDFN,"CH",BDL,0),"^",3) == "" or $P(^(0),"^",5) != TSTSP:
            continue
        Y = $S(+$P($P(^LR(LRDFN,"CH",BDL,0),"^"),"."):+$P($P(^(0),"^"),"."),1:$P(^(0),"^",3))
        print("*** MOST RECENT " + TSTN + " PERFORMED " + $E(Y,4,5) + "-" + $E(Y,6,7) + "-" + $E(Y,2,3) + " = " + +^LR(LRDFN,"CH",BDL,LDN) + " " + $P(^LAB(60,TST,1,TSTSP,0),"^",7))
        INDIC = 1
    if INDIC == 0:
        print("*** NO RESULTS FOR " + TSTN + " SINCE " + $E(EDT,4,5) + "-" + $E(EDT,6,7) + "-" + $E(EDT,2,3))
    CLEAN()
    return

def UNMRK():
    if ^PSDRUG(IEN50,"CLOZ1",2) == 1:
        DIR(0) = "Y"
        DIR("A",1) = ""
        DIR("A",2) = "Are you sure you want to unmark " + ^PSDRUG(IEN50,0)
        DIR("A") = "as a Lab Monitor drug"
        DIR("B") = "N"
        UNMRK0()
    return

def UNMRK0():
    ^DIR()
    if DIRUT or DTOUT or DUOUT:
        return
    UNMRK1()
    return

def UNMRK1():
    if "Yy".contains(X):
        LMFLAG = 0
        DR = "17.6///@"
        DIE = "^PSDRUG("
        DIE(^DIE)
        if LMFLAG == 0:
            print("\n\n" + ^PSDRUG(IEN50,0) + " is now unmarked as a Lab Monitor drug")
        ASKEM()
    return

def REASK():
    MONCLOZ^PSSDEE()
    return

def ASKEM():
    DIR = ""
    X = ""
    Y = ""
    DIRUT = ""
    DTOUT = ""
    DUOUT = ""
    print("\n\nDo you wish to mark this drug as a Clozapine drug?")
    DIR(0) = "Y"
    DIR(^DIR)
    if DTOUT or DUOUT or DIRUT:
        return
    if "Nn".contains(X):
        NFLAG = 1
        DIR = ""
        X = ""
        Y = ""
        DIRUT = ""
        DTOUT = ""
        DUOUT = ""
        return
    if "Yy".contains(X):
        CLOZ^PSSDEE()
    return