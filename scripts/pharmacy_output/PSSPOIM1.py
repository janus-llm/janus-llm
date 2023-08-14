def PSSPOIM1():
    CHK()
    END()

def CHK():
    global PSNO, PSMAN, PSNAME, SPHOLD, DOSEPTR, PSSP, PSMC, DIR, PSOUT
    PSNO = 0
    if PSMAN:
        print("\nMatching", PSNAME, "\n   to\n", SPHOLD, " ", ^PS(50.606,+DOSEPTR,0), "^")
    else:
        PSMC = ^PS(50.7,PSSP,0)
        print("\nMatching", PSNAME, "\n   to\n", PSMC, " ", ^PS(50.606,+$P(^PS(50.7,PSSP,0),"^",2),0), "^")
    DIR(0) = "Y"
    DIR("B") = "YES"
    DIR("A") = "Is this OK"
    ^DIR
    if Y == 0:
        PSNO = 1
    if Y != 1 and not PSNO:
        PSOUT = 1
    #Add trace of whether inactive date is present.
    #If one is added erroneously by code logic when the
    #orderable item should remain active,
    #the inactive date will be deleted at INACT^PSSPOIM1.
    ^TMP($J,"INACTIVE_DATE") = {}
    PSOITMP = PSPOINT if PSPOINT else PSSP
    if PSOITMP:
        ^TMP($J,"INACTIVE_DATE",PSOITMP) = $P(^PS(50.7,PSOITMP,0),"^",4)
    K PSMAN, PSOITMP

def END():
    ^TMP($J,"PSSOO") = {}
    PSSSSS = None
    PSCREATE = None
    ^TMP("PSSLOOP",$J) = {}
    ^TMP($J,"INACTIVE_DATE") = {}
    AAA = None
    ANS = None
    APLU = None
    COMM = None
    DA = None
    DIC = None
    DIE = None
    DOSEFORM = None
    DOSEFV = None
    DOSEPTR = None
    DR = None
    FFF = None
    MATCH = None
    NEWSP = None
    NODE = None
    NOFLAG = None
    OTH = None
    POINT = None
    PSCNT = None
    PSIEN = None
    PSMAN = None
    PSMC = None
    PSNAME = None
    PSNO = None
    PSSP = None
    PSND = None
    PSOUT = None
    SPHOLD = None
    SPR = None
    TMPTR = None
    TT = None
    VAGEN = None
    X = None
    Y = None
    ZZ = None
    PSOOOUT = None
    PSXDATE = None
    PSXADATE = None
    PSXSDATE = None
    AAAAA = None
    BBBBB = None
    ZXX = None
    PSXDDATE = None
    PSSDACT = None
    PSSSACT = None
    PSSAACT = None
    PSSINACT = None
    PSSDTENT = None
    PSSCOMP = None
    PSSDGDT = None
    PSSDGIDL = None
    PSSARR = None
    PSSACT = None
    PSSNEWIA = None

def MESS():
    print("\nThis option enables you to match Dispense Drugs to an entry in the Pharmacy")
    print("Orderable Item file, or create a new Pharmacy Orderable Item entry for a")
    print("Dispense Drug.")

def MESSZ():
    ^TMP("PSSLOOP",$J,DUZ) = {}
    print("\nThis option is for matching IV Additives, IV Solutions, and all Dispense Drugs")
    print("marked with an I, O, or U in the Application Packages' Use field to an")
    print("Orderable Item.")
    print("You will need to keep accessing this option until all drugs are matched.")
    print("A check will be done every time this option is exited to see if the matching")
    print("process is complete.")
    DIR(0) = "E"
    ^DIR
    if "^^" in X or "^^" in Y or "^^" in DIR("A"):
        PSOUT = 1

