# PSSHRVAL ;WOIFO/Alex Vasquez,Timothy Sabat,Steve Gordon - Data Validation routine for drug checks ;01/15/07
# 1.0;PHARMACY DATA MANAGEMENT;**136,160,178**;9/30/97;Build 14

# Business rules:
# 1. If a prospective" node does not have a GCNSEQNO, it will be KILLED
# 2. If a "profile" node does not have a GCNSEQNO, it will be KILLED
# 3. If no prospective nodes exist, DRUGDRUG, THERAPY, and DOSE will be killed off
# 4. Only checks will be performed for those check nodes that still exist (e.g. DRUGDRUG, THERAPY, and DOSE)
# 5. If any of the demographics are out of range (age<=0, BSA<0 (or null) or Weight<0 or null) dose node will be killed.

def DRIVER(PSSBASE):
    """
    @DRIVER
    @DESC The driver for the validation of drug checks.
    @PSSBASE The base
    """
    PSSHASH = {}
    PSSHASH["Base"] = PSSBASE
    PSSHASH["ReasonCode"] = "" # for version 0.5 version not yet defined.

    BUILD(PSSHASH)

    WRITE(PSSHASH)
    CHKNODES(PSSHASH)
    return CONTINUE(PSSHASH)


def CHKNODES(PSSHASH):
    """
    @DESC Determines which nodes should be killed off or kept
    """
    ORDER = ""
    if not [x for x in range(len(PSSHASH["Exception"]["PROSPECTIVE"]["DOSE"]))]:
        if "PROFILEVPROFILE" in PSSHASH["IN"] and [x for x in range(len(PSSHASH["IN"]["PROFILE"]))]:
            return
        KILLALL(PSSHASH["Base"])
    if "DoseValue" in PSSHASH and "DEMOAGE" in PSSHASH["DoseValue"]:
        KILLCHEK("DOSE", PSSHASH["Base"])


def CONTINUE(PSSHASH):
    """
    @DESC Determines whether or not to proceed with checks.
    @RETURNS 1 if you may continue, 0 if not.
    """
    PSS = {"AnyChecksLeft": 0}
    if "DRUGDRUG" in PSSHASH["IN"]:
        PSS["AnyChecksLeft"] = 1
    if "THERAPY" in PSSHASH["IN"]:
        PSS["AnyChecksLeft"] = 1
    if "DOSE" in PSSHASH["IN"]:
        PSS["AnyChecksLeft"] = 1
    if "PING" in PSSHASH["IN"]:
        PSS["AnyChecksLeft"] = 1
    return PSS["AnyChecksLeft"]


def BUILD(PSSHASH):
    """
    @DESC Builds the internal hash used to parse for errors.
    @PSSHASH The internal variables.
    """
    CHKINEXP(PSSHASH)
    DRUGPROS(PSSHASH)
    DRUGPROF(PSSHASH)


def CHKINEXP(PSSHASH):
    """
    INPUT PSSHASH array
    PSSHASH["Exception"][TYPE]["DOSE"][PSS["PharmOrderNum"]][COUNTER]
    PSSHASH["Exception"][TYPE][PSS["PharmOrderNum"]][COUNTER]
    """
    if "EXCEPTIONS" in PSSHASH["IN"] and "OI" in PSSHASH["IN"]["EXCEPTIONS"]:
        OIEXP(PSSHASH)
    if "EXCEPTIONS" in PSSHASH["IN"] and "DOSE" in PSSHASH["IN"]["EXCEPTIONS"]:
        DOSINEXP(PSSHASH)


def DRUGPROS(PSSHASH):
    """
    @DESC Loops on the prospective drugs
    @PSSHASH The internal variables.
    """
    PSS = {"ProspectiveOrProfile": "PROSPECTIVE", "PharmOrderNum": ""}
    while True:
        PSS["PharmOrderNum"] = next(iter(PSSHASH["IN"]["PROSPECTIVE"]), None)
        if PSS["PharmOrderNum"] is None:
            break
        PSS["DrugValue"] = PSSHASH["IN"]["PROSPECTIVE"][PSS["PharmOrderNum"]]
        CHECKGCN(PSS, PSSHASH)
        CHECKDOS(PSS, PSSHASH)


