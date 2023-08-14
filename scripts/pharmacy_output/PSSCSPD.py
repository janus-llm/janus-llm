def PSSCSPD():
    print("Since this report must check every drug in the DRUG (#50) File, we recommend")
    print("that you queue this report to a printer.")
    IOP, %ZIS, POP = None, None, None
    %ZIS = "QM"
    %ZIS = "^%ZIS"
    if POP:
        print("Nothing queued to print.")
        return
    if IO("Q"):
        ZTRTN = "START^PSSCSPD"
        ZTDESC = "Corresponding drug report"
        ^%ZTLOAD = [ZTRTN, ZTDESC]
        %ZIS = None
        print("Report queued to print.")
        return

def START():
    U = None
    U = IO
    ^TMP($J,"PSSC") = None
    PSSOUT, PSSHV, PSSONE = 0, 0, 0
    PSSDV = "C" if IOST[0] == "C" else "P"
    PSSCT = 1
    PSSLINE = "-" * 78
    HDC()
    PSSN = None
    for PSSN in ^PSDRUG("B"):
        if PSSN is None or PSSOUT:
            break
        PSSIEN = None
        for PSSIEN in ^PSDRUG("B", PSSN):
            if not PSSIEN or PSSOUT:
                break
            if not ^PSDRUG(PSSIEN):
                continue
            PSSINDTE = 0
            if ^PSDRUG(PSSIEN,"I") and ^PSDRUG(PSSIEN,"I") <= DT:
                PSSINDTE = 1
            PSSNODE = ^PSDRUG(PSSIEN,8)
            if not PSSNODE[4] and not PSSNODE[5]:
                continue
            if ($Y + 5) > IOSL:
                HDC()
                if PSSOUT:
                    break
            PSSONE = 1
            print("\n" + ^PSDRUG(PSSIEN,0))
            if ($Y + 5) > IOSL:
                HDC()
                if PSSOUT:
                    break
            PSSUSE = ^PSDRUG(PSSIEN,2)[2]
            PSSI = None
            PSSO = None
            PSSOX = None
            PSSIX = None
            if PSSNODE[4]:
                print(" " * 3 + "Corresponding Outpatient drug: " + " " * 36 + ^PSDRUG(PSSNODE[4],0))
                PSSOX = PSSNODE[4]
                if not PSSOX or not ^PSDRUG(PSSOX,0):
                    continue
                if not ^PSDRUG(PSSOX,8)[5]:
                    continue
                if ^TMP($J,"PSSC",$G(^PSDRUG(PSSOX,0)),1):
                    continue
                if PSSINDTE:
                    continue
                if PSSUSE[0] == "I" or PSSUSE[0] == "U":
                    ^TMP($J,"PSSC",$G(^PSDRUG(PSSOX,0)),1) = ^PSDRUG(PSSIEN,0)
            if PSSNODE[5]:
                print(" " * 3 + " Corresponding Inpatient drug: " + " " * 36 + ^PSDRUG(PSSNODE[5],0))
                PSSIX = PSSNODE[5]
                if not PSSIX or not ^PSDRUG(PSSIX,0):
                    continue
                if not ^PSDRUG(PSSIX,8)[4]:
                    continue
                if ^TMP($J,"PSSC",$G(^PSDRUG(PSSIX,0)),2):
                    continue
                if PSSINDTE:
                    continue
                if PSSUSE[1] == "O":
                    ^TMP($J,"PSSC",$G(^PSDRUG(PSSIX,0)),2) = ^PSDRUG(PSSIEN,0)
    if not PSSOUT and not PSSONE:
        print(" " * 5 + "No Corresponding Drugs were found.")
    if PSSOUT:
        return
    PSSHV = 1
    if PSSCT == 1:
        PSSCT = 2
    HDC()
    if PSSOUT:
        return
    if not ^TMP($J,"PSSC"):
        print("\n" + " " * 5 + "There are no potential matches!")
        return
    PSSNM = None
    for PSSNM in ^TMP($J,"PSSC"):
        if PSSNM is None or PSSOUT:
            break
        if ($Y + 5) > IOSL:
            HDC()
            if PSSOUT:
                break
        print("\n" + PSSNM)
        if ($Y + 5) > IOSL:
            HDC()
            if PSSOUT:
                break
        if ^TMP($J,"PSSC",PSSNM)[2]:
            print(" ** Potential corr. Outpatient Drug: " + ^TMP($J,"PSSC",PSSNM,2))
        if ^TMP($J,"PSSC",PSSNM)[1]:
            print(" **  Potential corr. Inpatient Drug: " + ^TMP($J,"PSSC",PSSNM,1))

def HDC():
    if PSSDV == "C" and PSSCT != 1:
        Y = input("Press Return to continue, '^' to exit")
        if not Y:
            PSSOUT = 1
            return
    print("Current Corresponding Inpatient/Outpatient Drug Matches" if not PSSHV else " *** Potential Corresponding Inpatient/Outpatient Drug Matches", " " * 68, "PAGE: " + str(PSSCT))
    print(PSSLINE)
    PSSCT += 1