def CHECK():
    print("\n\nChecking Drug files, please wait...")
    X1 = DT
    X2 = -365
    C^%DTC
    PSZXDATE = X
    DONEFLAG = 1
    FFFF = 0
    while True:
        FFFF = ^PSDRUG(FFFF)
        if not FFFF or not DONEFLAG:
            break
        QQNM = $P(^PSDRUG(FFFF,0),"^")
        if QQNM != "" and "^PSDRUG(" in ^PSDRUG("B",QQNM):
            USAGE = $P(^PSDRUG(FFFF,2),"^",3)
            ZZG = 1
            PSZZDATE = +^PSDRUG(FFFF,"I")
            if PSZZDATE and PSZZDATE < PSZXDATE:
                ZZG = 0
        if DONEFLAG == 1:
            QQQ = 0
            while True:
                QQQ = ^PS(52.6,QQQ)
                if not QQQ or not DONEFLAG:
                    break
                PSZNAME = $P(^PS(52.6,QQQ,0),"^")
                if PSZNAME != "" and "^PS(52.6," in ^PS(52.6,"B",PSZNAME) and $P(^PS(52.6,QQQ,0),"^",2) and not $P(^(0),"^",11):
                    ZZG = 1
                    PSZZDATE = +^PS(52.6,QQQ,"I")
                    if PSZZDATE and PSZZDATE < PSZXDATE:
                        ZZG = 0
            if DONEFLAG:
                QQQ = 0
                while True:
                    QQQ = ^PS(52.7,QQQ)
                    if not QQQ or not DONEFLAG:
                        break
                    PSZNAME = $P(^PS(52.7,QQQ,0),"^")
                    if PSZNAME != "" and "^PS(52.7," in ^PS(52.7,"B",PSZNAME) and $P(^PS(52.7,QQQ,0),"^",2) and not $P(^(0),"^",11):
                        ZZG = 1
                        PSZZDATE = +^PS(52.7,QQQ,"I")
                        if PSZZDATE and PSZZDATE < PSZXDATE:
                            ZZG = 0
    if DONEFLAG == 1:
        QQQ = 0
        while True:
            QQQ = ^PS(52.7,QQQ)
            if not QQQ or not DONEFLAG:
                break
            PSZNAME = $P(^PS(52.7,QQQ,0),"^")
            if PSZNAME != "" and "^PS(52.7," in ^PS(52.7,"B",PSZNAME) and $P(^PS(52.7,QQQ,0),"^",2) and not $P(^(0),"^",11):
                ZZG = 1
                PSZZDATE = +^PS(52.7,QQQ,"I")
                if PSZZDATE and PSZZDATE < PSZXDATE:
                    ZZG = 0

def MAIL():
    print("\n\nYou are finished matching to the Orderable Item File!",)
    print("\nA clean-up job is being queued now, and when it is finished, you will",)
    print("receive a mail message informing you of its completion.",)
    DIR(0) = "E"
    ^DIR
    if "^^" in X or "^^" in Y or "^^" in DIR("A"):
        PSOUT = 1
    PSSOMAIL = 1
    PSOUDUZ = DUZ
    ZTRTN = "DATE^PSSPOIM1"
    ZTIO = ""
    ZTDTH = $H
    ZTDESC = "ORDERABLE ITEM CLEAN UP"
    ZTSAVE("DUZ") = ""
    ZTSAVE("PSSOMAIL") = ""
    ^%ZTLOAD

def OTHER():
    print("\n\nThere are other Dispense Drugs with the same VA Generic Name and same Dose")
    print("Form already matched to orderable items. Choose a number to match, or enter")
    print("'^' to enter a new one.",)
    print("\n\nDisp. drug -> ", PSNAME, "!")

def EN(PSVAR):
    PSSDACT = None
    PSSSACT = None
    PSSAACT = None
    PSSINACT = None
    PSSDTENT = None
    print("\n\nNow editing Orderable Item:")
    print("\n\n", $P(^PS(50.7,PSVAR,0),"^"), "   ", $P($G(^PS(50.606,+$P(^(0),"^",2),0)),"^"),)
    print("\n")
    DIE = "^PS(50.7,"
    DA = PSVAR
    DR = "5;6"
    ^DIE
    if "^^" in X or "^^" in Y or "^^" in DIR("A"):
        return
    INACT()
    if "^^" in X or "^^" in Y or "^^" in DIR("A"):
        return
    EN1()

