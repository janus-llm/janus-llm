# BIR/WRT - MASTER DRUG ENTER/EDIT ROUTINE
# Nov 27, 2018@10:03
# 1.0;PHARMACY DATA MANAGEMENT;**3,5,15,16,20,22,28,32,34,33,38,57,47,68,61,82,90,110,155,156,180,193,200,207,195,227,220,214**;9/30/97;Build 43

# Reference to ^PS(59 supported by DBIA #1976
# Reference to REACT1^PSNOUT supported by DBIA #2080
# Reference to $$UP^XLFSTR(X) supported by DBIA #10104
# Reference to $$PSJDF^PSNAPIS(P1,P3) supported by DBIA #2531
# Reference to PSNAPIS supported by DBIA #2531
# Reference to ^XMB("NETNAME" supported by DBIA #1131
# Reference to ^XUSEC supported by DIBA #10076
# Reference to FDR & FDT^PSNACT supported by DBIA #6754

def BEGIN():
    global PSSUPRAF, PSSTDRUG
    PSSFLAG = 0
    PSSDEE2()
    PSSZ = 1
    PSSXX = 1
    while True:
        ASK()
        if PSSFLAG:
            break
    DONE()
    PSSDEE2()
    del PSSFLAG, PSSXX, DIE, DIR, CLFLAG, CLFALG, DISPDRG, DLAYGO, DR, ENTRY, FLAG, FLG1, FLG2, FLG4, FLG5, FLG6, FLG7, FLGKY, FLGMTH, FLGNDF, FLGOI, K, NEWDF, NFLAG, NWND, NWPC1, NWPC2, NWPC3, OLDDF, PSIUDA, PSIUX, PSNP, PSSANS, PSSASK, PSSDA, PSSDD, PSSFLAG, PSSOR, PSSZ, PSXBT, PSXF, PSXFL, PSXUM, PSXGOOD, PSXLOC, ZAPFLG

def ASK():
    print()
    DIC = "^PSDRUG("
    DIC(0) = "QEALMNTV"
    DLAYGO = 50
    DIC("T") = ""
    DIC("W") = "S PSSTDRUG=Y D GETTIER^PSSDEE(PSSTDRUG)"
    result = input(DIC)
    Y = int(result)
    if Y < 0:
        global PSSFLAG
        PSSFLAG = 1
        return
    PSINACT = 0
    FLG1, FLG2, FLG3, FLG4, FLG5, FLG6, FLG7, FLAG, FLGKY, FLGOI, PSINACT = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    DISPDRG = Y
    L = +^PSDRUG(DISPDRG)
    if not L:
        print("\nAnother person is editing this one.")
        return
    BEFORE^PSSDEEA($T(+0))  # drug enter/edit auditing
    if "^PSDRUG(", DISPDRG, "I" in globals():
        PSINACT = "^PSDRUG(", DISPDRG, "I"
        if PSINACT and PSINACT < DT:
            PSINACT = 1
    PSSHUIDG = 1
    PSSNEW = Y[2]
    USE()
    NOPE()
    COMMON()
    DEA()
    MF()
    PSSHUIDG = None
    del PSSUPRAF
    # if any outpatient site has a dispense machine running HL7 V.2.4, then
    # run the new routine and create message
    for XX in range(0, len(^PS(59))):
        DVER = GET1^DIQ(59, XX, 105, "I")
        DMFU = GET1^DIQ(59, XX, 105.2)
        DNSNAM = GET1^DIQ(59, XX, 2006)
        DNSPORT = GET1^DIQ(59, XX, 2007)
        if DVER == "2.4" and DNSNAM != "" and DMFU == "YES":
            DRG^PSSDGUPD(DISPDRG, PSSNEW, DNSNAM, DNSPORT)
    DRG^PSSHUIDG(DISPDRG, PSSNEW)
    L = -^PSDRUG(DISPDRG)
    AFTER^PSSDEEA($T(+0))  # drug enter/edit auditing
    XX = GET1(^PSDRUG(DISPDRG, 2), 3)
    if "U" in XX or "I" in XX:
        XX = SNDHL7^PSSMSTR()
        if XX:
            if PSSNEW and (XX == 2 or XX == 3):  # U=1,N=2,B=3
                pass
            elif not PSSNEW and XX == 2:  # U=1,N=2,B=3
                PSSPADE = 1
                ENP^PSSHLDFS(DISPDRG, "MUP")
    EPHARM^PSSBPSUT(DISPDRG)
    del FLG3, PSSNEW

