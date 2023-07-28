def PSS50ATC(PSSIEN, PSSFT, PSSFL, PSSPK, LIST):
    """
    BIR/LDT - API INFORMATION FROM FILE 50
    """
    # External reference to PS(57.5 supported by DBIA 2112
    def SETSCRN():
        """
        Set SCR("S") variable
        """
        if PSSFL > 0 or PSSPK:
            global SCR
            SCR["S"] = ""

    def SETSCN():
        """
        Set SCR("S") variable
        """
        if PSSFL > 0 or PSSPK:
            global SCR
            SCR["S"] = ""

    def SETATC():
        """
        Set ATC data
        """
        global PSS
        global LIST
        global PSSMLCT
        
        LIST[PSS[1]]["ATC"] = {}
        LIST[PSS[1]]["ATC"][0] = PSSMLCT if PSSMLCT else "-1^NO DATA FOUND"
        LIST[PSS[1]]["ATC"][+PSS[2]] = {}
        LIST[PSS[1]]["ATC"][+PSS[2]][".01"] = (
            f"{TMP_PSSP50[50.0212][PSS[2]][.01]['I']}^"
            f"{TMP_PSSP50[50.0212][PSS[2]][.01]['E']}"
        )
        LIST[PSS[1]]["ATC"][+PSS[2]][1] = TMP_PSSP50[50.0212][PSS[2]][1]["I"]

    def SETATC2():
        """
        Set ATC data
        """
        global PSS
        global LIST
        global PSSMLCT

        LIST[PSS[1]]["ATC"] = {}
        LIST[PSS[1]]["ATC"][0] = PSSMLCT if PSSMLCT else "-1^NO DATA FOUND"
        LIST[PSS[1]]["ATC"][+PSS[2]] = {}
        LIST[PSS[1]]["ATC"][+PSS[2]][".01"] = (
            f"{TMP_PSSP50[50.0212][PSS[2]][.01]['I']}^"
            f"{TMP_PSSP50[50.0212][PSS[2]][.01]['E']}"
        )
        LIST[PSS[1]]["ATC"][+PSS[2]][1] = TMP_PSSP50[50.0212][PSS[2]][1]["I"]

    def SETATCL():
        """
        Set ATC data
        """
        global PSS
        global LIST

        LIST[PSS[1]][".01"] = TMP_PSSP50[50][PSS[1]][.01]["I"]
        LIST["AC"][TMP_PSSP50[50][PSS[1]][.01]["I"]] = PSS[1]
        LIST[PSS[1]]["212.2"] = TMP_PSSP50[50][PSS[1]][212.2]["I"]

    def SETATCLM():
        """
        Set ATC data
        """
        global PSS
        global LIST

        PSS50212 = 0
        if TMP_PSSP50[50][PSS[1]].get(212):
            for PSSAT212 in TMP_PSSP50[50][PSS[1]][212]:
                PSSATCND = TMP_PSSP50[50][PSS[1]][212][PSSAT212]
                if PSSATCND[".01"]:
                    PSS50212 += 1
                    LIST[PSS[1]]["ATC"][PSSAT212][.01] = (
                        f"{PSSATCND['.01']['I']}^"
                        f"{PSSATCND['.01']['E']}"
                    )
                    LIST[PSS[1]]["ATC"][PSSAT212][1] = PSSATCND[1]["I"]
        LIST[PSS[1]]["ATC"][0] = PSS50212 if PSS50212 else "-1^NO DATA FOUND"

    def LOOP():
        """
        Loop through the data
        """
        global PSS
        global LIST

        PSSENCT = 0
        PSS[1] = 0
        while PSS[1] in TMP_PSSP50[50]:
            if not TMP_PSSP50[50][PSS[1]][.01]["I"]:
                continue
            if PSSFL and TMP_PSSP50[50][PSS[1]]["I"] and TMP_PSSP50[50][PSS[1]]["I"] <= PSSFL:
                continue
            PSSZ5 = 0
            for PSSZ6 in range(1, len(PSSPK)+1):
                if PSSPK[PSSZ6-1] in TMP_PSSP50[50][PSS[1]][2][3]:
                    PSSZ5 = 1
                    break
            if PSSPK and not PSSZ5:
                continue
            PSSAXXOK = 0
            for PSSAXX in TMP_PSSP50[50][PSS[1]][212]["AC"]:
                PSSAXX1 = ""
                while PSSAXX1 in TMP_PSSP50[50][PSS[1]][212]["AC"][PSSAXX]:
                    PSSAXX2 = 0
                    while PSSAXX2 in TMP_PSSP50[50][PSS[1]][212]["AC"][PSSAXX][PSSAXX1]:
                        if (
                            PSSAXX2 in TMP_PSSP50[50][PSS[1]][212]
                            and TMP_PSSP50[50][PSS[1]][212][PSSAXX2]
                        ):
                            PSSAXXOK = 1
                        PSSAXX2 += 1
                    if PSSAXXOK:
                        break
                    PSSAXX1 = next(iter(TMP_PSSP50[50][PSS[1]][212]["AC"][PSSAXX]))
                if PSSAXXOK:
                    break
            if not PSSAXXOK:
                continue
            SETSUB9(PSS[1])
            SETATCL()
            SETATCLM()
            PSSENCT += 1
            PSS[1] += 1
        LIST[0] = PSSENCT if PSSENCT else "-1^NO DATA FOUND"

    def SETSYN2():
        """
        Set SYN data
        """
        global PSS
        global LIST

        LIST[PSS[1]]["SYN"] = {}
        LIST[PSS[1]]["SYN"][+PSS[2]] = {}
        LIST[PSS[1]]["SYN"][+PSS[2]][".01"] = (
            f"{TMP_PSSP50[50.1][PSS[2]][.01]['I']}"
        )
        LIST[PSS[1]]["SYN"][+PSS[2]][1] = (
            f"{TMP_PSSP50[50.1][PSS[2]][1]['I']}^"
            f"{TMP_PSSP50[50.1][PSS[2]][1]['E']}"
        )
        LIST[PSS[1]]["SYN"][+PSS[2]][2] = TMP_PSSP50[50.1][PSS[2]][2]["I"]
        LIST[PSS[1]]["SYN"][+PSS[2]][400] = TMP_PSSP50[50.1][PSS[2]][400]["I"]
        PSSUTNX = TMP_PSSP50[50.1][PSS[2]][401]["I"]
        if PSSUTNX:
            LIST[PSS[1]]["SYN"][+PSS[2]][401] = (
                f"{TMP_PSSP50[50.1][PSS[2]][401]['I']}^"
                f"{TMP_PSSP50[50.1][PSS[2]][401]['E']}"
            )
            LIST[PSS[1]]["SYN"][+PSS[2]][401] += f"^{TMP_DIC[51.5][PSSUTNX][0][2]}"
        LIST[PSS[1]]["SYN"][+PSS[2]][402] = TMP_PSSP50[50.1][PSS[2]][402]["I"]
        LIST[PSS[1]]["SYN"][+PSS[2]][403] = TMP_PSSP50[50.1][PSS[2]][403]["I"]
        LIST[PSS[1]]["SYN"][+PSS[2]][404] = TMP_PSSP50[50.1][PSS[2]][404]["I"]
        LIST[PSS[1]]["SYN"][+PSS[2]][405] = TMP_PSSP50[50.1][PSS[2]][405]["I"]

    def SETINV():
        """
        Set INV data
        """
        global PSS
        global LIST

        LIST[PSS[1]][".01"] = TMP_PSSP50[50][PSS[1]][.01]["I"]
        LIST["B"][TMP_PSSP50[50][PSS[1]][.01]["I"]] = PSS[1]
        LIST[PSS[1]]["11"] = TMP_PSSP50[50][PSS[1]][11]["I"]
        PSSUTN = TMP_PSSP50[50][PSS[1]][12]["I"]
        if PSSUTN:
            LIST[PSS[1]]["12"] = (
                f"{TMP_PSSP50[50][PSS[1]][12]['I']}^"
                f"{TMP_PSSP50[50][PSS[1]][12]['E']}"
            )
            LIST[PSS[1]]["12"] += f"^{TMP_DIC[51.5][PSSUTN][0][2]}"
        LIST[PSS[1]]["13"] = TMP_PSSP50[50][PSS[1]][13]["I"]
        LIST[PSS[1]]["14"] = TMP_PSSP50[50][PSS[1]][14]["I"]
        LIST[PSS[1]]["15"] = TMP_PSSP50[50][PSS[1]][15]["I"]
        LIST[PSS[1]]["16"] = TMP_PSSP50[50][PSS[1]][16]["I"]
        LIST[PSS[1]]["17"] = TMP_PSSP50[50][PSS[1]][17]["I"]
        LIST[PSS[1]]["14.5"] = TMP_PSSP50[50][PSS[1]][14.5]["I"]
        LIST[PSS[1]]["17.1"] = (
            f"{TMP_PSSP50[50][PSS[1]][17.1]['I']}^"
            f"{TMP_PSSP50[50][PSS[1]][17.1]['E']}"
        )
        LIST[PSS[1]]["50"] = TMP_PSSP50[50][PSS[1]][50]["I"]

    def SETIFC():
        """
        Set IFC data
        """
        global PSS
        global LIST

        LIST[PSS[1]]["IFC"][+PSS[2]] = (
            f"{TMP_PSSP50[50.0441][PSS[2]][.01]['I']}"
        )

    # Main function
    import copy

    # Initialize variables
    DIERR = None
    ZZERR = None
    PSSP50 = None
    SCR = {"S": ""}
    PSS = [None] * 6
    PSSMLCT = None
    PSSAXX = None
    PSSAXX1 = None
    PSSAXX2 = None
    PSSAXXOK = None

    # Check if LIST is empty
    if not LIST:
        return

    # Clear previous data in LIST
    LIST.clear()

    # Check if PSSIEN and PSSFT are not provided
    if (not PSSIEN or PSSIEN <= 0) and not PSSFT:
        LIST[0] = "-1^NO DATA FOUND"
        return

    # Set screen variable
    SETSCRN()

    # Check if PSSIEN is provided
    if PSSIEN and PSSIEN > 0:
        PSSIEN2 = PSSIEN
        if "TMP_PSSP50" not in globals():
            TMP_PSSP50 = {}
        if "TMP_DIERR" not in globals():
            TMP_DIERR = {}
        PSSIEN2 = TMP_DIERR["PSS"]["PSS"]["210"]
        if PSSIEN2 <= 0:
            LIST[0] = "-1^NO DATA FOUND"
            return
        PSSAXXOK = 0
        PSSAXX = None
        while True:
            PSSAXX = next(iter(TMP_PSSP50[50][PSSIEN2][212]["AC"]))
            if not PSSAXX:
                break
            PSSAXX1 = None
            while True:
                PSSAXX1 = next(iter(TMP_PSSP50[50][PSSIEN2][212]["AC"][PSSAXX]))
                if not PSSAXX1:
                    break
                PSSAXX2 = None
                while True:
                    PSSAXX2 = next(iter(TMP_PSSP50[50][PSSIEN2][212]["AC"][PSSAXX][PSSAXX1]))
                    if not PSSAXX2:
                        break
                    if PSSAXX2 in TMP_PSSP50[50][PSSIEN2][212]:
                        PSSAXXOK = 1
                        break
                if PSSAXXOK:
                    break
            if PSSAXXOK:
                break
        if not PSSAXXOK:
            LIST[0] = "-1^NO DATA FOUND"
            return
        LIST[0] = 1
        LIST[PSSIEN2] = {}
        SETSUB9(PSSIEN2)
        TMP_PSSP50 = None
        PSS[1] = 0
        while True:
            PSS[1] += 1
            if PSS[1] not in TMP_PSSP50[50]:
                break
            SETATCL()
            PSS[2] = 0
            PSSMLCT = 0
            while True:
                PSS[2] += 1
                if PSS[2] not in TMP_PSSP50[50.0212]:
                    break
                PSSMLCT += 1
                SETATC2()
            LIST[PSS[1]]["ATC"][0] = PSSMLCT if PSSMLCT else "-1^NO DATA FOUND"
        return

    # Check if PSSFT is provided
    if PSSFT:
        if PSSFT.endswith("??"):
            LOOP()
        else:
            if "TMP_DILIST" not in globals():
                TMP_DILIST = {}
            PSSXX = 0
            while True:
                PSSXX += 1
                if PSSXX not in TMP_DILIST:
                    break
                PSSIEN = TMP_DILIST[PSSXX][0]
                PSSAXXOK = 0
                PSSAXX = None
                while True:
                    PSSAXX = next(iter(TMP_PSSP50[50][PSSIEN][212]["AC"]))
                    if not PSSAXX:
                        break
                    PSSAXX1 = None
                    while True:
                        PSSAXX1 = next(iter(TMP_PSSP50[50][PSSIEN][212]["AC"][PSSAXX]))
                        if not PSSAXX1:
                            break
                        PSSAXX2 = None
                        while True:
                            PSSAXX2 = next(iter(TMP_PSSP50[50][PSSIEN][212]["AC"][PSSAXX][PSSAXX1]))
                            if not PSSAXX2:
                                break
                            if PSSAXX2 in TMP_PSSP50[50][PSSIEN][212]:
                                PSSAXXOK = 1
                                break
                        if PSSAXXOK:
                            break
                    if PSSAXXOK:
                        break
                if not PSSAXXOK:
                    continue
                if PSS[1] not in LIST:
                    LIST[PSS[1]] = {}
                LIST[0] = LIST[0] + 1 if LIST[0] else 1
                SETSUB9(PSSIEN)
                TMP_PSSP50 = None
                PSS[1] = 0
                while True:
                    PSS[1] += 1
                    if PSS[1] not in TMP_PSSP50[50]:
                        break
                    SETATCL()
                    PSS[2] = 0
                    PSSMLCT = 0
                    while True:
                        PSS[2] += 1
                        if PSS[2] not in TMP_PSSP50[50.0212]:
                            break
                        PSSMLCT += 1
                        SETATC2()
                    LIST[PSS[1]]["ATC"][0] = PSSMLCT if PSSMLCT else "-1^NO DATA FOUND"
        if not LIST[0]:
            LIST[0] = "-1^NO DATA FOUND"
        return

    LIST[0] = "-1^NO DATA FOUND"