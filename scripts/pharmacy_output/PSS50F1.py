def PSS50F1():
    """
    BIR/RTR - API FOR INFORMATION FROM FILE 50
    1.0;PHARMACY DATA MANAGEMENT;**85**;9/30/97
    """
    # Reference to ^PS(50.605 is supported by DBIA #2138

    def LIST():
        """
        PSSFT - Free Text name in 50
        PSSFL - Inactive flag - "" - All entries
                                FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
        PSSD - Index used in the lookup in the format B^C
        PSSPK - Application Package's Use - "" - All entries
                                             Alphabetic codes that represent the DHCP packages that consider this drug to be
                                             part of their formulary.
        LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
               piece being returned.
        """
        nonlocal PSSENCT, PSSXSUB, SCR, PSS, CNT, PSSLUPAR, PSSLUPP, PSSSCRN
        if not LIST:
            return
        ^TMP($J, LIST) = {}
        if not PSSFT:
            ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"
            return
        SCR["S"] = ""
        PSSXSUB = ""
        SETXSUB()
        PSSENCT = 0
        if PSSFL > 0 or PSSPK:
            SETSCRN()
        if PSSFT:
            if PSSFT == "??":
                LOOP()
            else:
                ^TMP("DILIST", $J) = {}
                ^TMP($J, "PSSLDONE") = {}
                PSSSCRN = SCR["S"]
                if not PSSD:
                    PSSD = "B"
                PARSE^PSS50F(PSSD)
                if not PSSLUPAR:
                    return
                for PSSLUPP in PSSLUPAR:
                    SCR["S"] = PSSSCRN
                    FIND^DIC(50, , "@;.01", "QPB" + (PSSLUPAR[PSSLUPP][1] and "X" or ""), PSSFT, , PSSLUPAR[PSSLUPP], SCR["S"], , )
                    if ^TMP("DILIST", $J, 0) == 0:
                        continue
                    for PSSXX in ^TMP("DILIST", $J):
                        PSSIEN = +^TMP("DILIST", $J, PSSXX, 0)
                        if PSSIEN not in ^TMP($J, "PSSLDONE"):
                            ^TMP($J, "PSSLDONE", PSSIEN) = ""
                            ^TMP("PSSP50", $J) = {}
                            GETS^DIQ(50, +PSSIEN, ".01;100;2.1", "IE", "^TMP(""PSSP50"",$J)")
                            PSS(1) = 0
                            for PSS(1) in ^TMP("PSSP50", $J, 50):
                                SETLIST()
        ^TMP($J, LIST, 0) = PSSENCT or "-1^NO DATA FOUND"
        K ^TMP("DILIST", $J), ^TMP("PSSP50", $J), ^TMP($J, "PSSLDONE")

    def SETLIST():
        """
        Set the data in the ^TMP array.
        """
        nonlocal PSSENCT, PSS
        PSSENCT += 1
        ^TMP($J, LIST, +PSS(1), .01) = ^TMP("PSSP50", $J, 50, PSS(1), .01, "I")
        ^TMP($J, LIST, (PSSXSUB or "B"), ^TMP("PSSP50", $J, 50, PSS(1), .01, "I"), +PSS(1)) = ""
        ^TMP($J, LIST, +PSS(1), 2.1) = ^TMP("PSSP50", $J, 50, PSS(1), 2.1, "I") or "" + "^" + ^TMP("PSSP50", $J, 50, PSS(1), 2.1, "E")
        if ^TMP($J, LIST, +PSS(1), 2.1):
            PSSADDF = SETDF^PSS50AQM(^TMP($J, LIST, +PSS(1), 2.1))
            ^TMP($J, LIST, +PSS(1), 2.1) += (PSSADDF > 0 and "^" + PSSADDF[3] + "^" + PSSADDF[4] or "")
        ^TMP($J, LIST, +PSS(1), 100) = ^TMP("PSSP50", $J, 50, PSS(1), 100, "I") or ""

    def LOOP():
        """
        Loop through all drugs in the DRUG file (#50) and set the data in the ^TMP array.
        """
        nonlocal PSS
        PSS(1) = 0
        while PSS(1) < MAX_DRUG:
            if not ^PSDRUG(PSS(1)):
                continue
            if PSSFL and ^PSDRUG(PSS(1), "I") and ^("I") <= PSSFL:
                continue
            if PSSPK:
                PSSZ5 = 0
                for PSSZ6 in range(1, len(PSSPK)):
                    if PSSPK[PSSZ6] in ^PSDRUG(PSS(1), 2)[3]:
                        PSSZ5 = 1
                        break
                if not PSSZ5:
                    continue
            SETLIST()
            PSSENCT += 1
            PSS(1) += 1

    def SETXSUB():
        """
        Set the PSSXSUB variable based on PSSD.
        """
        nonlocal PSSXSUB
        if not PSSD:
            return
        PSSLSXCT = PSSD.count("^") + 1
        PSSLCNT = 0
        for PSSLSX in range(1, PSSLSXCT):
            PSSDSUB = PSSD.split("^")[PSSLSX]
            if PSSLCNT > 1:
                break
            PSSXSUB = PSSDSUB or PSSXSUB
            if PSSDSUB:
                PSSLCNT += 1
        if PSSLCNT > 1:
            PSSXSUB = ""

    def LOOKUP():
        """
        PSSFT - Free Text value that could be the NAME field (#.01), IEN, VA PRODUCT NAME field (#21), NATIONAL DRUG CLASS field (#25),
                or SYNONYM (#.01) mutiple of the DRUG file (#50).
        PSSFL - Inactive flag - "" - All entries
                                FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
        PSSPK - Application Package's Use - "" - All entries
                                             Alphabetic codes that represent the DHCP packages that consider this drug to be
                                             part of their formulary.
        PSSRTOI - 1 - only drugs with data in the PHARMACY ORDERABLE ITEM field (#2.1) will be returned.
        PSSIFCAP - 1 - only drugs with no data in the IFCAP ITEM NUMBER multiple (#441) will be returned.
        PSSCMOP         - 1 - only drugs with no data in the CMOP ID field (#27) will be returned.
        PSSD - Index used in the lookup in the format B^C.
        LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
               piece being returned.
        """
        nonlocal PSSLKIEN, PSSLKSUB, PSSENCT, SCR, PSSXSUB, CNT, PSS, DIERR
        if not LIST:
            return
        ^TMP($J, LIST) = {}
        if not PSSFT:
            ^TMP($J, LIST, 0) = -1 + "^" + "NO DATA FOUND"
            return
        PSSENCT = 0
        if PSSFT == "??":
            LOOPLK()
        else:
            PSSLKSUB = "B"
            PSSLKIEN = 0
            while PSSLKIEN < MAX_DRUG:
                if not ^PSDRUG(PSSLKIEN):
                    continue
                if PSSCMOP and ^PSDRUG(PSSLKIEN, "ND", 10):
                    continue
                if PSSIFCAP and ^PSDRUG(PSSLKIEN, 441):
                    continue
                if PSSFL and ^PSDRUG(PSSLKIEN, "I") and ^("I") <= PSSFL:
                    continue
                if PSSRTOI and not ^PSDRUG(PSSLKIEN, 2):
                    continue
                if PSSPK:
                    PSSZ5 = 0
                    for PSSZ6 in range(1, len(PSSPK)):
                        if PSSPK[PSSZ6] in ^PSDRUG(PSSLKIEN, 2)[3]:
                            PSSZ5 = 1
                            break
                    if not PSSZ5:
                        continue
                LOOKSET()
                PSSLKIEN += 1
            ^TMP($J, LIST, 0) = PSSENCT or "-1^NO DATA FOUND"

    def LOOKSET():
        """
        Set the data in the ^TMP array.
        """
        nonlocal PSSLKIEN
        PSSLKNAM = ^PSDRUG(PSSLKIEN, 0)
        PSSLKND = ^("ND")
        PSSLKZER = ^("ND")
        if not PSSLKNAM:
            return
        ^TMP($J, LIST, PSSLKIEN, .01) = PSSLKNAM
        ^TMP($J, LIST, PSSLKSUB, PSSLKNAM, PSSLKIEN) = ""
        PSSENCT += 1
        ^TMP($J, LIST, PSSLKIEN, 25) = PSSLKND[6] and PSSLKND[6] + "^" + ^PS(50.605, +PSSLKND[6], 0) + "^" + $P(^PS(50.605, +PSSLKND[6], 0), "^", 2) or ""
        ^TMP($J, LIST, PSSLKIEN, 100) = ^PSDRUG(PSSLKIEN, "I") or ""

    def LOOPLK():
        """
        Loop through all drugs in the DRUG file (#50) and set the data in the ^TMP array.
        """
        nonlocal PSSLKIEN
        PSSLKSUB = "B"
        PSSLKIEN = 0
        while PSSLKIEN < MAX_DRUG:
            if not ^PSDRUG(PSSLKIEN):
                continue
            if PSSCMOP and ^PSDRUG(PSSLKIEN, "ND", 10):
                continue
            if PSSIFCAP and ^PSDRUG(PSSLKIEN, 441):
                continue
            if PSSFL and ^PSDRUG(PSSLKIEN, "I") and ^("I") <= PSSFL:
                continue
            if PSSRTOI and not ^PSDRUG(PSSLKIEN, 2):
                continue
            if PSSPK:
                PSSZ5 = 0
                for PSSZ6 in range(1, len(PSSPK)):
                    if PSSPK[PSSZ6] in ^PSDRUG(PSSLKIEN, 2)[3]:
                        PSSZ5 = 1
                        break
                if not PSSZ5:
                    continue
            LOOKSET()
            PSSLKIEN += 1
        ^TMP($J, LIST, 0) = PSSENCT or "-1^NO DATA FOUND"

    LIST()
    LOOKUP()

PSS50F1()