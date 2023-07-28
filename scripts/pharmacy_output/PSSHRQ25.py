def BUILDMSG(COUNT, HASH):
    PSSGXDFT = HASH[COUNT]["orderNumber"][14]
    PSSGXDU = HASH[COUNT]["orderNumber"][6]
    
    if not PSSGXDFT:
        PSSGXMSG = CNV(0)
        INTRO()
        PSSGX1 = PSSHXA["doseLow"]
        PSSGX2 = PSSHXA["doseHigh"]
        if PSSGX1.startswith("."):
            PSSGX1 = "0" + PSSGX1
        if PSSGX2.startswith("."):
            PSSGX2 = "0" + PSSGX2
        PSSGXMSG += f" {PSSGX1} {PSSHXA['doseLowUnit']}"
        if PSSGX1 == PSSGX2:
            PSSGXMSG += "."
        else:
            PSSGXMSG += f" to {PSSGX2} {PSSHXA['doseHighUnit']}."
        PSSGX3 = PSSHXA["maxDailyDose"]
        PSSGX8 = 0
        if PSSGX3 == " **unknown** " or not PSSGX3 or PSSHXA["maxDailyDoseUnit"] == " **unknown** ":
            PSSGX3 = "unavailable."
            PSSGX8 = 1
        PSSGX4 = CONRT()
        if PSSGX3.startswith("."):
            PSSGX3 = "0" + PSSGX3
        if PSSGX4:
            PSSGXMSG += " Maximum dose rate is "
        else:
            PSSGXMSG += " Maximum daily dose is "
        if PSSGX8:
            PSSGXMSG += PSSGX3
        else:
            PSSGXMSG += f"{PSSGX3} {PSSHXA['maxDailyDoseUnit']}."
    else:
        CNV(1)
        INTRO()
        PSSGX1 = PSSHXA["doseFormLow"]
        PSSGX2 = PSSHXA["doseFormHigh"]
        if PSSGX1.startswith("."):
            PSSGX1 = "0" + PSSGX1
        if PSSGX2.startswith("."):
            PSSGX2 = "0" + PSSGX2
        PSSGXMSG += f" {PSSGX1} {PSSHXA['doseFormLowUnit']}"
        if PSSGX1 == PSSGX2:
            PSSGXMSG += "."
        else:
            PSSGXMSG += f" to {PSSGX2} {PSSHXA['doseFormHighUnit']}."
        PSSGX3 = PSSHXA["maxDailyDoseForm"]
        PSSGX8 = 0
        if PSSGX3 == " **unknown** " or not PSSGX3 or PSSHXA["maxDailyDoseFormUnit"] == " **unknown** ":
            PSSGX3 = "unavailable."
            PSSGX8 = 1
        PSSGX4 = CONRT()
        if PSSGX3.startswith("."):
            PSSGX3 = "0" + PSSGX3
        if PSSGX4:
            PSSGXMSG += " Maximum dose rate is "
        else:
            PSSGXMSG += " Maximum daily dose is "
        if PSSGX8:
            PSSGXMSG += PSSGX3
        else:
            PSSGXMSG += f"{PSSGX3} {PSSHXA['maxDailyDoseFormUnit']}."
    return PSSGXMSG


def CASE(PSSLWR):
    return PSSLWR.upper()


def CONRT():
    PSSGX9 = HASH[COUNT]["orderNumber"][11]
    if PSSGX9 in ["CONTINUOUS EPIDURAL", "CONT INTRAARTER INF", "CONTINUOUS INFILTRAT", "CONT CAUDAL INFUSION",
                  "CONT INTRAOSSEOUS", "CONT INTRATHECAL INF", "CONTINUOUS INFUSION", "CONT NEBULIZATION",
                  "CONT SUBCUTAN INFUSI"]:
        return 1
    return 0


def INTRO():
    PSSGXMSG = f"General dosing range for {PSSHXA['drugName']}"
    if HASH[COUNT]["doseRouteDescription"]:
        PSSGXMSG += f" ({HASH[COUNT]['doseRouteDescription']})"
    PSSGXMSG += ":"
    return PSSGXMSG


