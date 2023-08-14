def PSSPOIC():
    # BIR/RTR-Orderable items by VA Name after Primary ; 09/01/98 7:10
    # 1.0;PHARMACY DATA MANAGEMENT;**15**;9/30/97

    if not PSMATCH:
        G CANT

    # VA Generic Name after Primary checks that can auto-match
    for PPP in range(0, len(PSDRUG)):
        NDNOD = PSDRUG[PPP]["ND"]
        PSODNAME = PSDRUG[PPP][0]
        PRIPTR = PSDRUG[PPP][2][6]
        PSOIPTR = PSDRUG[PPP][2][0]
        DA = PSNDO[0]
        K = PSNDO[2]
        X = PSJDF(PSNDO[0], PSNDO[2])
        DOFO = X

        if PSODNAME == "":
            continue

        if PSODNAME in TMP["PSS"]:
            continue

        if PSOIPTR:
            continue

        TMP["PSSPP"] = {}
        if NDNOD[0] and NDNOD[2]:
            for AA in range(0, len(PSDRUG)):
                if NDNOD[0] == PSDRUG[AA]["ND"][0]:
                    OTHNAME = PSDRUG[AA][0]
                    if OTHNAME in TMP["PSS"]:
                        ONOD = PSDRUG[AA]["ND"]
                        if ONOD[0] and ONOD[2] and DOFO != 0:
                            DA = ONOD[0]
                            K = ONOD[2]
                            X = PSJDF(DA, K)
                            DOFO1 = X
                            if DOFO1 != 0:
                                if DOFO == DOFO1:
                                    TMP["PSSPP"][AA] = TMP["PSS"][OTHNAME]

        COMM = 0
        COMMSUP = 0
        if TMP["PSSPP"]:
            COMM = 1
            WW = next(iter(TMP["PSSPP"]))
            POII = TMP["PSSPP"][WW]
            for WW in range(len(TMP["PSSPP"])):
                if POII != TMP["PSSPP"][WW]:
                    COMMSUP = 1

        if COMM and COMMSUP:
            continue

        if COMM and not COMMSUP:
            ZZZ = next(iter(TMP["PSSPP"]))
            ZZZ = TMP["PSSPP"][ZZZ]
            TMP["PSSD"][ZZZ][PSODNAME] = ""
            continue

        if NDNOD[0] and NDNOD[2]:
            DA = NDNOD[0]
            K = NDNOD[2]
            X = PSJDF(DA, K)
            D1F1 = X
            if D1F1 != 0:
                DA = NDNOD[0]
                X = VAGN(DA)
                VAGN = X
                if len(VAGN) < 41:
                    TMP["PSSD"][VAGN + " " + D1F1[1]][PSODNAME] = ""

    END()
    return

