# PSSLOCK ;BIR/RSB-Pharmacy patient lock ;09/15/97 13:30
# 1.0;PHARMACY DATA MANAGEMENT;**26,58,125**;9/30/97;Build 2
#
# Reference to ^ORX2 supported by DBIA #867
# Reference to ^PS(53.1 supported by DBIA #2140
# Reference to ^PS(52.41 supported by DBIA #2844
# Reference to ^PSRX supported by DBIA #2845
# Reference to ^PS(55 supported by DBIA #2191

def L(DFN, DIS):
    if PSONOLCK:
        return 1
    FLAG = None
    XTMP = {"PSSLOCK": {}}
    XTMP["PSSLOCK"][0] = PDATE()
    if DFN not in XTMP["PSSLOCK"]:
        NOW = NOW()
        XTMP["PSSLOCK"][DFN] = f"{DUZ}^{NOW}"
        FLAG = lock_xtmp(DFN)
    if DFN in XTMP["PSSLOCK"]:
        return R()

def UL(DFN):
    if PSONOLCK:
        return
    unlock_xtmp(DFN)
    del XTMP["PSSLOCK"][DFN]

def R():
    if get_xtmp(DFN)["DUZ"] == DUZ:
        return 1
    if lock_xtmp(DFN):
        NOW = NOW()
        get_xtmp(DFN)["DUZ"] = DUZ
        get_xtmp(DFN)["NOW"] = NOW
        return 1
    if not lock_xtmp(DFN):
        if DIS == 1:
            print(WHO(DFN))
        Y = get_xtmp(DFN)["NOW"]
        formatted_time = format_time(Y)
        return (0, get_username(get_xtmp(DFN)["DUZ"]), formatted_time) if DIS == 0 else 0

def PDATE():
    from datetime import datetime, timedelta
    X1 = datetime.now().date()
    X2 = timedelta(days=14)
    return f"{(X1 + X2).strftime('%Y%m%d')}^{X1.strftime('%Y%m%d')}^Pharmacy patient locks"

def WHO(DFN):
    Y = get_xtmp(DFN)["NOW"]
    formatted_time = format_time(Y)
    return f"{get_username(get_xtmp(DFN)['DUZ'])} is editing orders for this patient ({formatted_time})"

def LS(DFN, X):
    OR100 = ORD(DFN, X)
    if OR100 == 0:
        return 1
    L = lock1_ORX2(OR100)
    if L:
        return 1
    if not L:
        print(f"{L.split('^')[1]}\a")
        pause_VALM1()
        return 0
    return 0

def UNL(DFN, X):
    UNLK1_ORX2(ORD(DFN, X))

def ORD(DFN, X):
    ORD100 = None
    if "N" in X or "P" in X:
        ORD100 = "^PS(53.1,{X},0)"
    elif "V" in X:
        ORD100 = f"^PS(55,{DFN},'IV',{X},0)"
    else:
        ORD100 = f"^PS(55,{DFN},5,{X},0)"
    return int(get_value(ORD100, 21))

def PSOL(X):
    global PSOMSG
    PSOMSG = 1
    if "S" in X:
        X = int(get_value(f"^PS(52.41,{X},0)"))
        if X:
            PSOMSG = lock1_ORX2(X)
    else:
        X = int(get_value(f"^PSRX,{X},'OR1'"))
        if X:
            PSOMSG = lock1_ORX2(X)

def PSOUL(X):
    if "S" in X:
        X = int(get_value(f"^PS(52.41,{X},0)"))
        if X:
            UNLK1_ORX2(X)
    else:
        X = int(get_value(f"^PSRX,{X},'OR1'"))
        if X:
            UNLK1_ORX2(X)