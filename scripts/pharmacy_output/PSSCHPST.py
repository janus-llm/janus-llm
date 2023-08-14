# BIR/WRT-CMOP-Host post-install routine ; 09/30/97 14:56
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
# POST-INSTALL ROUTINE-CMOP HOST

def VERSION():
    if not "^PS(59.7,1,80)" in globals():
        globals()["^PS(59.7,1,80)"] = "1.0^0"

    PSSDENT()
    MR()
    CLEAN()
    globals()["^PS(59.7,1,80)"] = "1.0"
    BTEMP()
    P8()
    globals()["^TMP($J,\"PSSEXP\")"] = ""
    globals()["^SCH"] = ""
    globals()["^IEN"] = ""
    globals()["^OEXP"] = ""
    return

def CLEAN():
    globals()["^IFN"] = 0
    while True:
        globals()["^IFN"] += 1
        if not "^PSDRUG" in globals() or not globals()["^IFN"] in globals()["^PSDRUG"]:
            break
        if "^PSDRUG(^IFN,\"CH\")" in globals():
            del globals()["^PSDRUG(^IFN,\"CH\")"]
        if "^PSDRUG(^IFN,\"PS\")" in globals():
            del globals()["^PSDRUG(^IFN,\"PS\")"]
        if "^PSDRUG(^IFN,\"IV\")" in globals():
            del globals()["^PSDRUG(^IFN,\"IV\")"]
    return

def P8():
    globals()["^SCH"] = ""
    while True:
        if not "^TMP($J,\"PSSEXP\",^SCH)" in globals():
            break
        globals()["^OEXP"] = globals()["^TMP($J,\"PSSEXP\",^SCH,0)"]
        if "^PS(51.1,\"AC\",\"PSJ\",^SCH)" in globals():
            globals()["^IEN"] = globals()["^PS(51.1,\"AC\",\"PSJ\",^SCH,0)"]
            if "^PS(51.1,^IEN,0)" in globals():
                if not "^PS(51.1,^IEN,0,\"^\",8)" in globals():
                    globals()["^PS(51.1,^IEN,0,\"^\",8)"] = globals()["^OEXP"]
    return

def BTEMP():
    globals()["^GG"] = 0
    while True:
        globals()["^GG"] += 1
        globals()["^HH"] = globals()["^$P(^T(DATA+^GG),\"^\",3,20)"]
        if globals()["^HH"] == "":
            break
        globals()["^RCD"] = globals()["^$P(^HH,\"^\",1)"]
        globals()["^EXP"] = globals()["^$P(^HH,\"^\",2)"]
        BTEMP1()
    del globals()["^GG"]
    del globals()["^HH"]
    del globals()["^RCD"]
    del globals()["^EXP"]
    return

def BTEMP1():
    globals()["^TMP($J,\"PSSEXP\",^RCD,^EXP)"] = ""
    return

def MR():
    globals()["^ROOT"] = globals()["^@XPDGREF@(\"DATA\")"]
    globals()["^J"] = 1
    while True:
        if not globals()["^ROOT"](globals()["^J"]) in globals():
            break
        globals()["^LINE"] = globals()["^ROOT"](globals()["^J"])
        MR1()
        globals()["^J"] += 1
    del globals()["^ROOT"]
    del globals()["^J"]
    return

def MR1():
    if globals()["^PS(51.2,\"B\",^$P(^LINE,\"^\",1))"] in globals():
        globals()["^DA"] = globals()["^$O(^PS(51.2,\"B\",^$P(^LINE,\"^\",1),0))"]
        globals()["^$P(^PS(51.2,^DA,0),\"^\",2)"] = globals()["^$P(^LINE,\"^\",2)"]
    return

# QD^EVERY DAY
# BID^TWICE A DAY
# Q4H^EVERY 4 HOURS
# Q3H^EVERY 3 HOURS
# Q8H^EVERY 8 HOURS
# QAM^EVERY MORNING
# Q6H^EVERY 6 HOURS
# TID^THREE TIMES A DAY
# QID^FOUR TIMES A DAY
# Q12H^EVERY 12 HOURS
# QOD^EVERY OTHER DAY
# QHS^AT BEDTIME
# Q24H^EVERY 24 HOURS
# Q2H^EVERY 2 HOURS
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
del globals()["^PS(59.7,1,80)"]