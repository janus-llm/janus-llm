# DRIVER FOR COMPILED XREFS FOR FILE #52.6 ; 10/30/18
# 
DH = None
DU = None
DIKILL = None
DISET = None
DIKJ = None
DIKZ = None
DIKYR = None
DIKZA = None
DIK0Z = None
DIKZK = None
DIKDP = None
DIKM1 = None
DIKUP = None
DIKUM = None
DV = None
DIIX = None
DIKF = None
DIAU = None
DIKNM = None
DIKDA = None
DIKLK = None
DIKLM = None
DIKY = None
DIXR = None
DIKCOND = None
DIKSVDA = None
DIKPUSH = None
X1 = None
X2 = None

if not 'DIKSAT' in globals():
    DIKLK = DIK + DA + ")"
    lock_success = False
    try:
        lock_success = lock(DIKLK, 10)
        if not lock_success:
            DIKLK = None
    except Exception:
        pass

DI = None

if not 'DIKSAT' in globals() and 'DIKLK' in globals():
    unlock(DIKLK)
    DIKLK = None

Q = None

def DI():
    global DIKM1
    global DIKUM
    global DA
    global DV
    global DIKUP
    global DH
    global DIKZ1
    if not 'DIKKS' in globals():
        if DIKZ1 == DH:
            PSSVX61()
        DA = DIKUP
        if DIKZ1 == DH:
            PSSVX64()
        if DIKZ1 != DH:
            KILL()
        if DIKZ1 != DH:
            DA()
        if DIKZ1 != DH:
            SET()
        DA()
    if 'DIKIL' in globals():
        if DIKZ1 == DH:
            PSSVX61()
        if DIKZ1 == DH:
            DIKM1 = 1
        if DIKZ1 != DH:
            KILL()
        DA = DIKUP
        if DIKM1 > 0:
            KIL1()
        DA()
    if 'DIKST' in globals():
        if DIKZ1 == DH:
            PSSVX64()
        if DIKZ1 != DH:
            SET()
        DA()
    if 'DIKSAT' in globals():
        SET1()
        DA()
    return

def DA():
    global DA
    global DV
    global DIKUP
    DA = {}
    for DV in range(1, len(DIKUP) + 1):
        DA[DV] = DIKUP[DV]
    DA = DIKUP
    return

def SET1():
    global DA
    global DCNT
    global DU
    global DIK
    global DIKLK
    global DIKY
    global DIKY
    global DIKZ1
    global DH
    global DIKUM
    global DIKM1
    DA = 0
    DCNT = 0
    DU = DIK[:-1]
    if DIK.find(",") != -1:
        DIKLK = DU + ")"
    else:
        DIKLK = DU
    lock_success = False
    try:
        lock_success = lock(DIKLK, 10)
        if not lock_success:
            DIKLK = None
    except Exception:
        pass
    C()
    return

def C():
    global DA
    global DCNT
    global DIK
    global DIKLK
    global DIKY
    global DU
    global DIKZ1
    global DIKUP
    global DB
    if eval("$O(" + DIK + "DA)) <= 0"):
        DA = C1(DA)
        DIK[0] = DIK[0][:2] + DA + DCNT
        DCNT = None
        if 'DIKLK' in globals():
            unlock(DIKLK)
            DIKLK = None
        return
    DIKY = DA
    DA = {}
    DU = 1
    DCNT = DCNT + 1
    if DA == "":
        DIKY = DA = -1
    if DIKZ1 == DH:
        PSSVX64()
    if DIKZ1 != DH:
        SET()
    if DIKZ1 != DH:
        DA()
    DB[0] = None
    DA = DIKY
    C()
    return

def C1(A):
    global DIK
    if eval("$P($G(@" + DIK + "A,0)),U)>"""):
        return A
    while True:
        A = eval("+$O(" + DIK + "A),-1)")
        if eval("$P($G(@" + DIK + "A,0)),U)>""") or A <= 0:
            break
    return A

def KILL():
    global DIKILL
    global DIKZK
    global DIKZ1
    global DIKUM
    global DIKM1
    if DIKZ1 == 52.61 and DIKUM >= 1:
        DIKM1 = 1
        A1()
    if DIKZ1 == 52.63 and DIKUM >= 1:
        DIKM1 = 1
        A1()
    return

def SET():
    global DISET
    global DIKZK
    global DIKPUSH
    global DIKZ1
    global DIKUM
    global DIKM1
    if DIKZ1 == 52.61 and DIKUM >= 1:
        DIKM1 = 1
        A1()
    if DIKZ1 == 52.63 and DIKUM >= 1:
        DIKM1 = 1
        A1()
    return

def KIL1():
    global DIK
    global DA
    global DIKZ1
    global DIKUP
    global Y
    global DH
    global X
    if DIKZ1 == 52.61 and DIKUM >= 1:
        DIKM1 = 1
        A1()
    if DIKZ1 == 52.63 and DIKUM >= 1:
        DIKM1 = 1
        A1()
    if eval("$D(@" + DIK + "DA))"):
        Y = eval("@" + DIK + "DA)")
        DH = eval("$S($O(@" + DIK + "DA))'>0:0,1:$P(Y,U,4)-1)")
        X = eval("$P($P(Y,U,3),U,DH>0)")
        if X == DA:
            X = 3
        eval(@"@" + DIK + "DA)=$P(Y,U,1,2)_U_X_U_DH")
    return

def Q():
    global DIKGP
    global DIKZ1
    DIKGP = None
    DIKZ1 = None
    return

def A1():
    global DIKOZ
    global DIKZA
    global DIKZK
    if DIKZ1 == 52.61:
        DIKOZ = 1
        DIKZA = "CREA"
    else:
        DIKOZ = 1
        DIKZA = "DELE"
    if eval("$D(^DD(" + DIKZ1 + "," + DIKZZ + ",1," + DIKZR + ",DIKZA))"):
        return "...(`" + eval("^(DIKZA)") + "` BULLETIN WILL NOT BE TRIGGERED) "
    return

def PSSVX61():
    return

def PSSVX64():
    return

def PSSVX65():
    return

def PSSVX66():
    return

def lock(lock_name, timeout):
    # Implement lock logic here
    pass

def unlock(lock_name):
    # Implement unlock logic here
    pass