def EDIT():
    DIC = None
    DIC = "^PSDRUG("
    DIC(0) = "QEAMZ"
    DIC("A") = "Select Drug: "
    ^DIC = DIC
    if Y < 1 or DTOUT or DUOUT:
        return
    PSSI = +Y
    PSSN = ^PSDRUG(PSSI,0)
    PSSA = ^PSDRUG(PSSI,2)[2]
    print("\n" + "This entry is marked for the following PHARMACY packages:")
    if PSSA[0] == "O":
        print(" Outpatient")
    if PSSA[1] == "U":
        print(" Unit Dose")
    if PSSA[0] == "I":
        print(" IV")
    if PSSA[0] == "W":
        print(" Ward Stock")
    if PSSA[0] == "N":
        print(" Controlled Substances")
    if PSSA[0] == "O" and (PSSA[0] == "I" or PSSA[0] == "U"):
        Y = input("Press Return to continue")
        if not Y:
            return
    if PSSA[0] != "O" and PSSA[1] != "U" and PSSA[0] != "I" and PSSA[0] != "W" and PSSA[0] != "N":
        print(" (none)")
    if PSSA[0] != "O":
        DIE = None
        DA = PSSI
        DIE = "^PSDRUG("
        DR = 62.05
        ^DIE = [DA, DR]
        if Y or DTOUT:
            return
    if PSSA[0] != "I" and PSSA[1] != "U":
        DIE = None
        DA = PSSI
        DIE = "^PSDRUG("
        DR = 905
        ^DIE = [DA, DR]

def PAT():
    DIC = None
    DIC(0) = "QEAMZ"
    DIC("A") = "Select Pharmacy Orderable Item: "
    DIC = "^PS(50.7,"
    ^DIC = DIC
    if Y < 1 or DTOUT or DUOUT:
        return
    PSSOTH = 1 if ^PS(59.7,1,40.2) else 0
    DIE = None
    DA = +Y
    DIE = "^PS(50.7,"
    DR = "7"
    DR += "S:'$G(PSSOTH) Y=""@1"""
    DR += "7.1"
    DR += "@1"
    ^DIE = [DA, DR]
    if Y or DTOUT:
        return
    PAT()

def MARK():
    print("\n" + "This option will automatically mark all corresponding Inpatient and Outpatient")
    print("drugs that are listed in the 'Potential Corresponding Inpatient/Outpatient Drug")
    print("Matches' section of the 'Report of Corresponding Drugs'.")
    print("\n" + "Before using this option, please make sure you print a current 'Report of")
    print("Corresponding Drugs' for review.")
    DIR(0) = "Y"
    DIR("A") = "Mark potential corresponding drugs"
    DIR("B") = "Y"
    DIR("?") = " "
    DIR("?",1) = "Enter 'Yes' to mark corresponding inpatient and outpatient drugs as displayed"
    DIR("?",2) = "in the 'Potential Corresponding Inpatient/Outpatient Drug Matches' section of"
    DIR("?",3) = "the 'Report of Corresponding Drugs'."
    ^DIR = DIR
    if Y != 1:
        return
    print("\n" + "This job must be queued. You will receive a mail message upon completion.")
    ZTDTH = None
    ZTIO = ""
    ZTRTN = "MARKT^PSSCSPD"
    ZTDESC = "AUTO-MARK CORRESPONDING DRUGS"
    PSSDUZX = DUZ
    ^%ZTLOAD = [ZTRTN, ZTDESC]
    if not ZTSK:
        print("\n" + "Nothing queued.")
    PSSDUZX = None

def MARKT():
    PSSN = None
    for PSSN in ^PSDRUG("B"):
        if PSSN is None:
            continue
        PSSIEN = None
        for PSSIEN in ^PSDRUG("B", PSSN):
            if not PSSIEN:
                continue
            if not ^PSDRUG(PSSIEN):
                continue
            if ^PSDRUG(PSSIEN,"I") and ^PSDRUG(PSSIEN,"I") <= DT:
                continue
            PSSNODE = ^PSDRUG(PSSIEN,8)
            if not PSSNODE[4] and not PSSNODE[5]:
                continue
            PSSUSE = ^PSDRUG(PSSIEN,2)[2]
            if PSSNODE[4]:
                ^PSDRUG(PSSNODE[4],8)[6] = PSSIEN
            if PSSNODE[5]:
                ^PSDRUG(PSSNODE[5],8)[5] = PSSIEN
    if not PSSDUZX:
        GOTO MMM
    XMDUZ = "PHARMACY DATA MANAGEMENT"
    XMY(PSSDUZX) = ""
    XMSUB = "PDM CORRESPONDING DRUGS"
    PSSXTEXT(1) = "The PDM job that automatically marks corresponding inpatient and"
    PSSXTEXT(2) = "outpatient drugs is complete."
    XMTEXT = PSSXTEXT
    ^XMD = [XMDUZ, XMY, XMSUB, XMTEXT]
    PSSXTEXT = None
    XMDUZ = None
    XMY = None
    XMSUB = None
    XMTEXT = None

MMM:
    PSSI = None
    PSSO = None
    PSSOX = None
    PSSIX = None
    if PSSDUZX:
        PSSDUZX = None
    if ZTQUEUED:
        ZTREQ = "@"

def PSSCSPD():
    PSSCSPD()
    START()
    EDIT()
    PAT()
    MARK()
    MARKT()