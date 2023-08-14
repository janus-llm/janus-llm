# BIR/TSS - API FOR VARIOUS DATA FROM PHARMACY PATIENT FILE; 5 Sep 03
# 1.0;PHARMACY DATA MANAGEMENT;**112**;9/30/97;Build 30

def STATUS(PSSFILE, PSSFIELD, LIST):
    # PSSFILE - FILE NUMBER (VALIDATED AGAINST "FILES" LINE-TAG BELOW)
    # PSSFIELD - FIELD NUMBER FROM FILE
    # LIST - NAME OF LOCAL ARRAY RETURNED
    # Returns the set of codes valid for the status field
    PSSDIY = ""
    if not PSSFILE or not PSSFIELD or not LIST:
        return
    PSSTEST = VALID(PSSFILE, PSSFIELD)
    if PSSTEST <= 0:
        PSSDIY = -1
        return
    FIELD(PSSFILE, PSSFIELD, "", "POINTER", LIST)

def VALID(PSTFILE, PSTFIELD):
    # TEST FOR VALID DATA INPUT FOR PSOFILE AND DIC
    PSVALID = -1
    for PSVLOOP in range(1, 100):
        PSVTEST = f"{FILES[PSVLOOP][0]};;{FILES[PSVLOOP][1]}"
        if not PSVTEST or PSVALID == 1:
            break
        if PSTFILE == PSVTEST.split(";;")[0]:
            if PSTFIELD == PSVTEST.split(";;")[1]:
                PSVALID = 1
    return PSVALID

# ACCESS FILE LIST
FILES = [
    ["55.06", "28"],
    ["55.01", "100"],
    ["55.05", "5"]
]

def CLINIC(PSSORD, PSSDFN, PSSMED):
    # PSSORD - ORDER NUMBER
    # PSSDFN - DFN NUMBER
    # PSSMED - MED TYPE: "U" FOR UNIT DOSE, "I" FOR IV
    PSSOUT = ""
    if not PSSORD or not PSSDFN or not PSSMED:
        return
    PSSIEN = f"{PSSORD},{PSSDFN}"
    TEMP = {}
    # DMS TEST CASES FOR UNIT DOSE: 73,739
    # TEST CASES FOR IV: 6,1
    if PSSMED == "U":
        GETS(PSSIEN, "130", "IE", "^TMP($J,\"TEMP\")")
        if TEMP["55.06"][PSSIEN][130]["I"]:
            PSSOUT = f"{TEMP['55.06'][PSSIEN][130]['I']}^{TEMP['55.06'][PSSIEN][130]['E']}"
    if PSSMED == "I":
        GETS(PSSIEN, "136", "IE", "^TMP($J,\"TEMP\")")
        if TEMP["55.01"][PSSIEN][136]["I"]:
            PSSOUT = f"{TEMP['55.01'][PSSIEN][136]['I']}^{TEMP['55.01'][PSSIEN][136]['E']}"
    del TEMP
    return PSSOUT