def DEMOGRAF(PSS, PSSHASH, PSDRUG):
    """
    @DESC Validates the demographic info
    @PSSHASH The hash the demographic info is stored in
    """
    AGE = float(PSSHASH["IN"]["DOSE"]["AGE"])
    WEIGHT = float(PSSHASH["IN"]["DOSE"]["WT"])
    BSA = float(PSSHASH["IN"]["DOSE"]["BSA"])
    MESSAGE = DEMOCHK(AGE, BSA, WEIGHT, PSDRUG, PSSDSWHE)
    if MESSAGE:
        PSSNOAGE = 1
        if AGE <= 0:
            SETDSEXP(PSS, PSSHASH, MESSAGE, 0, 1)
            PSSDBCAR()
    return PSSNOAGE


def PSSDBCAR():
    """
    set global array for setting dose output globals ; cmf RTC #159140, #163341
    """
    if "PSSDBCAR" not in globals():
        return
    if "PharmOrderNum" not in PSS:
        return
    PSSDBCAR[PSS["PharmOrderNum"]] = (PSSDBCAR[PSS["PharmOrderNum"]][0:27] + "1")


def CHECKDOS(PSS, PSSHASH):
    """
    @DESC Check if the dose exists.
    @PSS The temp hash
    @PSSHASH The internal hash
    """
    if "DOSE" not in PSSHASH["IN"] or PSS["PharmOrderNum"] not in PSSHASH["IN"]["DOSE"]:
        return
    if PSS["ProspectiveOrProfile"] == "PROSPECTIVE" and PSS["PharmOrderNum"] not in PSSHASH["IN"]["PROSPECTIVE"]:
        return
    PSS["DoseValue"] = PSSHASH["IN"]["DOSE"][PSS["PharmOrderNum"]]
    PSS["Package"] = ""
    PSS["ReasonSource"] = GETUCI()
    DOSEVALUE = PSS["DoseValue"]
    DRUGNM = DOSEVALUE[3]
    DOSE = DOSEVALUE[4]
    DOSEUNIT = DOSEVALUE[5]
    DOSERATE = DOSEVALUE[6]
    FREQ = DOSEVALUE[7]
    DURATION = DOSEVALUE[8]
    DURRATE = DOSEVALUE[9]
    ROUTE = DOSEVALUE[10]
    DOSETYPE = DOSEVALUE[11]
    PSSNOAGE = DEMOGRAF(PSS, PSSHASH, DRUGNM)
    if DOSETYPE != "":
        MESSAGE = CHKDSTYP(DOSETYPE, DRUGNM)
        if MESSAGE:
            SETDSEXP(PSS, PSSHASH, MESSAGE, 12, 2)
    MESSAGE = CHKDOSE(DOSE, DRUGNM)
    if MESSAGE:
        SETDSEXP(PSS, PSSHASH, MESSAGE, 5)
    MESSAGE = CHKUNIT(DOSEUNIT, DRUGNM)
    if MESSAGE:
        SETDSEXP(PSS, PSSHASH, MESSAGE, 6)
    MESSAGE = CHKRATE(DOSERATE, "DOSE", DRUGNM)
    if MESSAGE:
        SETDSEXP(PSS, PSSHASH, MESSAGE, 7)
    MESSAGE = CHKDRATN(DURATION, DRUGNM)
    if MESSAGE:
        SETDSEXP(PSS, PSSHASH, MESSAGE, 9)
    MESSAGE = CHKRATE(DURRATE, "DURATION", DRUGNM, DURATION)
    if MESSAGE:
        SETDSEXP(PSS, PSSHASH, MESSAGE, 10)
    MESSAGE = MEDRTE(ROUTE, DRUGNM)
    if MESSAGE:
        SETDSEXP(PSS, PSSHASH, MESSAGE, 11, 2)


