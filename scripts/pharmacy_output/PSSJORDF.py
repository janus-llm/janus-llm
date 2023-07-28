def START(PSJORD, PSJOPAC):
    MR, MRNODE, PSJDFNO, X, MCT, Z, PSJOISC = None, None, None, None, None, None, None

    if not PSJORD:
        MEDROUTE()
        return

    PSJDFNO = int(PSJORD[0].split('^')[1])
    PSJOISC = PSJORD[0].split('^')[7]

    if PSJOPAC == "O" or PSJOPAC == "X":
        if PSJOISC:
            EN_PSSOUTSC(PSJOISC)
            if PSJOISC:
                TMP["PSJSCH", $J] = PSJOISC
        return

    if PSJOISC:
        EN_PSSGSGUI(PSJOISC, "I")
        if PSJOISC:
            TMP["PSJSCH", $J] = PSJOISC

    SCPASS()
    if not PSJORD[0]:
        NOD()
        if TMP["PSJMR", $J, 1]:
            MEDROUTE()
        return

    TMP["PSJMR", $J] = {}
    TMP["PSJNOUN", $J] = {}
    DF()
    IND()


def DF():
    VERB, MR, X, PM, II = None, None, None, None, None

    MR, X, MCT = 0, 0, 1
    VERB = TMP["PS50.606", PSJDFNO, "MISC"].split('^')[1]
    MR = int(PSJORD[0].split('^')[6])

    if MR and TMP["PS51.2", MR, 0].split('^')[4] == 1:
        TMP["PSJMR", $J, 1] = TMP["PS51.2", MR, 0].split('^')[1] + '^' + TMP["PS51.2", MR, 0].split('^')[3] + '^' + MR + '^' + (
            1 if TMP["PS51.2", MR, 0].split('^')[6] else 0) + '^D'
        MCT += 1

    if PSJORD[0].split('^')[13] != "Y":
        II = 0
        while II:
            PM = int(TMP["PS50.7", PSJORD[0], 3, II, 0])
            if PM and TMP["PS51.2", PM, 0].split('^')[4] == 1:
                TMP["PSJMR", $J, MCT] = TMP["PS51.2", PM, 0].split('^')[1] + '^' + TMP["PS51.2", PM, 0].split('^')[3] + '^' + PM + '^' + (
                    1 if TMP["PS51.2", PM, 0].split('^')[6] else 0)
                MCT += 1
            II += 1

    MR = 0
    while MR:
        X = int(TMP["PS50.606", PSJDFNO, "MR", MR, 0])
        if X and X != int(PSJORD[0].split('^')[6]):
            MRNODE = TMP["PS51.2", X, 0]
            if MRNODE.split('^')[4] == 1:
                TMP["PSJMR", $J, MCT] = MRNODE.split('^')[0] + '^' + MRNODE.split('^')[2] + '^' + X + '^' + MRNODE.split('^')[1] + '^' + (
                    1 if MRNODE.split('^')[6] else 0)
                MCT += 1
        MR += 1

    X = 0
    if TMP["PS50.606", PSJDFNO, "NOUN"]:
        Z = 0
        while Z:
            X += 1
            TMP["PSJNOUN", $J, X] = TMP["PS50.606", PSJDFNO, "NOUN", Z, 0].split('^')[0] + '^' + TMP["PS50.606", PSJDFNO, "MISC"].split('^')[0] + '^' + TMP["PS50.606", PSJDFNO, "MISC"].split('^')[2]
            Z += 1


def MEDROUTE():
    MR, MRNODE, MCT = None, None, None

    MR, MCT = 0, 0
    TMP["PSJMR", $J] = {}
    MR = 0
    while MR:
        MRNODE = TMP["PS51.2", MR, 0]
        if MRNODE.split('^')[4] == 1:
            MCT += 1
            TMP["PSJMR", $J, MCT] = MRNODE.split('^')[0] + '^' + MRNODE.split('^')[2] + '^' + MR + '^' + MRNODE.split('^')[1] + '^' + (
                1 if MRNODE.split('^')[6] else 0)


