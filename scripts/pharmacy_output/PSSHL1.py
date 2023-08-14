def PSSHL1():
    """
    BIR/RLW/WRT-BUILD HL7 MESSAGE TO POPULATE ORDERABLE ITEM FILE ;09/08/97
    1.0;PHARMACY DATA MANAGEMENT;**38,68,125**;9/30/97;Build 2
    External reference to ORD(101 supported by DBIA 872
    PSJEC=event code from HL7 table 8.4.2.1
    PSJSPIEN=ien to super-primary drug file (#50.7)
    SPDNAME=.01 field (name) of super-primary drug
    LIMIT=number of fields in HL7 segment being built
    """
    print("!!?3,\"This routine should not be accessed through programmer mode!\",")
    return

def EN1():
    """
    start here for pre-install auto load
    """
    MENU, MENUP, ITEM = None, None, None
    PRO()
    if XPDABORT:
        return
    PSSMFU = +$O(^PS(59.7, 0))
    if $P(^PS(59.7, PSSMFU, 80), "^", 2) == 4:
        K PSSMFU
        return
    APPL, CODE, FIELD, LIMIT, MFE, PSJI, SEGMENT, SPDNAME, SYN, SYNONYM, USAGE, X = None, None, None, None, None, None, None, None, None, None, None
    if not '$D(^XTMP("PSO_V7 INSTALL", 0)):
        X1 = DT
        X2 = +7
        C^%DTC
        ^XTMP("PSO_V7 INSTALL", 0) = DT + "^" + X + "^OUTPATIENT V7 KIDS INSTALL"
        L +^XTMP("PSO_V7 INSTALL", 0) : $S($G(DILOCKTM) > 0 : DILOCKTM, 1 : 3)
        G SKIP
    while '$D(^XTMP("PSO_V7 INSTALL", 0)):
        L +^XTMP("PSO_V7 INSTALL", 0) : $S($G(DILOCKTM) > 0 : DILOCKTM, 1 : 3)
        if $T:
            break
    if not '$D(^XTMP("PSO_V7 INSTALL", 0)):
        X1 = DT
        X2 = +7
        C^%DTC
        ^XTMP("PSO_V7 INSTALL", 0) = DT + "^" + X + "^OUTPATIENT V7 KIDS INSTALL"
        L +^XTMP("PSO_V7 INSTALL", 0) : $S($G(DILOCKTM) > 0 : DILOCKTM, 1 : 3)
    if $P(^PS(59.7, PSSMFU, 80), "^", 2) == 4:
        L -^XTMP("PSO_V7 INSTALL", 0)
        K ^XTMP("PSO_V7 INSTALL", 0)
        return
    SKIP:
    PSJEC = "MAD"
    CODE = "REP"
    INIT()
    LOOP()
    MF^PSSHLU(PSJI)
    PSLSITE = +$O(^PS(59.7, 0))
    $P(^PS(59.7, PSLSITE, 80), "^", 2) = 4
    K PSLSITE
    L -^XTMP("PSO_V7 INSTALL", 0)
    K ^XTMP("PSO_V7 INSTALL", 0)
    K ^TMP("HLS", $J, "PS")
    K PSJEC, PSJSPIEN, PSJCLEAR, PSSMFU
    return

def EN2(PSJSPIEN, PSJEC):
    """
    start here for \"manual\" update
    """
    PSLSITE = +$O(^PS(59.7, 0))
    if +$P($G(^PS(59.7, PSLSITE, 80)), "^", 2) < 4:
        K PSLSITE
        return
    K PSLSITE
    if not $P($G(^PS(50.7, PSJSPIEN, 0)), "^", 4):
        PSJEC = "MAC"
    K PSLSITE
    APPL, CODE, FIELD, PSJI, LIMIT, MFE, SEGMENT, SPDNAME, SYN, SYNONYM, USAGE, X, ZCOUNT, ZUSAGE = None, None, None, None, None, None, None, None, None, None, None, None
    CODE = "UPD"
    INIT()
    MFE(PSSIVID)
    MF^PSSHLU(PSJI)
    K ^TMP("HLS", $J, "PS")
    return

def INIT():
    """
    initialize HL7 variables, set master file identification segment fields
    """
    PSJI = 0
    LIMIT = 6
    HLMTN = "MFN"
    PSSIVID = $$GTIVID()
    INIT^PSSHLU()
    X PSJCLEAR
    FIELD[0] = "MFI"
    FIELD[1] = "50.7^PHARMACY ORDERABLE ITEM^99DD"
    FIELD[3] = CODE
    FIELD[6] = "NE"
    SEGMENT^PSSHLU(LIMIT)
    return

def LOOP():
    """
    loop through PHARMACY ORDERABLE ITEM file
    """
    PSJSPIEN = 0
    while PSJSPIEN:
        PSJSPIEN = $O(^PS(50.7, PSJSPIEN))
        if not PSJSPIEN:
            continue
        MFE(PSSIVID)
    return