def SETDSEXP(PSS, PSSHASH, MESSAGE, DOSPIECE=None, PSSDBIN=None):
    """
    SET DOSE EXCEPTION
    PSS - ARRAY OF MED PROFILE INFORMATION (BY REF)
    PSSHASH - HOLDS DATA EXCEPTION (BY REF)
    MESSAGE - REASON AND ERROR REASON
    DOSEPIECE - THE OFFENDING PIECE OF DATA FROM DOSING INFORMATON - NOT SENT IF FROM DEMOGRAF CALL.
    """
    PSS["Counter"] = NEXTDOS(PSS, PSSHASH)
    PSS["ReasonCode"] = PSSHASH["ReasonCode"]
    PSS["Message"] = MESSAGE.split('_')[0]
    PSS["ReasonText"] = MESSAGE.split('_')[1]
    PSS["CprsOrderNumber"] = ""
    PSSHASH["Exception"][PSS["ProspectiveOrProfile"]]["DOSE"][PSS["PharmOrderNum"]][PSS["Counter"]] = DOSPIECE(PSS)
    if DOSPIECE:
        PSSHASH["DoseValue"][DOSPIECE] = ""
    KILLNODE(PSSHASH["Base"], "DOSE", PSS["PharmOrderNum"])
    KILLNODE(PSSHASH["Base"], "PROSPECTIVE", PSS["PharmOrderNum"])
    PSSDBCAR()
    if PSSDBIN == 1:
        PSSDBCAR(19)
    if PSSDBIN == 2:
        PSSDBCAR(23)
    if PSSDBIN == 3:
        PSSDBCAR(25)
    if PSSDBIN == 4:
        PSSDBCAR(26)


def DOSINEXP(PSSHASH):
    for ORDERNUM in PSSHASH["IN"]["EXCEPTIONS"]["DOSE"]:
        TMPNODE = PSSHASH["IN"]["EXCEPTIONS"]["DOSE"][ORDERNUM]
        ERRNUM = TMPNODE[0]  # ERROR NUMBER
        DRUGNM = TMPNODE[1]
        MESSAGE = DOSEMSG(DRUGNM)
        REASON = INRSON(ERRNUM)
        PSS = {"PharmOrderNum": ORDERNUM, "ProspectiveOrProfile": "PROSPECTIVE", "Package": "", "DoseValue": "", "ReasonSource": GETUCI()}
        SETDSEXP(PSS, PSSHASH, MESSAGE)
        HDOSE(ORDERNUM)
        KILLNODE(PSSHASH["Base"], PSS["ProspectiveOrProfile"], ORDERNUM)


def OIEXP(PSSHASH):
    for ORDITEM in PSSHASH["IN"]["EXCEPTIONS"]["OI"]:
        TMPNODE = PSSHASH["IN"]["EXCEPTIONS"]["OI"][ORDITEM]
        ERRNUM = TMPNODE[0]  # ERROR NUMBER
        ORDERNUM = TMPNODE[1]
        MESSAGE = OIMSG(ORDITEM, ORDERNUM)
        REASON = ""
        if PSSHASH["Base"][:2] == "PS":
            REASON = INRSON(ERRNUM, ORDERNUM)
        PSS = {"PharmOrderNum": ORDERNUM, "ProspectiveOrProfile": "PROFILE", "Package": "", "DoseValue": "", "ReasonSource": GETUCI()}
        PSS["Counter"] = NEXTGCN(PSS, PSSHASH)
        PSS["I"] = MESSAGE
        PSS["I"][6] = REASON
        SETEXCP(PSS, PSSHASH)
        HDOSE(ORDERNUM)
        KILLNODE(PSSHASH["Base"], PSS["ProspectiveOrProfile"], ORDERNUM)


def NEXTDOS(PSS, PSSHASH):
    """
    @DESC Gets the next dose
    @PSS The temp hash
    @PSSHASH The internal hash
    """
    return max(PSSHASH["Exception"][PSS["ProspectiveOrProfile"]]["DOSE"][PSS["PharmOrderNum"]]) + 1