def COMMON():
    global DIE, DR
    DIE = "^PSDRUG("
    DR = "[PSSCOMMON]"
    ^DIE
    if Y or DTOUT:
        return
    if not "^PSDRUG(", DA, 660 in globals():
        ^PSDRUG(DA, 660) = ""
    if not Y:
        print("PRICE PER DISPENSE UNIT:", ^PSDRUG(DA, 660)[6])
    DEA()
    CK()
    ASKND()
    OIKILL^PSSDEE1()
    COMMON1()

def COMMON1():
    print("\nJust a reminder...you are editing ", ^PSDRUG(DISPDRG)[0], ".")
    PSSVVDA = DISPDRG
    DOSN^PSSDOS()
    DA = PSSVVDA
    USE()
    APP()
    ORDITM^PSSDEE1()

def CK():
    DSPY^PSSDEE1()
    FLGNDF = 0

def ASKND():
    global PSSUPRAF
    % = -1
    if ^XUSEC("PSNMGR", DUZ):
        MESSAGE^PSSDEE1()
        print("\nDo you wish to match/rematch to NATIONAL DRUG file", end=" ")
        % = 1
        if FLGMTH == 1:
            % = 2
        YN^DICN()
    if % == 0:
        print("\nIf you answer \"yes\", you will attempt to match to NDF.")
        ASKND()
    PSSUPRAF = %
    if % == 2:
        return
    if % == 1:
        RSET^PSSDEE1()
        if not PSINACT:
            EN1^PSSUTIL(DISPDRG, 1)
        X = "PSNOUT"
        if ^%ZOSF("TEST"):
            REACT1^PSNOUT()
            DA = DISPDRG
            if ^PSDRUG(DA, "ND") and ^PSDRUG(DA, "ND")[2:
                ONE()

def ONE():
    PSNP = ^PSDRUG(DA, "I")
    if PSNP and PSNP < DT:
        print("\nYou have just VERIFIED this match and MERGED the entry.")
        CKDF()
        EN2^PSSUTIL(DISPDRG, 1)
        if not OLDDF:
            OLDDF = ""
        if OLDDF != NEWDF:
            FLGNDF = 1
            WR()

def CKDF():
    NWND = ^PSDRUG(DA, "ND")
    NWPC1 = NWND[1]
    NWPC3 = NWND[3]
    DA = NWPC1
    K = NWPC3
    X = PSJDF^PSNAPIS(DA, K)
    NEWDF = X[2]
    DA = DISPDRG
    PSSK = PKIND^PSSDDUT2()

def NOPE():
    global ZAPFLG
    if not ^PSDRUG(DA, "ND") and ^PSDRUG(DA, 2) and ^PSDRUG(DA, 2)[1:
        DFNULL()
    if not ^PSDRUG(DA, "ND") and not ^PSDRUG(DA, 2):
        DFNULL()
    if ^PSDRUG(DA, "ND") and not ^PSDRUG(DA, "ND")[2 and ^PSDRUG(DA, 2) and not ^PSDRUG(DA, 2)[1:
        DFNULL()

def DFNULL():
    OLDDF = ""
    ZAPFLG = 1

def ZAPIT():
    global ZAPFLG
    if ZAPFLG and ZAPFLG == 1 and FLGNDF == 1 and OLDDF != NEWDF:
        CKIV^PSSDEE1()

def APP():
    print("\nMARK THIS DRUG AND EDIT IT FOR: ")
    CHOOSE()

def CHOOSE():
    global FLG1, FLG2, FLG3, FLG4, FLG5, FLG6, FLG7, FLAG, FLGKY
    if ^XUSEC("PSORPH", DUZ) or ^XUSEC("PSXCMOPMGR", DUZ):
        print("\nO  - Outpatient")
        FLG1 = 1
    if ^XUSEC("PSJU MGR", DUZ):
        print("\nU  - Unit Dose")
        FLG2 = 1
    if ^XUSEC("PSJI MGR", DUZ):
        print("\nI  - IV")
        FLG3 = 1
    if ^XUSEC("PSGWMGR", DUZ):
        print("\nW  - Ward Stock")
        FLG4 = 1
    if ^XUSEC("PSAMGR", DUZ) or ^XUSEC("PSA ORDERS", DUZ):
        print("\nD  - Drug Accountability")
        FLG5 = 1
    if ^XUSEC("PSDMGR", DUZ):
        print("\nC  - Controlled Substances")
        FLG6 = 1
    if ^XUSEC("PSORPH", DUZ):
        print("\nX  - Non-VA Med")
        FLG7 = 1
    if not FLG1 and not FLG2 and not FLG3 and not FLG4 and not FLG5 and not FLG6 and not FLG7:
        print("\nYou do not have the proper keys to continue.")
        print("Sorry, this concludes your editing session.")
        FLGKY = 1
        return
    if FLGKY != 1:
        PSSANS = input("\nEnter your choice(s) separated by commas: ")
        PSSANS = PSSANS.upper()
        BRANCH()
        BRANCH1()

def CHECK(X):
    # Validates Application Use response
    CHECK = 1
    if X == "" or "^" in Y or DIRUT in globals():
        return CHECK
    for C in X.split(","):
        print(C, "- ", end="")
        if C == "O" and FLG1:
            print("Outpatient")
            continue
        if C == "U" and FLG2:
            print("Unit Dose")
            continue
        if C == "I" and FLG3:
            print("IV")
            continue
        if C == "W" and FLG4:
            print("Ward Stock")
            continue
        if C == "D" and FLG5:
            print("Drug Accountability")
            continue
        if C == "C" and FLG6:
            print("Controlled Substances")
            continue
        if C == "X" and FLG7:
            print("Non-VA Med")
            continue
        print("Invalid Entry")
        CHECK = 0
    return CHECK

def BRANCH():
    global PSSANS
    if "O" in PSSANS:
        OP()
    if "U" in PSSANS:
        UD()
    if "I" in PSSANS:
        IV()
    if "W" in PSSANS:
        WS()
    if "D" in PSSANS:
        DACCT()
    if "C" in PSSANS:
        CS()
    if "X" in PSSANS:
        NVM()

def BRANCH1():
    global FLAG
    if FLAG and "A" in PSSANS:
        OP()
        UD()
        IV()
        WS()
        DACCT()
        CS()
        NVM()

def OP():
    global DIE, DR
    if FLG1:
        print("\n** You are NOW editing OUTPATIENT fields. **")
        PSIUDA = DA
        PSIUX = "O^Outpatient Pharmacy"
        ^PSSGIU()
        if % == 1:
            DIE = "^PSDRUG("
            DR = "[PSSOP]"
            ^DIE
            OPEI()
            ASKCMOP()
            if ^%ZOSF("TEST"):
                ASKCLOZ()
                FLGOI = 1
    if FLG1:
        CKCMOP()

def CKCMOP():
    if "^PSDRUG(", DISPDRG, 2, 3 not in globals():
        if "^PSDRUG(", DISPDRG, 3 in globals():
            ^PSDRUG(DISPDRG, 3)[1] = 0
            if "^PSDRUG(", DISPDRG in globals():
                del ^PSDRUG("AQ", DISPDRG)
            DA = DISPDRG
            ^PSSREF()

def UD():
    if FLG2:
        print("\n** You are NOW editing UNIT DOSE fields. **")
        PSIUDA = DA
        PSIUX = "U^Unit Dose"
        ^PSSGIU()
        if % == 1:
            DIE = "^PSDRUG("
            DR = "62.05;212.2"
            ^DIE
            DIE = "^PSDRUG("
            DR = "212"
            DR(2,50.0212) = ".01;1"
            ^DIE
            FLGOI = 1

def IV():
    if FLG3:
        print("\n** You are NOW editing IV fields. **")
        PSIUDA = DA
        PSIUX = "I^IV"
        ^PSSGIU()
        if % == 1:
            IV1()
            FLGOI = 1

def IV1():
    global PSSIVOUT
    PSSIVOUT = None
    print("\nEdit Additives or Solutions: ")
    DIR(0) = "SO^A:ADDITIVES;S:SOLUTIONS;"
    ^DIR
    if DIRUT in globals():
        return
    PSSASK = Y[0]
    if PSSASK == "ADDITIVES":
        ENA^PSSVIDRG()
    if PSSASK == "SOLUTIONS":
        ENS^PSSVIDRG()
    if not PSSIVOUT:
        IV1()
    del PSSIVOUT

def WS():
    if FLG4:
        print("\n** You are NOW editing WARD STOCK fields. **")
        DIE = "^PSDRUG("
        DR = "300;301;302"
        ^DIE

def DACCT():
    if FLG5:
        print("\n** You are NOW editing DRUG ACCOUNTABILITY fields. **")
        DIE = "^PSDRUG("
        DR = "441"
        ^DIE
        DIE = "^PSDRUG("
        DR = "9"
        DR(2,50.1) = "1;2;400;401;402;403;404;405"
        ^DIE

def CS():
    if FLG6:
        print("\n** You are NOW Marking/Unmarking for CONTROLLED SUBS. **")
        PSIUDA = DA
        PSIUX = "N^Controlled Substances"
        ^PSSGIU()

def NVM():
    if FLG7:
        print("\n** You are NOW Marking/Unmarking for NON-VA MEDS. **")
        PSIUDA = DA
        PSIUX = "X^Non-VA Med"
        ^PSSGIU()

def ASKCMOP():
    if ^XUSEC("PSXCMOPMGR", DUZ):
        print("\nDo you wish to mark to transmit to CMOP? ")
        ^DIR
        if "Nn" in X:
            return
        if "Yy" in X:
            PSXFL = 0
            TEXT^PSSMARK()
            H 7
            PSXUDA = DA
            PSXUM = DA
            PSXLOC = ^PSDRUG(DA)[0]
            PSXGOOD = 0
            PSXF = 0
            PSXBT = 0
            BLD^PSSMARK()
            PICK2^PSSMARK()
            DA = PSXUDA

def ASKCLOZ():
    print("\nDo you wish to mark/unmark as a LAB MONITOR or CLOZAPINE DRUG? ")
    ^DIR
    if "Nn" in X:
        return
    if "Yy" in X:
        MONCLOZ()

def MONCLOZ():
    global LMFLAG, CLFALG, WHICH
    WHICH = ^PSDRUG(DISPDRG, "CLOZ1")
    LMFLAG = 0
    CLFLAG = 0
    if WHICH == "PSOCLO1":
        CLFLAG = 1
    if WHICH != "PSOCLO1":
        if WHICH != "":
            LMFLAG = 1
    print("\nMark/Unmark for Lab Monitor or Clozapine: ")
    ^DIR
    if "Nn" in X:
        return
    if "Yy" in X:
        PSSAST = Y[0]
        if PSSAST == "LAB MONITOR":
            ^PSSLAB()
        if PSSAST == "CLOZAPINE":
            CLOZ()

def FLASH():
    global LMFLAG, CLFALG, WHICH
    WHICH = ^PSDRUG(DISPDRG, "CLOZ1")
    LMFLAG = 0
    CLFLAG = 0
    if WHICH == "PSOCLO1":
        CLFLAG = 1
    if WHICH != "PSOCLO1":
        if WHICH != "":
            LMFLAG = 1

def CLOZ():
    global NFLAG
    print("\n** You are NOW editing CLOZAPINE fields. **")
    if NFLAG:
        return
    if DTOUT:
        return
    ^PSSCLDRG()

def USE():
    PACK = ""
    if ^PSDRUG(DISPDRG, "PSG")[2]:
        PACK = "W"
    if ^PSDRUG(DISPDRG, 2):
        PACK += ^PSDRUG(DISPDRG, 2)[3]
    if PACK:
        print("\nThis entry is marked for the following PHARMACY packages: ", end="")
        USE1()

def USE1():
    if "O" in PACK:
        print("\n Outpatient")
    if "U" in PACK:
        print("\n Unit Dose")
    if "I" in PACK:
        print("\n IV")
    if "W" in PACK:
        print("\n Ward Stock")
    if "D" in PACK:
        print("\n Drug Accountability")
    if "N" in PACK:
        print("\n Controlled Substances")
    if "X" in PACK:
        print("\n Non-VA Med")
    if not PACK:
        print("\n NONE")
    if "O" not in PACK and "U" not in PACK and "I" not in PACK and "W" not in PACK and "D" not in PACK and "N" not in PACK and "X" not in PACK:
        print("\n NONE")

def WR():
    if not ("CMOP-" in ^XMB("NETNAME")):
        if OLDDF:
            print("\nThe dosage form has changed from", OLDDF, "to", NEWDF, "due to")
            print("matching/rematching to NDF.")
            print("You will need to rematch to Orderable Item.")

def PRIMDRG():
    global VAPROD
    if ^PS(59.7, 1, 20)[1] == 4 or ^PS(59.7, 1, 20)[1] == 4.5:
        if ^PSDRUG(DISPDRG, 2):
            VAR = ^PSDRUG(DISPDRG, 2)[3]
            if "U" in VAR or "I" in VAR:
                PRIM1()

def PRIM1():
    print("\nYou need to match this drug to \"PRIMARY DRUG\" file as well.")
    DIE = "^PSDRUG("
    DR = "64"
    DA = DISPDRG
    ^DIE
    VAR = None

def MF():
    if ^PS(59.7, 1, 80)[2] > 1:
        if ^PSDRUG(DISPDRG, 2):
            PSSOR = ^PSDRUG(DISPDRG, 2)[1]
            if PSSOR:
                EN^PSSPOIDT(PSSOR)
                EN2^PSSHL1(PSSOR, "MUP")

def MFA():
    if ^PS(59.7, 1, 80)[2] > 1:
        PSSOR = ^PS(52.6, ENTRY)[11]
        PSSDD = ^PS(52.6, ENTRY)[2]
        if PSSOR:
            EN^PSSPOIDT(PSSOR)
            EN2^PSSHL1(PSSOR, "MUP")
            MFDD()

def MFS():
    if ^PS(59.7, 1, 80)[2] > 1:
        PSSOR = ^PS(52.7, ENTRY)[11]
        PSSDD = ^PS(52.7, ENTRY)[2]
        if PSSOR:
            EN^PSSPOIDT(PSSOR)
            EN2^PSSHL1(PSSOR, "MUP")
            MFDD()

def MFDD():
    if ^PSDRUG(PSSDD, 2):
        PSSOR = ^PSDRUG(PSSDD, 2)[1]
        if PSSOR:
            EN^PSSPOIDT(PSSOR)
            EN2^PSSHL1(PSSOR, "MUP")

def OPEI():
    global DIE, DR
    DIE = "^PSDRUG("
    DR = "28"
    DA = DISPDRG
    ^DIE
    if int(^PSDRUG(DA, 6)):
        OPEI2()

def OPEI2():
    global DIE, DR
    DIE = "^PSDRUG("
    DR = "906"
    DA = DISPDRG
    ^DIE

def DEA():
    if int(^PSDRUG(DISPDRG, 3)):
        if ^PSDRUG(DISPDRG, 0)[3] in [1, 2]:
            DSH()

def DSH():
    print("\n****************************************************************************")
    print("This entry contains a \"1\" or a \"2\" in the \"DEA, SPECIAL HDLG\"")
    print("field, therefore this item has been UNMARKED for CMOP transmission.")
    print("****************************************************************************")
    ^PSDRUG(DISPDRG, 3)[1] = 0
    del ^PSDRUG("AQ", DISPDRG)
    DA = DISPDRG
    ^PSSREF()

def CPTIER(VAPID):
    # Called from PSSCOMMON Input Template
    # VAPID = IEN OF DRUG FILE #50
    PSSCP = $$CPTIER^PSNAPIS("", CPDATE, VAPID, 1)
    # PSSCP = Copay Tier^Effective Date^End Date
    print("Copay Tier:", PSSCP[1])
    print("Copay Effective Date:", PSSCP[2])

def GETTIER(PSSTDRUG):
    # called by DIC to get copay tier for today's date
    VAPID = PSSTDRUG
    PSSDRDAT = GETS^DIQ(50, PSSTDRUG, "2;22;51;6;100;101;102", "IE")
    PSSDRGCL = PSSDRDAT[50, PSSTDRUG, 2]
    PSSFSN = PSSDRDAT[50, PSSTDRUG, 6]
    PSSNFORM = PSSDRDAT[50, PSSTDRUG, 51]
    PSSINACT = PSSDRDAT[50, PSSTDRUG, 100]
    PSSMSG = PSSDRDAT[50, PSSTDRUG, 101]
    PSSRESTR = PSSDRDAT[50, PSSTDRUG, 102]
    VAPROD = PSSDRDAT[50, PSSTDRUG, 22]
    print(" ", PSSDRGCL)
    PSSCP = $$CPTIER^PSNAPIS(VAPROD, CPDATE, "", 1)
    print(" ", PSSFSN)
    print(" ", PSSNFORM)
    PSSFD = $$FDR^PSNACT(VAPROD)
    print(" ", PSSFD)
    if VAPROD and PSSCP[1]:
        print("  Tier", PSSCP[1])
    PSSCONVD = $$DATE(PSSINACT)
    print(" ", PSSCONVD)
    print(" ", PSSMSG)
    print(" ", PSSRESTR)

def DATE(PSSCONVD):
    # convert fileman date to mm/dd/yyyy
    return PSSCONVD[4:6] + "/" + PSSCONVD[6:8] + "/" + str(1700 + int(PSSCONVD[1:3]))

def FD(PSSTDRUG):
    PSSDRDAT = GETS^DIQ(50, PSSTDRUG, 22, "I")
    VAPROD = PSSDRDAT[50, PSSTDRUG, 22]
    if VAPROD != "":
        PSSFD = GET1^DIQ(50.68, VAPROD, 109)
        print("Formulary Designator:", PSSFD)
        if ^PSNDF(50.68, VAPROD, 5.1, 1, 0):
            FDT^PSNACT(VAPROD)