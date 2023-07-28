# BIR/CMF-Exceptions for Dose call Continuation

# Called from PSSDSEXE, this routine takes the results from the call to First DataBank and creates displayable TMP
# globals for the calling applications. Typically, PSSDBASA indicates a CPRS call, and PSSDBASB indicates a pharmacy call

# PSSDBCAR ARRAY pieces, set mostly in PSSDSAPD are described in PSSDSEXC:


def TWEAK200():
    # loop through exception then error globals, ensure no duplicate generic messages
    PSSDXLP = ""
    while True:
        PSSDXLP = next(iter(^TMP($J, PSSDBASF, "OUT", "EXCEPTIONS", "DOSE", PSSDXLP)), None)
        if PSSDXLP is None:
            break
        PSSDXLP["MSG"] = ""
        PSSDXLP["RSN"] = ""
        PSSDXLP["TYP"] = ""
        PSSDXLP["FLG"] = ""
        PSSDXLP["MSG"] = ^TMP($J, PSSDBASF, "OUT", "EXCEPTIONS", "DOSE", PSSDXLP, 1)
        if PSSDXLP["MSG"] == "":
            continue
        PSSDXLP["TYP"] = "S" if "Maximum Single" in PSSDXLP["MSG"] else "D" if "Max Daily" in PSSDXLP["MSG"] else "B"
        PSSDXLP["RSN"] = ^TMP($J, PSSDBASF, "OUT", "EXCEPTIONS", "DOSE", PSSDXLP, 2)
        if PSSDXLP["RSN"] == "":
            TWEAK205(PSSDXLP)
        if PSSDXLP["FLG"] == 1:
            PSSREPL["Maximum Single Dose Check"] = "Dosing Checks"
            PSSREPL["Max Daily Dose Check"] = "Dosing Checks"
            PSSDEMSG = REPLACE(PSSDXLP["MSG"], PSSREPL)
            ^TMP($J, PSSDBASF, "OUT", "EXCEPTIONS", "DOSE", PSSDXLP, 1) = PSSDEMSG
            PSSDBCAR(PSSDXLP).split("^")[27] = 1


def TWEAK205(PSSDXLP):
    # look for errors matching the exception, remove if found, return flag to TWEAK200
    PSSDWLP = PSSDXLP
    PSSDWCNT = ""
    while True:
        PSSDWCNT = next(iter(^TMP($J, PSSDBASF, "OUT", "DOSE", "ERROR", PSSDWLP, PSSDWCNT)), None)
        if PSSDWCNT == "":
            break
        PSSDWLP["MSG"] = ^TMP($J, PSSDBASF, "OUT", "DOSE", "ERROR", PSSDWLP, PSSDWCNT, "MSG")
        if PSSDWLP["MSG"] == "":
            continue
        PSSDWLP["RSN"] = ^TMP($J, PSSDBASF, "OUT", "DOSE", "ERROR", PSSDWLP, PSSDWCNT, "TEXT")
        if PSSDWLP["RSN"] == "":
            PSSDWLP["MSG"] = ""
            PSSDWLP["RSN"] = ""
            PSSDWLP["TYP"] = ""
            PSSDWLP["TYP"] = "S" if "Maximum Single" in PSSDWLP["MSG"] else "D" if "Max Daily" in PSSDWLP["MSG"] else "B"
            if PSSDWLP["TYP"] != PSSDXLP["TYP"]:
                PSSDXLP["FLG"] = 1
            del ^TMP($J, PSSDBASF, "OUT", "DOSE", "ERROR", PSSDWLP, PSSDWCNT)