def NOD():
    MR = int(PSJORD[0].split('^')[6])

    if MR and TMP["PS51.2", MR, 0].split('^')[4] == 1:
        TMP["PSJMR", $J, 1] = TMP["PS51.2", MR, 0].split('^')[0] + '^' + TMP["PS51.2", MR, 0].split('^')[2] + '^' + MR + '^' + TMP["PS51.2", MR, 0].split('^')[1] + '^' + (
            1 if TMP["PS51.2", MR, 0].split('^')[6] else 0) + '^D'


def START1(PSJORD, PSJQOF):
    if not PSJQOF:
        PSJQOF = 0

    PSJORD1 = {}
    TMP["PSJMR", $J] = {}

    if PSJORD[0] == 1:
        PSJOPAC = "I"
        PSJORD = PSJORD[1].split('^')[0]
        MEDRT(PSJORD)
        if PSJQOF == 1:
            MCT = len(TMP["PSJMR", $J, "A"])
            ALLMED(MCT)
        PSJORD1 = TMP["PSJMR", $J].copy()
        REMDUP()
        PSJORD = PSJORD1.copy()
        TMP["PSJMR", $J] = {}
        return

    for X in range(1, len(PSJORD)):
        PSJORD1[X] = {}
        PSJORD[X] = PSJORD[X].split('^')[0]
        MEDRT(PSJORD)
        PSJORD1[X] = TMP["PSJMR", $J].copy()
        TMP["PSJMR", $J] = {}

    OVERLAP()
    if PSJQOF == 1:
        MCT = len(MRTEMP2["A"])
        ALLMED(MCT)
    PSJORD1 = TMP["PSJMR", $J].copy()
    REMDUP()
    MULTIDEF(PSJORD, PSJORD1)
    TMP["PSJMR", $J] = PSJORD1.copy()
    TMP["PSJMR", $J] = {}
    MRTEMP2, MRTEMP, MRNODE, MRNODE1, PSSCNTR1, PSJOPAC, ZZX, SAMEDEF, DEFAULT = None, None, None, None, None, None, None, None, None


def MEDRT(PSJORD):
    MR, X, PSJDFNO, MCT, PM, II = None, None, None, None, None, None

    MR, MCT, X = 0, 1, 0
    PSJDFNO = int(TMP["PS50.7", PSJORD, 0].split('^')[1])
    MR = int(TMP["PS50.7", PSJORD, 0].split('^')[6])

    if MR and TMP["PS51.2", MR, 0].split('^')[4] == 1:
        TMP["PSJMR", $J, 1] = MR + '^' + TMP["PS51.2", MR, 0].split('^')[0] + '^' + TMP["PS51.2", MR, 0].split('^')[2] + '^' + TMP["PS51.2", MR, 0].split('^')[1] + '^D'
        MCT += 1

    if TMP["PS50.7", PSJORD, 0].split('^')[13] != "Y":
        II = 0
        while II:
            PM = int(TMP["PS50.7", PSJORD, 3, II, 0])
            if PM and TMP["PS51.2", PM, 0].split('^')[4] == 1:
                TMP["PSJMR", $J, MCT] = PM + '^' + TMP["PS51.2", PM, 0].split('^')[0] + '^' + TMP["PS51.2", PM, 0].split('^')[2] + '^' + TMP["PS51.2", PM, 0].split('^')[1]
                MCT += 1
            II += 1

    MR = 0
    while MR:
        X = int(TMP["PS50.606", PSJDFNO, "MR", MR, 0])
        if X != int(TMP["PS50.7", PSJORD, 0].split('^')[6]):
            MRNODE = TMP["PS51.2", X, 0]
            if MRNODE.split('^')[4] == 1:
                TMP["PSJMR", $J, MCT] = X + '^' + MRNODE.split('^')[0] + '^' + MRNODE.split('^')[2] + '^' + MRNODE.split('^')[1]
                MCT += 1
        MR += 1