def INACT():
    DIE = "^PS(50.7,"
    DA = PSVAR
    PSSNEWIA = ""
    if $G(PSBEFORE):
        Y = PSBEFORE
        DD^%DT
        DIR("B") = Y
    DIR(0) = "DO"
    DIR("A") = "INACTIVE DATE"
    ^DIR
    if "^^" in X or "^^" in Y or "^^" in DIR("A"):
        return
    if $G(PSBEFORE):
        DIE = "^PS(50.7,"
        DA = PSVAR
        DR = ".04////@"
        ^DIE
        if $P(^PS(50.7,PSVAR,0),"^",4) == "":
            print("\n\nAll Drugs/Additives/Solutions matched to this")
            print("Orderable Item are inactive.")
            print("\n\nThe INACTIVE DATE cannot be deleted.")
    if PSSNEWIA:
        DIE = "^PS(50.7,"
        DA = PSVAR
        DR = ".04////"_PSSNEWIA
        ^DIE
    PSSINACT = $P(^PS(50.7,PSVAR,0),"^",4)
    if PSSINACT == "":
        return
    if not PSSNEWIA:
        print("\n\nThe Inactive Date is: ",)
        Y = PSSINACT
        DD^%DT
        print(Y, ".")
    return

def INACT1():
    PSSNEWIA = ""
    DIR(0) = "DO"
    DIR("A") = "INACTIVE DATE"
    ^DIR
    if "^^" in X or "^^" in Y or "^^" in DIR("A"):
        return
    DIE = "^PS(50.7,"
    DA = PSVAR
    PSSNEWIA = Y
    if $G(PSBEFORE):
        DIE = "^PS(50.7,"
        DA = PSVAR
        DR = ".04////@"
        ^DIE
        if $P(^PS(50.7,PSVAR,0),"^",4) == "":
            print("\n\nAll Drugs/Additives/Solutions for this orderable item")
            print("are inactive.")
            print("\n\nThe INACTIVE DATE cannot be deleted.")
    if PSSNEWIA:
        DIE = "^PS(50.7,"
        DA = PSVAR
        DR = ".04////"_PSSNEWIA
        ^DIE
    PSSINACT = $P(^PS(50.7,PSVAR,0),"^",4)
    if PSSINACT == "":
        return
    if not PSSNEWIA:
        print("\n\nThe Inactive Date is: ",)
        Y = PSSINACT
        DD^%DT
        print(Y, ".")
    return

def IACHK():
    PSSCOMP = ""
    PSSACT = 0
    while True:
        PSSCOMP = ^PS(50.7,"A50",PSVAR,PSSCOMP)
        if PSSCOMP == "":
            break
        PSSARR(PSSCOMP) = ""
    PSSDGIDL = ""
    while True:
        PSSCOMP = ^PSSARR(PSSCOMP)
        if PSSCOMP == "":
            break
        PSSDGDT = ^PSDRUG(PSSCOMP,"I")
        if PSSDGDT == "":
            PSSACT = 1
        if PSSDGDT > PSSDGIDL:
            PSSDGIDL = PSSDGDT
    return

def IACHK1():
    if PSSDGIDL != "" and not PSSACT:
        Y = PSSDGIDL
        DD^%DT
        if PSSDGIDL < PSSINACT:
            print("\n\n**** **** NOTE **** ****",)
            print("\n\nAll Drugs/Additives/Solutions for this orderable item")
            print("are inactive as of ", Y, ".",)
            Y = $P(^PS(50.7,PSVAR,0),"^",4)
            DD^%DT
            print("\n\nHowever, the orderable item ", $P(^PS(50.7,PSVAR,0),"^"),)
            print("\nis inactive on ", Y, ".",)
            print("\n\nYou may need to change the inactive date on the orderable item")
            print("using option PSS EDIT ORDERABLE ITEMS.",)
            print("\n\n****    ****    ****    ****    ****",)
        else:
            print("\n\nAll Drugs/Additives/Solutions matched to this",)
            print("Orderable Item are inactive as of ", Y, ".",)
    return

def EN1():
    PSSDTENT = PSSINACT
    PSSOTH = $P(^PS(59.7,1,40.2),"^")
    DIE = "^PS(50.7,"
    DA = PSVAR
    DR = "D LIND^PSSPOIMO;14;13;14.1T;14.2"
    ^DIE
    IMMUN()
    SYN()
    FIN()
    return

