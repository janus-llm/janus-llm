def ALL(PSSIEN, PSSFT, PSSFL, PSSPK, LIST):
    """
    PSSIEN - IEN of entry in MEDICATION ROUTES file (#51.2).
    PSSFT - Free Text name in MEDICATION ROUTES file (#51.2).
    PSSFL - Inactive flag - "" - All entries
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    PSSPK - PACKAGE USE field (#3) of the MEDICATION ROUTES file (#51.2).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is
    the Field Number of the data piece being returned.
    Returns NAME field (#.01), ABBREVIATION field (#1), PACKAGE USE field (#3), OUTPATIENT EXPANSION field (#4),
    OTHER LANGUAGE EXPANSION field (#4.1), INACTIVATION DATE field (#5), and IV FLAG field (#6)
    of MEDICATION ROUTES file (#51.2).
    """
    import datetime

    DIERR = None
    ZZERR = None
    PSS51P2 = None
    SCR = {"S": ""}
    PSS = None
    PSSBGCNT = 0
    PSSCNT = None
    PSSTIEN = None
    PSSTMP = None
    PSSNAM = None
    PSSCAP = None

    PSSBGCNT = 0
    SCR["S"] = ""
    if not LIST:
        return
    del ^TMP("DILIST", $J)
    del ^TMP($J, LIST)
    if not PSSIEN and not PSSFT:
        ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"
        return
    SCR["S"] = ""
    if PSSFL > 0:
        ND = None
        SETSCRN()
    if PSSIEN > 0:
        PSSIEN2 = FIND1(51.2, "", "A", "`" + PSSIEN, "", SCR["S"], "")
        if PSSIEN2 > 0:
            DIRREAD()
        COUNTBG()
    if PSSIEN == 0:
        if PSSFT == "??":
            LOOPDIR()
            COUNTBG()
        else:
            FIND(51.2, "", "@;.01;1", "QP", PSSFT, "", "B^C", SCR["S"], "", "")
            LOOPDI()
            COUNTBG()

def COUNTBG():
    """
    CHECKS PSSBGCNT AND FILLS COUNT IN ON 0 NODE OF ^TMP($J,LIST)
    """
    if PSSBGCNT > 0:
        ^TMP($J, LIST, 0) = PSSBGCNT
    else:
        ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"

def LOOPDI():
    """
    LOOPS ON "DILIST" FROM FILEMAN CALL (USED FOR RETURNING MULTIPLE DRUGS FROM PSSFT)
    """
    PSSTIEN = 0  # TEMP IEN TO ITERATE OVER DILIST
    while True:
        PSSTIEN = PSSTIEN + 1
        if PSSTIEN == "":
            break
        PSSIEN2 = ^TMP("DILIST", $J, PSSTIEN, 0)
        DIRREAD()

def LOOPDIR():
    """
    LOOP FOR A DIRECT READ.  READS ALL IENs FOR ^PSDRUG(
    """
    PSSIEN2 = 0
    while True:
        PSSIEN2 = PSSIEN2 + 1
        if not PSSIEN2:
            break
        DIRALL()

def DIRALL():
    """
    TEST FOR PSSFL, PSSPK, BAILS IF CONDITIONS MEET TRUE
    """
    if PSSFL and ^PS(51.2, PSSIEN2, 0)[5] and ^PS(51.2, PSSIEN2, 0)[5] <= PSSFL:
        return
    PSSZ5 = 0
    PSSZ6 = 0
    while True:
        PSSZ6 = PSSZ6 + 1
        if PSSZ6 > len(PSSPK) or PSSZ5:
            break
        if ^PS(51.2, PSSIEN2, 0)[4].contains(PSSPK[PSSZ6]):
            PSSZ5 = 1
    if PSSPK and not PSSZ5:
        return
    DIRREAD()