def ALLMED(MCT):
    MR, MRNODE = None, None

    if MCT is None:
        MCT = 0

    MR, MRNODE = "", ""
    for MR in range(1, MR):
        MRNODE = TMP["PS51.2", MR, 0]
        if MRNODE.split('^')[4] == 1 and MRNODE.split('^')[6] == 1:
            MCT += 1
            TMP["PSJMR", $J, MCT] = MR + '^' + MRNODE.split('^')[0] + '^' + MRNODE.split('^')[2] + '^' + MRNODE.split('^')[1]


def OVERLAP():
    MR, MRNODE, X, PSSCNTR1 = None, None, None, None

    MRTEMP, MRTEMP2 = {}, {}
    MR, MRNODE, X = "", "", ""
    for X in range(1, len(PSJORD1) + 1):
        for MR in PSJORD1[X]:
            MRNODE = PSJORD1[X][MR].split('^')[0]
            MRTEMP[MRNODE] += 1

    MR = ""
    for MR in MRTEMP:
        if MRTEMP[MR] != PSJORD[0]:
            del MRTEMP[MR]

    if not MRTEMP:
        PSJORD1 = ""
        return

    PSSCNTR1 = 1
    for MR in MRTEMP:
        MRNODE = TMP["PS51.2", MR, 0]
        MRTEMP2[PSSCNTR1] = MR + '^' + MRNODE.split('^')[0] + '^' + MRNODE.split('^')[2] + '^' + MRNODE.split('^')[1]
        PSSCNTR1 += 1

    PSJORD1 = MRTEMP2.copy()


def REMDUP():
    MR, MRNODE = None, None

    MR, MRNODE = "", ""
    for MR in PSJORD1:
        MRNODE = PSJORD1[MR].split('^')[1]
        if MRNODE in MRTEMP:
            del PSJORD1[MR]
        else:
            MRTEMP[MRNODE] = PSJORD1[MR]

        if MR == 1 and PSJORD1[MR].split('^')[5] == "D":
            MRTEMP[MR] = PSJORD1[MR]

    MR = ""
    for MR in MRTEMP:
        if not MR.isdigit():
            del MRTEMP[MR]

    if PSJORD[0] == 1:
        PSJORD1 = MRTEMP.copy()
    MRTEMP = {}


def MULTIDEF(PSJORD, PSJORD1):
    ZZX, DEFAULT, SAMEDEF, DEFAULT = None, "", 0, []

    DEFAULT = ""
    for ZZX in PSJORD:
        DEFAULT = PSJORD[ZZX]
        DEFAULT[ZZX] = TMP["PS50.7", DEFAULT, 0].split('^')[6]

    ZZX = ""
    for ZZX in DEFAULT:
        if DEFAULT[ZZX] != DEFAULT[1]:
            SAMEDEF = 0
            break
        SAMEDEF = 1

    if SAMEDEF == 0:
        PSJORD1 = ""
        return

    if SAMEDEF == 1 and DEFAULT[1] == "":
        return

    ZZX = ""
    for ZZX in PSJORD1:
        if PSJORD1[ZZX].split('^')[0] == DEFAULT[1]:
            PSJORD1[ZZX] += "D"


def IND():
    TMP["PSJIND", $J] = {}
    IND, I, ARR, K = None, None, None, None

    K = 0
    if TMP["PS50.7", PSJORD, 4, 2]:
        K += 1
        TMP["PSJIND", $J, K] = ENLU_PSSGMI(TMP["PS50.7", PSJORD, 4, 2])

    for I in TMP["PS50.7", PSJORD, "IND", "B"]:
        IND = ENLU_PSSGMI(I)
        if IND not in ARR:
            ARR[IND] = ""

    for I in ARR:
        K += 1
        TMP["PSJIND", $J, K] = I