def IMMUN():
    if ^PSDRUG("AOC",PSVAR,"IM000") != "IM":
        return
    DIE = "^PS(50.7,"
    DA = PSVAR
    DR = 9
    ^DIE
    return

def SYN():
    if "^^" in X or "^^" in Y or "^^" in DIR("A"):
        return
    DIC = "^PS(50.7,"
    if not ^PS(50.7,PSVAR,2,0):
        ^PS(50.7,PSVAR,2,0) = "^50.72^0^0"
    DIC = "^PS(50.7,"_PSVAR_",2,"
    DA(1) = PSVAR
    DIC(0) = "QEAMZL"
    DIC("A") = "Select SYNONYM: "
    DLAYGO = 50.72
    ^DIC
    if Y < 0 or "^^" in X or "^^" in Y or "^^" in DIR("A"):
        if not ^PS(50.7,PSVAR,2,0):
            ^PS(50.7,PSVAR,2,0) = "^50.72^0^0"
        PSSNOOI = 1
    else:
        DA = +Y
        DIE = "^PS(50.7,"_PSVAR_",2,"
        DA(1) = PSVAR
        DR = .01
        ^DIE
        SYN()
    return

def FIN():
    ^TMP($J,"PSSOO") = {}
    PSSSSS = None
    PSCREATE = None
    ^TMP("PSSLOOP",$J) = {}
    ^TMP($J,"INACTIVE_DATE") = {}
    AAA = None
    ANS = None
    APLU = None
    COMM = None
    DA = None
    DIC = None
    DIE = None
    DOSEFORM = None
    DOSEFV = None
    DOSEPTR = None
    DR = None
    FFF = None
    MATCH = None
    NEWSP = None
    NODE = None
    NOFLAG = None
    OTH = None
    POINT = None
    PSCNT = None
    PSIEN = None
    PSMAN = None
    PSMC = None
    PSNAME = None
    PSNO = None
    PSSP = None
    PSND = None
    PSOUT = None
    SPHOLD = None
    SPR = None
    TMPTR = None
    TT = None
    VAGEN = None
    X = None
    Y = None
    ZZ = None
    PSOOOUT = None
    PSXDATE = None
    PSXADATE = None
    PSXSDATE = None
    AAAAA = None
    BBBBB = None
    ZXX = None
    PSXDDATE = None
    PSSDACT = None
    PSSSACT = None
    PSSAACT = None
    PSSINACT = None
    PSSDTENT = None
    PSSCOMP = None
    PSSDGDT = None
    PSSDGIDL = None
    PSSARR = None
    PSSACT = None
    PSSNEWIA = None
    if PSCREATE:
        ^TMP($J,"PSSOO") = {}
        PSSSSS = None
        ^TMP("PSSLOOP",$J) = {}
        ^TMP($J,"INACTIVE_DATE") = {}
        AAA = None
        ANS = None
        APLU = None
        COMM = None
        DA = None
        DIC = None
        DIE = None
        DOSEFORM = None
        DOSEFV = None
        DOSEPTR = None
        DR = None
        FFF = None
        MATCH = None
        NEWSP = None
        NODE = None
        NOFLAG = None
        OTH = None
        POINT = None
        PSCNT = None
        PSIEN = None
        PSMAN = None
        PSMC = None
        PSNAME = None
        PSNO = None
        PSSP = None
        PSND = None
        PSOUT = None
        SPHOLD = None
        SPR = None
        TMPTR = None
        TT = None
        VAGEN = None
        X = None
        Y = None
        ZZ = None
        PSOOOUT = None
        PSXDATE = None
        PSXADATE = None
        PSXSDATE = None
        AAAAA = None
        BBBBB = None
        ZXX = None
        PSXDDATE = None
        PSSDACT = None
        PSSSACT = None
        PSSAACT = None
        PSSINACT = None
        PSSDTENT = None
        PSSCOMP = None
        PSSDGDT = None
        PSSDGIDL = None
        PSSARR = None
        PSSACT = None
        PSSNEWIA = None
    PSSITE = +$O(^PS(59.7,0))
    ^PS(59.7,PSSITE,80) = "^2"
    ^%ZISC
    ^TMP($J,"PSSOO") = {}
    PSSSSS = None
    PSCREATE = None
    ^TMP("PSSLOOP",$J) = {}
    ^TMP($J,"INACTIVE_DATE") = {}
    AAA = None
    ANS = None
    APLU = None
    COMM = None
    DA = None
    DIC = None
    DIE = None
    DOSEFORM = None
    DOSEFV = None
    DOSEPTR = None
    DR = None
    FFF = None
    MATCH = None
    NEWSP = None
    NODE = None
    NOFLAG = None
    OTH = None
    POINT = None
    PSCNT = None
    PSIEN = None
    PSMAN = None
    PSMC = None
    PSNAME = None
    PSNO = None
    PSSP = None
    PSND = None
    PSOUT = None
    SPHOLD = None
    SPR = None
    TMPTR = None
    TT = None
    VAGEN = None
    X = None
    Y = None
    ZZ = None
    PSOOOUT = None
    PSXDATE = None
    PSXADATE = None
    PSXSDATE = None
    AAAAA = None
    BBBBB = None
    ZXX = None
    PSXDDATE = None
    PSSDACT = None
    PSSSACT = None
    PSSAACT = None
    PSSINACT = None
    PSSDTENT = None
    PSSCOMP = None
    PSSDGDT = None
    PSSDGIDL = None
    PSSARR = None
    PSSACT = None
    PSSNEWIA = None
    if PSSOMAIL:
        PSOTEXT(1) = "You have completed the matching process required for the installation of"
        PSOTEXT(2) = "Outpatient V. 7.0 and Inpatient Medications V. 5.0!"
        XMDUZ = .5
        XMY(DUZ) = ""
        XMTEXT = "PSOTEXT("
        XMSUB = "Pharmacy Orderable Item File"
        ^XMD
        PSSITE = +$O(^PS(59.7,0))
        ^PS(59.7,PSSITE,80) = "^2"
        ^%ZISC
        PSSOMAIL = None
    PSOTYPE = None
    DA = None
    DIE = None
    WW = None
    RRRR = None
    PSDFLAG = None
    PSAPPL = None
    GGG = None
    HHH = None
    ZZZZZ = None

