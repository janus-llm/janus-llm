def PSSDACS():
    # BIR/WRT-loops thru file 50 and sends MM message if a "N" is in APPLICATION PACKAGES' USE field ; 10/22/97 15:21
    # 1.0;PHARMACY DATA MANAGEMENT;**3**;9/30/97
    # POST-INSTALL ROUTINE

    # Initialize variables
    K ^TMP($J,"PSSBT")
    D SETOP,START,REBD
    N DIFROM
    D MESS
    
    # Clean up
    K NBR, PSSDUZ, NM
    Q

def SETOP():
    ^TMP($J,"PSSBT","*1",1) = "The following entries need to be reviewed as to how they are marked package-"
    ^TMP($J,"PSSBT","*2",2) = "wise as to Drug Accountability/Inventory Interface vs. Controlled Substances."
    ^TMP($J,"PSSBT","*3",3) = "If entries need to be marked or unmarked, use the ""Controlled Substances Menu""."
    ^TMP($J,"PSSBT","*4",4) = "Select ""Supervisor (CS) Menu"", then select ""Set Up CS (Build Files) Menu""."
    ^TMP($J,"PSSBT","*5",5) = "Select ""Enter/Edit Menu"" and then select ""Mark/Unmark for Controlled SubstancesUse"" option."
    ^TMP($J,"PSSBT","*6",6) = "  "
    ^TMP($J,"PSSBT","*7",7) = "  "
    return

def START():
    NM = ""
    while NM != "":
        NM = $O(^PSDRUG("B", NM))
        if NM != "":
            NBR = $O(^PSDRUG("B", NM, 0))
            if $P($G(^PSDRUG(NBR, 2)), "^", 3) == "N":
                SETIT(NBR)
    return

def SETIT(NBR):
    ^TMP($J,"PSSBT", $P(^PSDRUG(NBR, 0), "^"), NBR) = $P(^PSDRUG(NBR, 0), "^")
    return

def REBD():
    NME = ""
    while NME != "":
        NME = $O(^TMP($J,"PSSBT", NME))
        if NME != "":
            NDA = $O(^TMP($J,"PSSBT", NME, 0))
            NUM = $S('$D(NUM):9, 1:NUM + 1)
            ^TMP($J,"PSSWRT", NUM, 0) = $P(^TMP($J,"PSSBT", NME, NDA), "^")
    return

def MESS():
    XMDUZ = "PHARMACY DATA MANAGEMENT PACKAGE"
    XMSUB = "DRUGS TO BE REVIEWED (DA vs CS)"
    XMTEXT = "^TMP($J,""PSSWRT"","
    XMY(DUZ) = ""

    if $D(^XUSEC("PSAMGR")):
        PSSDUZ = 0
        while PSSDUZ != 0:
            PSSDUZ = $O(^XUSEC("PSAMGR", PSSDUZ))
            if PSSDUZ != 0:
                XMY(PSSDUZ) = ""

    if $D(^XUSEC("PSA ORDERS")):
        PSSDUZ = 0
        while PSSDUZ != 0:
            PSSDUZ = $O(^XUSEC("PSA ORDERS", PSSDUZ))
            if PSSDUZ != 0:
                XMY(PSSDUZ) = ""

    if $D(^XUSEC("PSDMGR")):
        PSSDUZ = 0
        while PSSDUZ != 0:
            PSSDUZ = $O(^XUSEC("PSDMGR", PSSDUZ))
            if PSSDUZ != 0:
                XMY(PSSDUZ) = ""

    D ^XMD
    K ^TMP($J,"PSSBT"), ^TMP($J,"PSSWRT"), XMY, NUM, XMDUZ, XMTEXT, PSSDUZ, XMSUB
    return

PSSDACS()