def DIRREAD():
    """
    MAIN DIRECT READ FOR ENTIRE ROUTINE
    """
    PSSNAM = ^PS(51.2, PSSIEN2, 0)[0]
    ^TMP($J, LIST, PSSIEN2, .01) = PSSNAM
    ^TMP($J, LIST, PSSIEN2, 1) = ^PS(51.2, PSSIEN2, 0)[2]
    PSSTMP = ^PS(51.2, PSSIEN2, 0)[3]
    if PSSTMP == "0":
        ^TMP($J, LIST, PSSIEN2, 3) = PSSTMP + "^" + "NATIONAL DRUG FILE ONLY"
    elif PSSTMP == "1":
        ^TMP($J, LIST, PSSIEN2, 3) = PSSTMP + "^" + "ALL PACKAGES"
    elif PSSTMP == "":
        ^TMP($J, LIST, PSSIEN2, 3) = ""
    ^TMP($J, LIST, PSSIEN2, 4) = ^PS(51.2, PSSIEN2, 0)[1]
    ^TMP($J, LIST, PSSIEN2, 4.1) = ^PS(51.2, PSSIEN2, 0)[6]
    if ^PS(51.2, PSSIEN2, 0)[5]:
        PSSCAP = uppercase(format(^PS(51.2, PSSIEN2, 0)[5]))
        ^TMP($J, LIST, PSSIEN2, 5) = ^PS(51.2, PSSIEN2, 0)[5] + "^" + PSSCAP
    else:
        ^TMP($J, LIST, PSSIEN2, 5) = ""
    PSSTMP = ^PS(51.2, PSSIEN2, 0)[6]
    if PSSTMP == "0" or PSSTMP == "":
        ^TMP($J, LIST, PSSIEN2, 6) = PSSTMP + "^" + "NO"
    elif PSSTMP == "1":
        ^TMP($J, LIST, PSSIEN2, 6) = PSSTMP + "^" + "YES"
        ^TMP($J, LIST, "IV", PSSNAM, PSSIEN2) = ""
    elif PSSTMP == "":
        ^TMP($J, LIST, PSSIEN2, 6) = ""
    ^TMP($J, LIST, "B", ^PS(51.2, PSSIEN2, 0)[0], PSSIEN2) = ""
    PSSAB = ^PS(51.2, PSSIEN2, 0)[2]
    if PSSAB:
        ^TMP($J, LIST, "C", PSSAB, PSSIEN2) = ""
    PSSTMP = ^PS(51.2, PSSIEN2, 0)[7]
    ^TMP($J, LIST, PSSIEN2, 7) = PSSTMP
    if PSSTMP:
        ^TMP($J, LIST, PSSIEN2, 7) = PSSTMP + "^" + ("YES" if PSSTMP else "NO")
    PSSTMP = ^PS(51.2, PSSIEN2, 0)[8]
    ^TMP($J, LIST, PSSIEN2, 8) = PSSTMP
    if PSSTMP:
        ^TMP($J, LIST, PSSIEN2, 8) = PSSTMP + "^" + ("YES" if PSSTMP else "NO")
    PSSBGCNT = PSSBGCNT + 1

def SETSCRN():
    """
    Set Screen for inactive Medication Routes
    """
    SCR["S"] = "ND = ^PS(51.2, +Y, 0)[5] if ND == '' or ND > PSSFL"

def NAME(PSSFT, PSSPK, LIST):
    """
    PSSFT - Free Text name in MEDICATION ROUTES file (#51.2).
    PSSPK - PACKAGE USE field (#3) of the MEDICATION ROUTES file (#51.2).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is
    the Field Number of the data piece being returned.
    Returns NAME field (#.01), ABBREVIATION field (#1), and INACTIVATION DATE field (#5)
    of MEDICATION ROUTES file (#51.2).
    """
    DIERR = None
    ZZERR = None
    PSS51P2 = None
    SCR = {"S": ""}
    PSS = None

    if not LIST:
        return
    del ^TMP($J, LIST)
    if not PSSFT:
        ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"
        return
    SCR["S"] = "I ^PS(51.2, +Y, 0)[4] = PSSPK" if PSSPK else ""
    if PSSFT == "??":
        LOOP(2)
        return
    FIND(51.2, "", "@;.01;1", "QP", PSSFT, "", "B", SCR["S"], "", "")
    if +^TMP("DILIST", $J, 0) == 0:
        ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"
        return
    ^TMP($J, LIST, 0) = +^TMP("DILIST", $J, 0)
    PSSXX = 0
    while True:
        PSSXX = PSSXX + 1
        if not PSSXX:
            break
        PSSIEN = +^TMP("DILIST", $J, PSSXX, 0)
        del ^TMP("PSS51P2", $J)
        GETS(51.2, +PSSIEN, ".01;1;5", "IE", "^TMP(""PSS51P2"",$J)")
        PSS = 0
        while True:
            PSS = PSS + 1
            if not PSS:
                break
            SETZRO()