def CANT():
    # Generic Name after Primary, can't match
    for LLL in range(0, len(PSDRUG)):
        RSN = {}
        DOSFO = {}
        POTDOS = {}

        PSNDO = PSDRUG[LLL]["ND"]
        PSNAME = PSDRUG[LLL][0]
        PSPTR = PSDRUG[LLL][2][0]
        PSPRIM = PSDRUG[LLL][2][6]
        DA = PSNDO[0]
        K = PSNDO[2]
        X = PSJDF(DA, K)
        FRM1 = X
        TMPFLG = 0

        if PSPTR:
            continue

        if PSNAME in TMP["PSS"]:
            continue

        TMP["PSSO"] = {}
        if PSNDO[0] and PSNDO[2]:
            for BB in range(0, len(PSDRUG)):
                if PSNDO[0] == PSDRUG[BB]["ND"][0]:
                    OTHER = PSDRUG[BB][0]
                    if OTHER in TMP["PSS"]:
                        OTNO = PSDRUG[BB]["ND"]
                        if OTNO[0] and OTNO[2] and FRM1 != 0:
                            DA = OTNO[0]
                            K = OTNO[2]
                            X = PSJDF(DA, K)
                            FRM2 = X
                            if FRM2 != 0:
                                if FRM1 == FRM2:
                                    SAME = 0
                                    POINAME = TMP["PSS"][OTHER]
                                    for III in range(len(TMP["PSSO"])):
                                        if POINAME == TMP["PSSO"][III]:
                                            SAME = 1
                                    if not SAME:
                                        TMP["PSSO"][BB] = TMP["PSS"][OTHER]

        PSCOMMD = 0
        if TMP["PSSO"]:
            TTT = next(iter(TMP["PSSO"]))
            ORDNAM = TMP["PSSO"][TTT]
            for TTT in range(len(TMP["PSSO"])):
                if ORDNAM != TMP["PSSO"][TTT]:
                    PSCOMMD = 1

        if TMP["PSSO"] and not PSCOMMD:
            continue

        CNT = 0
        if TMP["PSSO"] and not TMP["PSSD"]["ZZZZ"][PSNAME]:
            CNT = 1
            TMPFLG = 1
            for NN in range(len(TMP["PSSO"])):
                TMP["PSSD"]["ZZZZ"][PSNAME][CNT] = TMP["PSSO"][NN]
                CNT = CNT + 1

        if CNT:
            RSN = "Multiple Orderable Items"
            continue

        QFLAG = 0
        if PSNDO[0] and PSNDO[2]:
            DA = PSNDO[0]
            X = VAGN(DA)
            VAGN1 = X
            if VAGN1 != 0:
                DOSFO = FRM1[0]
                if DOSFO and DOSFO in DOSAGE:
                    if len(VAGN1) < 41:
                        QFLAG = 1

        if QFLAG:
            continue

        if TMP["PSSD"]["ZZZZ"][PSNAME]:
            continue

        TMPFLG = 1
        if PSNDO[0] == "":
            RSN = "NDF link missing or incomplete"
            continue

        if PSNDO[2] == "":
            RSN = "No PSNDF VA Product Name Entry"
            continue

        if VAGN1 == 0:
            RSN = "Invalid National Drug File Entry"
            continue

        PVA = PSNDO[2]
        DA = PSNDO[0]
        K = PVA
        X = PROD0(DA, K)
        if X == "":
            RSN = "Invalid PSNDF VA Product Name Entry"
            continue

        DA = PSNDO[0]
        K = PVA
        X = PSJDF(DA, K)
        FRM0 = X
        if FRM0 == 0:
            RSN = "No Dosage Form entry in NDF"
            continue

        if FRM0 == 0:
            RSN = "Missing Dosage Form in NDF"
            continue

        if FRM0 == 0:
            RSN = "Invalid Entry in Dosage Form File"
            continue

        if len(VAGN1) > 40:
            RSN = "Generic name exceeds 40 characters"
            continue

        RSN = "Undetermined problem"
        continue

    DONE()
    return

def END():
    TMP["PSSO"] = {}
    AA = {}
    APPU = {}
    COMM = {}
    COMMSUP = {}
    NDNOD = {}
    ONOD = {}
    OTHNAME = {}
    POII = {}
    PPP = {}
    PSOIPTR = {}
    PRIPTR = {}
    PSODF = {}
    PSODNAME = {}
    WW = {}
    ZZZ = {}
    return

def DONE():
    TMP["PSSO"] = {}
    TMP["PSS"] = {}
    APL = {}
    BB = {}
    CNT = {}
    DOSFRM = {}
    DOSPNT = {}
    SAME = {}
    LLL = {}
    III = {}
    NN = {}
    ORDNAM = {}
    OTHER = {}
    OTNO = {}
    POINAME = {}
    PSCOMMD = {}
    PSNAME = {}
    PSPTR = {}
    PSPRIM = {}
    POTDOS = {}
    PSNDO = {}
    DOSFO = {}
    PVA = {}
    QFLAG = {}
    RSN = {}
    TTT = {}
    TMPFLG = {}
    return

PSSPOIC()