def DATE():
    ZZZ = 0
    while True:
        ZZZ = ^PS(50.7,ZZZ)
        if not ZZZ:
            break
        PSOTYPE = $P(^PS(50.7,ZZZ,0),"^",3)
        if PSOTYPE and not ^PS(52.6,"AOI",ZZZ) and not ^PS(52.7,"AOI",ZZZ) and not $P(^PS(50.7,ZZZ,0),"^",4):
            DIE = "^PS(50.7,"
            DA = ZZZ
            DR = ".04////"_DT
            ^DIE
    ZZZ = 0
    while True:
        ZZZ = ^PS(52.7,ZZZ)
        if not ZZZ:
            break
        RRRR = $P(^PS(52.7,ZZZ,0),"^",11)
        if RRRR and not $P(^PS(50.7,RRRR,0),"^",3):
            DIE = "^PS(52.7,"
            DA = ZZZ
            DR = "9////"_"@"
            ^DIE
    ZZZ = 0
    while True:
        ZZZ = ^PS(52.6,ZZZ)
        if not ZZZ:
            break
        RRRR = $P(^PS(52.6,ZZZ,0),"^",11)
        if RRRR and not $P(^PS(50.7,RRRR,0),"^",3):
            DIE = "^PS(52.6,"
            DA = ZZZ
            DR = "15////"_"@"
            ^DIE
    if PSCREATE:
        MAIL^PSSCREAT
    if not PSSOMAIL:
        PSOTYPE = None
        DA = None
        DIE = None
        WW = None
        RRRR = None
        PSDFLAG = None
        PSAPPL = None
        GGG = None
        HHH = None
        ZZZZZ = None
        PSOTEXT = None
        XMDUZ = None
        XMY = None
        XMTEXT = None
        XMSUB = None
        PSSITE = None

PSSPOIM1()