def IEN(PSSABBR, LIST):
    """
    PSSABBR - ABBREVIATION field (#1) in MEDICATION ROUTES file (#51.2).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is
    the Field Number of the data piece being returned.
    Returns NAME field (#.01), ABBREVIATION field (#1), and INACTIVATION DATE field (#5)
    of MEDICATION ROUTES file (#51.2).
    """
    DIERR = None
    ZZERR = None
    PSS51P2 = None
    SCR = {"S": ""}
    PSS = None

    if not LIST:
        return
    del ^TMP($J, LIST)
    if not PSSABBR:
        ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"
        return
    FIND(51.2, "", "@;.01;1", "QP", PSSABBR, "", "C", "", "", "")
    if +^TMP("DILIST", $J, 0) == 0:
        ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"
        return
    ^TMP($J, LIST, 0) = +^TMP("DILIST", $J, 0)
    PSSXX = 0
    while True:
        PSSXX = PSSXX + 1
        if not PSSXX:
            break
        PSSIEN = +^TMP("DILIST", $J, PSSXX, 0)
        del ^TMP("PSS51P2", $J)
        GETS(51.2, +PSSIEN, ".01;1;3;4;5;6;4.1", "IE", "^TMP(""PSS51P2"",$J)")
        PSS = 0
        while True:
            PSS = PSS + 1
            if not PSS:
                break
            SETZRO2()

def SETZRO():
    """
    Set values in ^TMP($J,LIST,+PSS(1), field_number)
    """
    ^TMP($J, LIST, +PSS(1), .01) = ^TMP("PSS51P2", $J, 51.2, PSS(1), .01, "I")
    ^TMP($J, LIST, "B", ^TMP("PSS51P2", $J, 51.2, PSS(1), .01, "I"), +PSS(1)) = ""
    ^TMP($J, LIST, +PSS(1), 4) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 4, "I")
    ^TMP($J, LIST, +PSS(1), 1) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 1, "I")
    ^TMP($J, LIST, +PSS(1), 3) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 3, "I") + "^" + ^TMP("PSS51P2", $J, 51.2, PSS(1), 3, "E")
    ^TMP($J, LIST, +PSS(1), 5) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 5, "I") + "^" + ^TMP("PSS51P2", $J, 51.2, PSS(1), 5, "E")
    ^TMP($J, LIST, +PSS(1), 6) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 6, "I") + "^" + ^TMP("PSS51P2", $J, 51.2, PSS(1), 6, "E")
    ^TMP($J, LIST, +PSS(1), 4.1) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 4.1, "I")

def SETZRO2():
    """
    Set values in ^TMP($J,LIST,+PSS(1), field_number) for SETZRO2 function
    """
    ^TMP($J, LIST, +PSS(1), .01) = ^TMP("PSS51P2", $J, 51.2, PSS(1), .01, "I")
    ^TMP($J, LIST, "B", ^TMP("PSS51P2", $J, 51.2, PSS(1), .01, "I"), +PSS(1)) = ""
    ^TMP($J, LIST, +PSS(1), 1) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 1, "I")
    ^TMP($J, LIST, +PSS(1), 5) = ^TMP("PSS51P2", $J, 51.2, PSS(1), 5, "I") + "^" + ^TMP("PSS51P2", $J, 51.2, PSS(1), 5, "E")

def LOOP(PSS):
    """
    Loop function for PSS = 1 or PSS = 2
    """
    CNT = 0
    PSSIEN = 0
    while True:
        PSSIEN = PSSIEN + 1
        if not PSSIEN:
            break
        exec(f"{PSS}()")
        CNT = CNT + 1
    ^TMP($J, LIST, 0) = CNT if CNT > 0 else "-1^NO DATA FOUND"

def 1():
    """
    Function for PSS = 1 in LOOP function
    """
    if PSSFL and ^PS(51.2, PSSIEN2, 0)[5] and ^PS(51.2, PSSIEN2, 0)[5] <= PSSFL:
        return
    ^TMP("PSS51P2", $J) = ^PS(51.2, PSSIEN2, 0)
    PSS = 0
    while True:
        PSS = PSS + 1
        if not PSS:
            break
        SETZRO()
        CNT = CNT + 1

def 2():
    """
    Function for PSS = 2 in LOOP function
    """
    if PSSPK and ^PS(51.2, PSSIEN2, 0)[4] != PSSPK:
        return
    ^TMP("PSS51P2", $J) = ^PS(51.2, PSSIEN2, 0)
    PSS = 0
    while True:
        PSS = PSS + 1
        if not PSS:
            break
        SETZRO2()
        CNT = CNT + 1