def MFE(PSSIVID):
    """
    set master file entry segment fields
    """
    LIMIT = 4
    X PSJCLEAR
    X = $G(^PS(50.7, PSJSPIEN, 0))
    FIELD[0] = "MFE"
    FIELD[1] = PSJEC
    FIELD[3] = $P($G(^PS(50.7, PSJSPIEN, 0)), "^", 4)
    if FIELD[3]:
        FIELD[3] = $$HLDATE^HLFNC(FIELD[3])
    FIELD[4] = "^^^"_PSJSPIEN_"^"_$P(X, "^")+"~"_$P($G(^PS(50.606, $P(X, "^", 2), 0)), "^")+"~"_$S($P($G(^PS(50.7, PSJSPIEN, 0)), "^", 3):$G(PSSIVID), 1:"")+"^99PSP"
    SEGMENT^PSSHLU(LIMIT)
    ZPS()
    ZSY()
    return

def ZPS():
    """
    get USAGE from dispense drug(s), set ZPS segment
    """
    LIMIT = 2
    X PSJCLEAR
    FIELD[0] = "ZPS"
    USAGE = $$USAGE^PSSHLU(PSJSPIEN)
    if USAGE == "" and not $P($G(^PS(50.7, PSJSPIEN, 0)), "^", 9) and not $P($G(^PS(50.7, PSJSPIEN, 0)), "^", 12):
        return
    for I in "I", "O", "A", "B", "V":
        if +$P(USAGE, I, 2) > 0:
            FIELD[1] = FIELD[1] + I
    if $P($G(^PS(50.7, PSJSPIEN, 0)), "^", 9):
        FIELD[1] = FIELD[1] + "S"
    if $P($G(^PS(50.7, PSJSPIEN, 0)), "^", 10):
        FIELD[1] = FIELD[1] + "N"
    if $P($G(^PS(50.7, PSJSPIEN, 0)), "^", 12):
        FIELD[2] = 1
    SEGMENT^PSSHLU(LIMIT)
    return

def ZSY():
    """
    get SYNONYMs
    """
    LIMIT = 2
    FIELD[0] = "ZSY"
    SYNONYM = ""
    J, SYNIEN = 0, 0
    while SYNIEN:
        SYNIEN = $O(^PS(50.7, PSJSPIEN, 2, SYNIEN))
        if not SYNIEN:
            continue
        SYNONYM = $P($G(^(SYNIEN, 0)), "^")
        if SYNONYM == "":
            continue
        FIELD[1] = "1"
        FIELD[2] = SYNONYM
        SEGMENT^PSSHLU(LIMIT)
    return

def PRO():
    """
    Check for protocols
    """
    MENU = "PS MFSEND OR"
    ITEM = "OR ITEM RECEIVE"
    MENUP = $O(^ORD(101, "B", MENU, 0))
    X = $O(^ORD(101, "B", ITEM, 0))
    if not X:
        print("!!?5,\"Sorry, you need the OR ITEM RECEIVE protocol to proceed,\",!?5,\"which is exported with Order Entry/Results Reporting V3!\",!")
        XPDABORT = 1
        return
    if $D(^ORD(101, MENUP, 10, "B", X)):
        return
    if $D(^ORD(101, MENUP, 10, 0))[0:
        ^ORD(101, MENUP, 10, 0) = "^"_"101.01PA"
    DIC = "^ORD(101,"_MENUP_",10,"
    DIC(0) = "L"
    DLAYGO = 101.01
    DA(1) = MENUP
    FILE^DICN
    K DIC
    if Y < 0:
        print("!!?5,\"Sorry, unable to add OR ITEM RECEIVE protocol as an Item to the PS MFSEND\",!,\"protocol, cannot proceed!\",!")
        XPDABORT = 1
    return

def ENIVID():
    """
    Edit IV Identifier field to be displayed with IV Orderable Items.
    """
    DA, DIC, DIE, DRG, PSSOI, PSSIVID, PSSFIL, PSSDRG, X, Y = None, None, None, None, None, None, None, None, None, None
    DIC = 59.7
    DIC(0) = "AEMQ"
    ^DIC
    if Y < 0:
        return
    print("\n\n\n\"Changing the IV Identifier will update the name of ALL Orderable Items\",!\n\"marked as an IV!\",!!")
    PSSIVID = $P($G(^PS(59.7, +Y, 31)), U, 2)
    DIE = 59.7
    DA = PSSSITE = +Y
    DR = 32
    ^DIE
    if PSSIVID == $P($G(^PS(59.7, PSSSITE, 31)), U, 2):
        return
    print("\n\"Updating Orderable Item names in OE/RR\"")
    PSSOI = 0
    while PSSOI:
        PSSOI = $O(^PS(50.7, "AIV", 1, PSSOI))
        if not PSSOI:
            continue
        if $D(^PS(50.7, PSSOI)):
            EN2^PSSHL1(PSSOI, "MUP")
        print("\".\"")
    return

def GTIVID():
    """
    Return IV Identifier. If being edited, wait until edit is done.
    """
    X = PX = $O(^PS(59.7, 0))
    if not X:
        return
    while L + ^PS(59.7, X, 31): $S($G(DILOCKTM) > 0 : DILOCKTM, 1 : 3)
        if $T:
            break
        H 2
    X = $P($G(^PS(59.7, X, 31)), U, 2)
    L - ^PS(59.7, PX, 31)
    return X