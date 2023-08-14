# PSSFIL ;BIR/CML3-SON OF VARIOUS FILES' UPKEEP ; 09/15/97 13:21
# ;;1.0;PHARMACY DATA MANAGEMENT;;9/30/97
# ;
def ENDTE():
    if not '^PS(57.7,DA,1,0' in globals():
        print("NO TEAMS ENTERED TO CHOOSE FROM!")
        return
    DIC = "^PS(57.7," + str(DA) + ",1,"
    DIC(0) = "EQM"
    DIC(^DICN)
    if Y <= 0:
        return
    X = int(Y)
    return

def ENOAOPT():
    ENSWT()
    if % < 0:
        return
    DA = 1
    DIE = "^PS(59.7,"
    DR = "[PSJ OAOPT]"
    ^DIE
    X = "PSGSETU"
    ^%ZOSF("TEST")
    if ?:
        ^PSGSETU
    return

def ENSWT():
    X = "PSGFILD1"
    ^%ZOSF("TEST")
    if ?:
        while True:
            print("Do you want the instructions for auto-discontinue set-up")
            % = 1
            ^DICN
            if %:
                break
        if % < 0:
            return
        if % == 1:
            ^PSGFILD1
    while True:
        print("Do you want the package to set-up all of your wards for auto-discontinue")
        % = 2
        ^DICN
        if %:
            break
        ?SWTH()
    if % != 1:
        return
    print("Working...")
    PSGW = 0
    Q = 0
    while True:
        Q = Q + 1
        if not Q in globals():
            break
        if not ^DIC(42,Q,0) in globals():
            continue
        X = ^DIC(42,Q,0)
        PSGW(Q) = X if X != "" else Q + ";DIC(42,"
        PSGW = PSGW + 1
    if not ^PS(59.7,1,22,0) in globals():
        ^PS(59.7,1,22,0) = "^59.722P"
    PSGX = 0
    while True:
        PSGX = PSGX + 1
        if not PSGW(PSGX) in globals():
            break
        print(PSGW(PSGX), "...")
        if not ^PS(59.7,1,22,PSGX) in globals():
            ?SW()
        PSGY = 0
        while True:
            PSGY = PSGY + 1
            if not PSGW(PSGY) in globals():
                break
            if PSGX != PSGY and not ^PS(59.7,1,22,PSGX,1,PSGY,0) in globals():
                ?SW1()
    %=0
    return

def SW():
    ^PS(59.7,1,22,
    DIC = "^PS(59.7,1,22,"
    DIC(0) = "L"
    DA(1) = 1
    DINUM = PSGX
    ^DICN
    if not ^PS(59.7,1,22,PSGX,1,0) in globals():
        ^(0) = "^59.7221P"
    return

def SW1():
    ^PS(59.7,1,22,PSGX,1,
    DIC = "^PS(59.7,1,22," + str(PSGX) + ",1,"
    DIC(0) = "L"
    DA(2) = 1
    DA(1) = PSGX
    DINUM = PSGY
    ^DICN
    return

def SWTH():
    print("Enter \"YES\" to have the package set-up all of your wards for auto-discontinue")
    print("for you.  Enter \"NO\" if you prefer to set-up the wards individually.  Enter \"^\"")
    print("to abort the set-up.")
    print()
    print("If you answer YES, you will still be able to add, edit and delete individual")
    print("wards.")
    print()
    print("PLEASE NOTE that this is not a flag for the package, but a one-time action.")
    print("If you add new wards to your WARD LOCATION file, you will")
    print("need to add those")
    print("wards here.")
    return

def ENSUEP():
    while True:
        DIC = "^PS(53.45,"
        DIC(0) = "AELQZ"
        DIC("A") = "Select INPATIENT USER: "
        DLAYGO = 53.45
        ^DIC
        if Y <= 0:
            break
        DA = int(Y)
        DIE = "^PS(53.45,"
        DR = "[PSJ IUP SUPER EDIT]"
        IU = int(Y(0))
        for X in range(1, 4):
            if ^XUSEC("PSJ " + $P("RPHARM^RNURSE^PHARM TECH", "^", X), IU):
                break
        if not $T:
            X = 0
        R = ^VA(200,IU,"PS")
        R = 0 if not R else 1 if not $P(R,"^",4) else $P(R,"^",4) > DT
        print("This user is a", $P("PHARMACIST^NURSE^PHARMACY TECHNICIAN", "^", X), end="")
        print("WARD CLERK" if not X and not R else ".", end="")
        if R:
            print(" and a", end="")
            print("PROVIDER" if X else ".")
    X = "PSGSETU"
    ^%ZOSF("TEST")
    if ?:
        ^PSGSETU
    return

def ENUUEP():
    X = "PSGSETU"
    ^%ZOSF("TEST")
    if ?:
        ^PSGSETU
    DA = PSJSYSP
    DIE = "^PS(53.45,"
    DR = "[PSJ IUP USER EDIT]"
    ^DIE
    ^XUTL("OR",$J,"PSG")
    ^PSGSETU
    for X in range(1, 4):
        if ^XUSEC("PSJ " + $P("RPHARM^RNURSE^PHARM TECH", "^", X), DUZ):
            break
    if not $T:
        X = 0
    R = ^VA(200,DUZ,"PS")
    R = 0 if not R else 1 if not $P(R,"^",4) else $P(R,"^",4) > DT
    print("You are a", $P("PHARMACIST^NURSE^PHARMACY TECHNICIAN", "^", X), end="")
    print("WARD CLERK" if not X and not R else ".", end="")
    if R:
        print(" and a", end="")
        print("PROVIDER" if X else ".")
    print("PLEASE NOTE: Any changes made take effect immediately.")
    return

def ENIWPE():
    while True:
        DIC = "^PS(59.6,"
        DIC(0) = "AELMQ"
        DIC("A") = "Select WARD: "
        DLAYGO = 59.6
        ^DIC
        if Y <= 0:
            break
        DA = int(Y)
        DIE = "^PS(59.6,"
        DR = "[PSJ IWP EDIT]"
        ^DIE
    ^TMP("OR",$J,"PSG")
    X = "PSGSETU"
    ^%ZOSF("TEST")
    if ?:
        ^PSGSETU
    return

def ENPDE():
    while True:
        DIC = "^PS(50.3,"
        DIC(0) = "AELMQ"
        DIC("A") = "Select PRIMARY DRUG: "
        DLAYGO = 50.3
        ^DIC
        if Y <= 0:
            break
        DA = int(Y)
        DIE = "^PS(50.3,"
        DR = "[PSS PD EDIT]"
        ^DIE
    return

def ENALU():
    PSJ = DA(1)
    DIC = "^PS(50.35,"
    DIC(0) = "EIMZ" if not '$D(PSJPRE4) else "EIM"
    ^DIC1
    ^DIC
    if Y <= 0:
        X = $P(Y(0),"^",2)
        if X == "" or ^PS(50.3,PSJ,1,"B",X):
            X = None
    return X

def ENAQ():
    X = DZ
    DIC = "^PS(50.35,"
    DIC(0) = "EIMQ"
    ^DIC1
    ^DIC
    return