def CNV(PSSHXTYP):
    PSSGXFL = 0
    PSSGXNUL = 0
    PSSGXNM = ""
    PSSGXOLD = ""
    PSSGXCV1 = 0
    PSSGXCV2 = 0
    
    if PSSGXDU:
        PSSGXIEN = PSSGXDU
        if PSSGXIEN:
            sunit(PSSUNARA, PSSGXIEN)
    
    if PSSHXTYP:
        DFT1()
    else:
        for PSSHXL in ["doseLowUnit", "doseHighUnit", "maxDailyDoseUnit"]:
            PSSHXA[PSSHXL] = HASH[COUNT][PSSHXL]
            PSSGX5 = PSSHXA[PSSHXL]
            if not PSSGX5:
                PSSHXA[PSSHXL] = " **unknown** "
                if PSSHXL.startswith("dose"):
                    PSSGXNUL = 1
            if PSSGXIEN:
                FDUNIT(PSSGX5)
    
    if PSSGXIEN:
        PSSGXNM = HASH[COUNT]["doseLow"]  # Assuming this is a typo and it should be "drugName"
        if PSSGXNM:
            PSSGXFL = 0
    
    if not PSSGXDU or not PSSGXFL or PSSGXNUL or not PSSGXIEN:
        return
    
    for PSSHXL in PSSHXMCH["MISMATCH"]:
        PSSUNARF = {}
        PSSHX9 = PSSHXA[PSSHXL]
        PSSHX9 = CASE(PSSHX9)
        PSSHX8 = LKUN(PSSHX9)
        if PSSHX8:
            SUNIT(PSSUNARF, PSSHX8)
        if PSSHX9 not in PSSHXFL:
            PSSGXFL = 0
        if PSSHX9 != " ":
            PSSHX9 = PSSHX9.split(" ")[0]
            if not PSSHX9:
                PSSGXFL = 0
            PSSHX8 = LKUN(PSSHX9)
            if PSSHX8:
                SUNIT(PSSUNARF, PSSHX8)
                PRS()
            else:
                PSSGXFL = 0
    
    if not PSSGXFL:
        return
    
    if PSSHXTYP:
        for PSSHXL in ["doseFormLowUnit", "doseFormHighUnit", "maxDailyDoseFormUnit"]:
            PSSHXA[PSSHXL] = PSSGXNM
            if PSSHXL in PSSHXMCH["MISMATCH"]:
                PSSHXOLD = f"doseForm{PSSHXL.replace('Unit', '')}"
                PSSHXA[PSSHXOLD] = PSSHXA[PSSHXOLD] * PSSHX4[PSSHXL]
                PSSHXA[PSSHXOLD] = FMTNUM(PSSHXA[PSSHXOLD], 1)
    else:
        for PSSHXL in ["doseLowUnit", "doseHighUnit", "maxDailyDoseUnit"]:
            PSSHXA[PSSHXL] = PSSGXNM
            if PSSHXL in PSSHXMCH["MISMATCH"]:
                PSSHXOLD = f"dose{PSSHXL.replace('Unit', '')}"
                PSSHXA[PSSHXOLD] = PSSHXA[PSSHXOLD] * PSSHX4[PSSHXL]
                PSSHXA[PSSHXOLD] = FMTNUM(PSSHXA[PSSHXOLD], 1)


def LKUN(PSSLUNV):
    PSSLNUNI = None
    if PSSLUNV in PSSUNARA["B"]:
        PSSLNUNI = PSSUNARA["B"][PSSLUNV]
    elif PSSLUNV in PSSUNARA["C"]:
        PSSLNUNI = PSSUNARA["C"][PSSLUNV]
    elif PSSLUNV in PSSUNARA["D"]:
        PSSLNUNI = PSSUNARA["D"][PSSLUNV]
    return PSSLNUNI


def SUNIT(PSSUNARG, PSSUNARR):
    PSSUNARN = CASE(PSSUNARR["name"])
    if PSSUNARN:
        PSSUNARG[PSSUNARN] = ""
    for PSSUNARL in PSSUNARR["synonyms"]:
        PSSUNARG[CASE(PSSUNARL)] = ""


def PRS():
    PSSPER1 = CASE(PSSHXA[PSSHXL])
    if " PER " in PSSPER1:
        PSSPER2 = PSSPER1.find(" PER ")
        PSSPER2 -= 5
        PSSHXNM[PSSHXL] = PSSHXA[PSSHXL][PSSPER2:]
        

def FNCV(PSSLUNFN):
    PSSHX2 = LKUN(PSSLUNFN)
    if PSSHX2:
        for PSSHX3 in PSSHX2["synonyms"]:
            if PSSHX3 in PSSUNARA:
                PSSHXCV1 = PSSHX2["conversions"][PSSHX3]
                PSSHXCV2 = PSSHX2["conversions"][PSSHX3]
                PSSHX4[PSSHXL] = PSSHXCV2
                return True
    return False


def FDUNIT(PSSKQ1):
    PSSKQ2 = CASE(PSSKQ1)
    if PSSKQ2 in PSSUNARA:
        PSSHXMCH["MATCH"][PSSHXL] = ""
        return
    if " " not in PSSKQ2:
        FDSET()
        return
    PSSKQ2 = PSSKQ2.split(" ")[0]
    if not PSSKQ2:
        FDSET()
        return
    if PSSKQ2 in PSSUNARA:
        PSSHXMCH["MATCH"][PSSHXL] = ""
        return
    FDSET()


def FDSET():
    PSSHXMCH["MISMATCH"][PSSHXL] = ""
    PSSGXFL = 1


def DFT1():
    for PSSHXL in ["doseFormLowUnit", "doseFormHighUnit", "maxDailyDoseFormUnit"]:
        PSSHXA[PSSHXL] = HASH[COUNT][PSSHXL]
        PSSGX5 = PSSHXA[PSSHXL]
        if not PSSGX5:
            PSSHXA[PSSHXL] = " **unknown** "
            if PSSHXL.startswith("dose"):
                PSSHXNUL = 1
        if PSSGXIEN:
            FDUNIT(PSSGX5)


def DFT3():
    for PSSHXL in ["doseFormLow", "doseFormHigh", "maxDailyDoseForm", "drugName"]:
        PSSHXA[PSSHXL] = HASH[COUNT][PSSHXL]
        if not PSSHXA[PSSHXL]:
            PSSHXA[PSSHXL] = " **unknown** "
            if PSSHXL.startswith("dose"):
                PSSHXNUL = 1