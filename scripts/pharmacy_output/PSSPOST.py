# PSSPOST ;BIR/WRT-Post-install routine ; 04/07/98 10:19
# ;;1.0;PHARMACY DATA MANAGEMENT;**10**;9/30/97
# ; POST-INSTALL ROUTINE

def VERSION():
    if not '^PS(59.7,1,80)' in globals():
        globals()['^PS(59.7,1,80)'] = "1.0^0"
    PSSDENT()
    MR()
    LABM()
    CLEAN()
    globals()['^PS(59.7,1,80)'] = "1.0"
    BTEMP()
    P8()
    globals()['^TMP($J,"PSSEXP")'] = {}
    globals()['SCH'] = None
    globals()['IEN'] = None
    globals()['OEXP'] = None

    if not '^PS(59.7,1,31)' in globals():
        globals()['^PS(59.7,1,31)'] = "^IV"
    if '^PS(59.7,1,31)' in globals() and not globals()['^PS(59.7,1,31)'].split('^')[1]:
        globals()['^PS(59.7,1,31)'] = "^IV"

    X = "PSSJXR"
    Y = "55"
    DMAX = "5000"
    EN^DIKZ(X, Y, DMAX)

    X = "PSSVX6"
    Y = "52.6"
    DMAX = "5000"
    EN^DIKZ(X, Y, DMAX)

def P8():
    SCH = ""
    while SCH != "":
        OEXP = min(^TMP($J,"PSSEXP",SCH))
        if "^PS(51.1,"AC","PSJ",SCH) in globals():
            IEN = min(^PS(51.1,"AC","PSJ",SCH))
            if not $P(^PS(51.1,IEN,0),"^",8):
                $P(^PS(51.1,IEN,0),"^",8) = OEXP

def BTEMP():
    GG = 0
    while True:
        GG += 1
        HH = ^T(DATA+GG)
        if not HH:
            break
        RCD = $P(HH,"^",1)
        EXP = $P(HH,"^",2)
        BTEMP1(RCD, EXP)

def BTEMP1(RCD, EXP):
    globals()['^TMP($J,"PSSEXP")'][RCD] = EXP

def CLA():
    globals()['^PSDRUG("VAC")'] = {}
    DIK = "^PSDRUG("
    DIK(1) = "25"
    ENALL^DIK()

def MR():
    ROOT = $NA(@XPDGREF@("DATA"))
    J = 0
    while True:
        J += 1
        if not @ROOT@(J):
            break
        LINE = @ROOT@(J)
        MR1(LINE)

def MR1(LINE):
    if "^PS(51.2,"B",$P(LINE,"^",1))" in globals():
        DA = min(^PS(51.2,"B",$P(LINE,"^",1)))
        $P(^PS(51.2,DA,0),"^",2) = $P(LINE,"^",2)

def CLEAN():
    IFN = 0
    while True:
        IFN += 1
        if not ^PSDRUG(IFN):
            break
        if $D(^PSDRUG(IFN,"CH")):
            del ^PSDRUG(IFN,"CH")
        if $D(^PSDRUG(IFN,"PS")):
            del ^PSDRUG(IFN,"PS")
        if $D(^PSDRUG(IFN,"IV")):
            del ^PSDRUG(IFN,"IV")

def LABM():
    IEN = 0
    while True:
        IEN += 1
        if not ^PSDRUG(IEN):
            break
        LABM1(IEN)
        LABM2(IEN)
        LABM3(IEN)

def LABM1(IEN):
    if $P(^PSDRUG(IEN,"CLOZ1"),"^") == "LAB MONITOR":
        ^PSDRUG(IEN,"CLOZ1") = "^1"

def LABM2(IEN):
    if $D(^PSDRUG(IEN,"CLOZ1")) and $P(^PSDRUG(IEN,"CLOZ1"),"^") == "" and $D(^PSDRUG(IEN,"CLOZ")):
        $P(^PSDRUG(IEN,"CLOZ1"),"^",2) = 1

def LABM3(IEN):
    if not $D(^PSDRUG(IEN,"CLOZ1")) and $D(^PSDRUG(IEN,"CLOZ")):
        $P(^PSDRUG(IEN,"CLOZ1"),"^",2) = 1

DATA = [
    "QD^EVERY DAY",
    "BID^TWICE A DAY",
    "Q4H^EVERY 4 HOURS",
    "Q3H^EVERY 3 HOURS",
    "Q8H^EVERY 8 HOURS",
    "QAM^EVERY MORNING",
    "Q6H^EVERY 6 HOURS",
    "TID^THREE TIMES A DAY",
    "QID^FOUR TIMES A DAY",
    "Q12H^EVERY 12 HOURS",
    "QOD^EVERY OTHER DAY",
    "QHS^AT BEDTIME",
    "Q24H^EVERY 24 HOURS",
    "Q2H^EVERY 2 HOURS"
]

VERSION()