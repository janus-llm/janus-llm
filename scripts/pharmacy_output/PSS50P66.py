def ALL(PSSIEN, PSSFT, PSSFL, LIST):
    """
    PSSIEN - IEN of entry in DOSAGE FORM file (#50.606).
    PSSFT - Free Text name in DOSAGE FORM file (#50.606).
    PSSFL - Inactive flag - "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where
           Field Number is the Field Number of the data piece being returned.
    Returns NAME field (#.01), VERB field (#3), PREPOSITION field (#5), INACTIVE DATE field (#7),
    MED ROUTE FOR DOSAGE FORM multiple (#50.6061), MED ROUTE FOR DOSAGE FORM field (#.01), and NOUN multiple (#50.6066),
    NOUN field (#.01) of DOSAGE FORM file (#50.606).
    """
    import os

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    from django import setup

    setup()

    from myapp.models import MyModel

    def SETSCRN():
        nonlocal SCR
        SCR["S"] = "S ND=$P($G(^PS(50.606,+Y,0)),""^"",2) I ND=""""!(ND>PSSFL)"

    def SETNOUN():
        nonlocal PSS, CNT1, PSSIEN, LIST
        ^TMP[$J, LIST, +PSSIEN, "NOUN", +PSS[3], .01] = "" if ^TMP[$J, "PSS50P66", 50.6066, PSS[3], .01, "I"] == "" else ^TMP[$J, "PSS50P66", 50.6066, PSS[3], .01, "I"]

    def SETMRDF():
        nonlocal PSS, CNT, PSSIEN, LIST
        ^TMP[$J, LIST, +PSSIEN, "MRDSFRM", +PSS[2], .01] = "" if ^TMP[$J, "PSS50P66", 50.6061, PSS[2], .01, "I"] == "" else ^TMP[$J, "PSS50P66", 50.6061, PSS[2], .01, "I"]

    def SETZRO():
        nonlocal PSS, PSSIEN, LIST
        ^TMP[$J, LIST, +PSS[1], .01] = ^TMP[$J, "PSS50P66", 50.606, PSS[1], .01, "I"]
        ^TMP[$J, LIST, "B", ^TMP[$J, "PSS50P66", 50.606, PSS[1], .01, "I"], +PSS[1]] = ""
        ^TMP[$J, LIST, +PSS[1], 3] = ^TMP[$J, "PSS50P66", 50.606, PSS[1], 3, "I"]
        ^TMP[$J, LIST, +PSS[1], 5] = ^TMP[$J, "PSS50P66", 50.606, PSS[1], 5, "I"]
        ^TMP[$J, LIST, +PSS[1], 7] = "" if ^TMP[$J, "PSS50P66", 50.606, PSS[1], 7, "I"] == "" else ^TMP[$J, "PSS50P66", 50.606, PSS[1], 7, "I"] + "^" + ^TMP[$J, "PSS50P66", 50.606, PSS[1], 7, "E"]

    def LOOP():
        nonlocal PSSIEN, CNT2, CNT1, LIST, SCR
        PSSIEN = 0
        while PSSIEN:
            if PSSFL and ^PS[50.606, PSSIEN, 0][2] and ^PS[50.606, PSSIEN, 0][2] <= PSSFL:
                continue
            ^TMP[$J, "PSS50P66"] = GETS^DIQ(50.606, +PSSIEN, ".01;3;5;7;1*;6*", "IE")
            PSS[1] = 0
            while PSS[1]:
                SETZRO()
                CNT2 += 1
            PSS[2] = 0
            while PSS[2]:
                SETMRDF()
                CNT += 1
            PSS[3] = 0
            while PSS[3]:
                SETNOUN()
                CNT1 += 1
            ^TMP[$J, LIST, +PSSIEN, "MRDSFRM", 0] = CNT if CNT else "-1^NO DATA FOUND"
            ^TMP[$J, LIST, 0] = CNT2 if CNT2 else "-1^NO DATA FOUND"
            ^TMP[$J, LIST, +PSSIEN, "NOUN", 0] = CNT1 if CNT1 else "-1^NO DATA FOUND"

    def SETSCRN():
        nonlocal SCR
        SCR["S"] = ""

    def SETNOUN():
        nonlocal PSS, CNT1, PSSIEN, LIST
        ^TMP[$J, LIST, +PSSIEN, "NOUN", +PSS[3], .01] = "" if ^TMP[$J, "PSS50P66", 50.6066, PSS[3], .01, "I"] == "" else ^TMP[$J, "PSS50P66", 50.6066, PSS[3], .01, "I"]

    def SETMRDF():
        nonlocal PSS, CNT, PSSIEN, LIST
        ^TMP[$J, LIST, +PSSIEN, "MRDSFRM", +PSS[2], .01] = "" if ^TMP[$J, "PSS50P66", 50.6061, PSS[2], .01, "I"] == "" else ^TMP[$J, "PSS50P66", 50.6061, PSS[2], .01, "I"]

    def SETZRO():
        nonlocal PSS, PSSIEN, LIST
        ^TMP[$J, LIST, +PSS[1], .01] = ^TMP[$J, "PSS50P66", 50.606, PSS[1], .01, "I"]
        ^TMP[$J, LIST, "B", ^TMP[$J, "PSS50P66", 50.606, PSS[1], .01, "I"], +PSS[1]] = ""
        ^TMP[$J, LIST, +PSS[1], 3] = ^TMP[$J, "PSS50P66", 50.606, PSS[1], 3, "I"]
        ^TMP[$J, LIST, +PSS[1], 5] = ^TMP[$J, "PSS50P66", 50.606, PSS[1], 5, "I"]
        ^TMP[$J, LIST, +PSS[1], 7] = "" if ^TMP[$J, "PSS50P66", 50.606, PSS[1], 7, "I"] == "" else ^TMP[$J, "PSS50P66", 50.606, PSS[1], 7, "I"] + "^" + ^TMP[$J, "PSS50P66", 50.606, PSS[1], 7, "E"]

    def LOOP():
        nonlocal PSSIEN, CNT2, CNT1, LIST, SCR
        PSSIEN = 0
        while PSSIEN:
            if PSSFL and ^PS[50.606, PSSIEN, 0][2] and ^PS[50.606, PSSIEN, 0][2] <= PSSFL:
                continue
            ^TMP[$J, "PSS50P66"] = GETS^DIQ(50.606, +PSSIEN, ".01;3;5;7;1*;6*", "IE")
            PSS[1] = 0
            while PSS[1]:
                SETZRO()
                CNT2 += 1
            PSS[2] = 0
            while PSS[2]:
                SETMRDF()
                CNT += 1
            PSS[3] = 0
            while PSS[3]:
                SETNOUN()
                CNT1 += 1
            ^TMP[$J, LIST, +PSSIEN, "MRDSFRM", 0] = CNT if CNT else "-1^NO DATA FOUND"
            ^TMP[$J, LIST, 0] = CNT2 if CNT2 else "-1^NO DATA FOUND"
            ^TMP[$J, LIST, +PSSIEN, "NOUN", 0] = CNT1 if CNT1 else "-1^NO DATA FOUND"

    from datetime import datetime
    import os

    if not LIST:
        return

    ^TMP[$J, LIST] = {}

    if not PSSIEN and not PSSFT:
        ^TMP[$J, LIST, 0] = "-1^NO DATA FOUND"
        return

    if PSSIEN:
        PSSIEN2 = $$FIND1^DIC(50.606, "", "X", "`" + PSSIEN, , SCR["S"], "")
        if not PSSIEN2:
            ^TMP[$J, LIST, 0] = "-1^NO DATA FOUND"
            return
        ^TMP[$J, LIST, 0] = 1
        ^TMP[$J, "PSS50P66"] = GETS^DIQ(50.606, +PSSIEN2, ".01;3;5;7;1*;6*", "IE")
        PSS[1] = 0
        while PSS[1]:
            SETZRO()
        CNT, PSS[2] = 0, 0
        while PSS[2]:
            SETMRDF()
            CNT += 1
        ^TMP[$J, LIST, +PSSIEN, "MRDSFRM", 0] = CNT if CNT else "-1^NO DATA FOUND"
        CNT1, PSS[3] = 0, 0
        while PSS[3]:
            SETNOUN()
            CNT1 += 1
        ^TMP[$J, LIST, +PSSIEN, "NOUN", 0] = CNT1 if CNT1 else "-1^NO DATA FOUND"

    if not PSSIEN and PSSFT:
        if "??" in PSSFT:
            LOOP()
            return
        FIND^DIC(50.606, , "@;.01", "QP", PSSFT, , "B", SCR["S"], , "")
        if +^TMP["DILIST", $J, 0] == 0:
            ^TMP[$J, LIST, 0] = "-1^NO DATA FOUND"
            return
        if +^TMP["DILIST", $J, 0] > 0:
            ^TMP[$J, LIST, 0] = +^TMP["DILIST", $J, 0]
            PSSXX = 0
            while PSSXX:
                PSSIEN = +^TMP["DILIST", $J, PSSXX, 0)
                ^TMP[$J, "PSS50P66"] = GETS^DIQ(50.606, +PSSIEN, ".01;3;5;7;1*;6*", "IE")
                PSS[1] = 0
                while PSS[1]:
                    SETZRO()
                CNT, PSS[2] = 0, 0
                while PSS[2]:
                    SETMRDF()
                    CNT += 1
                ^TMP[$J, LIST, +PSSIEN, "MRDSFRM", 0] = CNT if CNT else "-1^NO DATA FOUND"
                CNT1, PSS[3] = 0, 0
                while PSS[3]:
                    SETNOUN()
                    CNT1 += 1
                ^TMP[$J, LIST, +PSSIEN, "NOUN", 0] = CNT1 if CNT1 else "-1^NO DATA FOUND"
                PSSXX += 1
    ^TMP[$J, "DILIST"], ^TMP[$J, "PSS50P66"] = {}, {}

def ADD(PSSIEN, PSSMR):
    """
    PSSIEN - IEN of entry in DOSAGE FORM file (#50.606).
    PSSMR - IEN of entry in MEDICATION ROUTES file (#51.2).
    0 (zero)is returned if ADD was unsuccessful.  1 (one) will indicate successful ADD.
    Adding new entry to MED ROUTE FOR DOSAGE FORM multiple (#50.6061) of the DOSAGE FORM file (#50.606).
    """
    if not (PSSIEN and PSSMR):
        return 0
    PSSIEN2 = $$FIND1^DIC(51.2, "", "A", "`" + PSSMR, , , "")
    if not PSSIEN2:
        return 0
    PSSIEN3 = $$FIND1^DIC(50.606, "", "A", "`" + PSSIEN, , , "")
    if not PSSIEN3:
        return 0
    ^TMP["DILIST", $J] = LIST^DIC(50.6061, ","_PSSIEN_",", "@;.01IE", "P", , , , , , , "")
    if +^TMP["DILIST", $J, 0] <= 0:
        PSS[1, 50.6061, "+2,"_PSSIEN_",", .01] = PSSMR
    else:
        QFLG, PSS = 0, 0
        while PSS:
            if ^TMP["DILIST", $J, PSS, 0][2] == PSSMR:
                QFLG = 1
                break
            PSS[1, 50.6061, "+2,"_PSSIEN_",", .01] = PSSMR
    UPDATE^DIE("", PSS[1])
    return 1