def NEXTGCN(PSS, PSSHASH):
    """
    @DESC Gets the next Gcn
    @PSS The temp hash
    @PSSHASH The internal hash
    """
    return max(PSSHASH["Exception"][PSS["ProspectiveOrProfile"]][PSS["PharmOrderNum"]]) + 1


def DOSPIECE(PSS):
    """
    @DESC Appends all pre-defined pieces to a temp var
    @PSS The temp hash
    @RETURNS The appended temp var.
    """
    I = PSS["DoseValue"][0] + "^"  # Gcn
    I += PSS["DoseValue"][1] + "^"  # Vuid
    I += PSS["DoseValue"][2] + "^"  # Ien
    I += PSS["DoseValue"][3] + "^"  # DrugName
    I += PSS["CprsOrderNumber"] + "^"  # CprsOrderNumber
    I += PSS["Package"] + "^"  # Package
    I += PSS["Message"] + "^"
    I += PSS["ReasonCode"] + "^"
    I += PSS["ReasonSource"] + "^"
    I += PSS["ReasonText"]
    return I


def CHECKGCN(PSS, PSSHASH):
    """
    @DESC Checks the GCN for a Drug
    @PSS A temp array
    @PSSHASH The input array
    @ASSERT PSS["DrugValue"] exists.
    """
    if not PSS["DrugValue"][0]:
        DRUGIEN = PSS["DrugValue"][2]
        DRUGNM = PSS["DrugValue"][3]
        BADGCN = -1 if not PSS["DrugValue"][0].isdigit() else 0
        MESSAGE = GCNREASN(DRUGIEN, DRUGNM, PSS["PharmOrderNum"], BADGCN)
        if MESSAGE:
            REASON = MESSAGE.split('_')[1:]
            MESSAGE = MESSAGE.split('_')[0]
        PSS["Counter"] = NEXTGCN(PSS, PSSHASH)
        PSS["I"] = PSS["DrugValue"][0] + "^"  # Gcn
        PSS["I"] += PSS["DrugValue"][1] + "^"  # Vuid
        PSS["I"] += PSS["DrugValue"][2] + "^"  # Ien
        PSS["I"] += PSS["DrugValue"][3] + "^"  # DrugName
        PSS["I"] += PSS["DrugValue"][4] + "^"  # CprsOrderNumber
        PSS["I"] += PSS["DrugValue"][5] + "^"  # Package
        PSS["I"] += MESSAGE + "^"
        PSS["I"] += PSSHASH["ReasonCode"] + "^"
        PSS["I"] += GETUCI() + "^"
        PSS["I"] += REASON
        SETEXCP(PSS, PSSHASH)
        HDOSE(PSS["PharmOrderNum"])
        KILLNODE(PSSHASH["Base"], PSS["ProspectiveOrProfile"], PSS["PharmOrderNum"])


def SETEXCP(PSS, PSSHASH):
    PSSHASH["Exception"][PSS["ProspectiveOrProfile"]][PSS["PharmOrderNum"]][PSS["Counter"]] = PSS["I"]


def DRUGPROF(PSSHASH):
    """
    @DESC Checks the profile drugs.
    @PSSHASH The internal hash
    """
    PSS = {"ProspectiveOrProfile": "PROFILE", "PharmOrderNum": ""}
    while True:
        PSS["PharmOrderNum"] = next(iter(PSSHASH["IN"]["PROFILE"]), None)
        if PSS["PharmOrderNum"] is None:
            break
        PSS["DrugValue"] = PSSHASH["IN"]["PROFILE"][PSS["PharmOrderNum"]]
        CHECKGCN(PSS, PSSHASH)


def HDOSE(PSSDLDOS):
    """
    If it's a Dose Call
    """
    if "DOSE" not in PSSHASH["IN"] or PSSDLDOS not in PSSHASH["IN"]["DOSE"]:
        return
    KILLNODE(PSSHASH["Base"], "DOSE", PSSDLDOS)
    PSSDBCAR()


PSSHASH = {}
PSSHASH["Exception"] = {"PROSPECTIVE": {"DOSE": {}, "PHARMORDERNUM": {}}, "PROFILE": {}}
PSSHASH["IN"] = {}

DRIVER(PSSBASE)