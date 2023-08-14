def PSSJSPU():
    """
    BIR/CML3,WRT-SCHEDULE PROCESSOR UTILITY
    06/24/96 9:20
    """
    PSJC = 0
    RUN()

def DONE():
    """
    Clean up variables
    """
    AM, CD, H, HCD, I, J, M, MID, OD, PDL, ST, Q, QQ, WD, WDT, WS, WS1, X, X1, X2, XX = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

def RUN():
    """
    Main processing logic
    """
    if PSJSCH == "PRN" or PSJOFD < PSJSD or (PSJOSD > PSJFD and PSJTS == "O"):
        return

    if (
        PSJTS == "O"
        or PSJSCH == "STAT"
        or PSJSCH == "NOW"
        or PSJSCH == "ONCE"
        or PSJSCH == "ONE-TIME"
        or PSJSCH == "ON CALL"
        or PSJSCH == "ONE TIME"
    ):
        PSJC = 1
        PSJC[str(+PSJOSD)] = ""
        return

    ST = PSJOSD
    CD = PSJOFD if PSJFD > PSJOFD else PSJFD
    OD = ST if ST > PSJSD else PSJSD
    MID = 1

    if PSJTS == "R":
        RANGE()
    elif "S" in PSJTS:
        SHFT()
    elif "@" in PSJSCH or "D" in PSJTS:
        MWF()
    else:
        TS = PSJAT
        if PSJM > 1440 and TS and not (PSJM % 1440):
            TSFMN()
        if TS > 0 and TS[0] in "24":
            if PSJSD > ST:
                ST = PSJSD
            TS()
        elif PSJM <= 0:
            PSJC = "-1^PSJM"
        else:
            MN()

def MN():
    """
    Process minutes (MN) only
    """
    OD = X1 = PSJSD
    X2 = ST
    X = X2 - X1
    if X > 1:
        AM = X - 1 * 1440 // PSJM * PSJM
        ADD()
        ST = X
    X = ST
    for I in range(1000):
        AM = PSJM * I
        ST = X
        if AM:
            ADD()
        if X > CD or (CD == PSJOFD and X >= CD):
            break
        if X >= OD:
            PSJC += 1
            PSJC[str(+X)] = ""

def TSFMN():
    """
    Process admin times and minutes#1440=0
    """
    X = ST.split(".")
    MID = PSJM // 1440
    for I in range(1000):
        X1 = ST.split(".")
        X2 = MID * I
        if X2:
            C^%DTC()
        if X >= CD:
            break
        if X >= (PSJSD // 1):
            ST = X if PSJSD // 1 < X else PSJSD
            break

def MTS():
    """
    Process admin times
    """
    global CD, ST
    CD = ST if HCD.split(".") > ST else HCD
    ST = ST if OD.split(".") < ST else OD
    if PSJTS == "DR":
        if ST <= CD:
            PSJC += 1
            PSJC[ST] = CD
        return

    TS()
    for Q in range(1000):
        XX = TS.split("-", Q)
        if not XX:
            X1 = ST.split(".")
            X2 = MID
            C^%DTC()
            ST = X
            Q = 1
        for QQ in range(Q, 1000):
            XX = TS.split("-", QQ)
            if not XX:
                ST = ST.split(".")
                ST = ST[0] + "." + XX
                if X > CD or (CD == PSJOFD and X >= CD):
                    break
                PSJC += 1
                PSJC[+ST] = ""
                ST = X

def MWF():
    """
    Process multiple weekdays
    """
    TS = PSJAT if PSJTS != "DR" else PSJAT
    HCD = CD
    WS = PSJSCH.split("@")[0]
    X = OD.split(".")
    PDL = "-"
    if "-" not in WS and any(char.isdigit() for char in WS):
        for PSJ1 in range(len(WS)):
            if WS[PSJ1] in "!@#$%^&*()_-+=<>,.?/\\|":
                PDL = WS[PSJ1]
                break
    for PSJ1 in range(1000):
        X1 = OD.split(".")
        X2 = PSJ1
        if X2:
            C^%DTC()
        if X > HCD:
            break
        ST = X
        DW^%DTC()
        X = X + "S"
        for PSJ2 in range(1, len(WS.split(PDL))):
            if WS.split(PDL)[PSJ2] not in X.split(WS.split(PDL)[PSJ2]):
                MTS()
                break

def ADD():
    """
    Helper function to add minutes to a time
    """
    global X, AM, HRS, MN
    if not AM:
        X = ST
        return
    T = 1
    if AM < 0:
        T = -1
        AM = -AM
    X2 = AM // 1440
    AM = AM - (X2 * 1440)
    H = AM // 60
    MN = AM % 60
    HRS = int(str(ST) + "00"[len(str(HRS)) < 2] + str(HRS) + "00"[len(str(MN)) < 2] + str(MN))
    if MN:
        MN = MN + (M * T)
        if MN > 59:
            MN = MN - 60
            H = H + 1
        if MN < 0:
            MN = MN + 60
            H = H + 1
    if H:
        HRS = HRS + (H * T)
        if HRS > 24 or (HRS == 24 and MN):
            HRS = HRS - 24
            X2 = X2 + 1
        if HRS < 0:
            HRS = HRS + 24
            X2 = X2 + 1
    if X2:
        X1 = X.split(".")
        X2 = X2 * T
        C^%DTC()
    X = int(str(X) + "." + str(HRS)[len(str(HRS)) < 2] + str(MN)[len(str(MN)) < 2])

def SHFT():
    """
    Process shift schedules
    """
    global TM
    TM = {}
    for TM_key in PSJAT:
        TM[TM_key] = ""
    if OD // 1 == CD // 1:
        for TM_key in TM:
            X = TM_key
            if "-" in TM_key and TM_key:
                TM_key = TM_key.split("-")
                if TM_key[1] < TM_key[0]:
                    TM_key[1] = 24
                X1 = OD // 1 + "." + TM_key[0]
                X2 = OD // 1 + "." + TM_key[1]
                if X1 <= CD and X2 >= OD:
                    PSJC += 1
                    PSJC[+X1] = +X2
    if OD // 1 == CD // 1:
        return
    LD = {1: OD}
    for LD in range(2, 1000):
        X1 = OD // 1
        X2 = LD - 1
        C^%DTC()
        LD[LD] = X
        if CD // 1 == X:
            break
    for LDC in range(1, LD - 1):
        for TM_key in TM:
            X1 = "." + TM_key.split("-")[0]
            X2 = "." + TM_key.split("-")[1]
            X3 = CD % 1
            if X2 >= X1 and X3 >= X1:
                PSJC += 1
                X = LD[LDC] + X1 if LDC > 1 else LD[LDC] + X1
                Y = LD[X2 < X1 + LDC] + X2
                if Y > CD:
                    Y = CD
                PSJC[X] = Y
    for TM_key in TM:
        X1 = "." + TM_key.split("-")[0]
        X2 = "." + TM_key.split("-")[1]
        X3 = CD % 1
        if X2 >= X1 and X3 >= X1:
            PSJC += 1
            X = LD[LDC] + X1
            Y = CD if X3 < X2 else LD[LDC] // 1 + X2
            PSJC[CD // 1 + X1] = Y

def RANGE():
    """
    Process range schedules
    """
    global ST
    if not PSJM:
        PSJC += 1
        PSJC[OD] = CD
        return
    ST = OD
    while True:
        AM = PSJM
        ADD()
        PSJC += 1
        PSJC[ST] = X
        if X >= CD:
            break
        AM = 1
        ST = X
        ADD()
        ST = X

PSSJSPU()