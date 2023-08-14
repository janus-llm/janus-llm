# REPORT OF REFORMATTED LOCAL POSSIBLE DOSES
# 1.0;PHARMACY DATA MANAGEMENT;**134**;9/30/97;Build 8

# LOOP THROUGH DRUG FILE FOR ALL LOCAL POSSIBLE DOSES
def PSSP134():
    PSSDRUG = 0
    while PSSDRUG:
        PSSLPDX = 0
        while PSSLPDX:
            PSSLPD2 = ""
            if PSSLPD2 == "":
                continue
            PSSNLPD = DOSE(PSSLPD2)
            PSSDRUGN = ""
            ^XTMP("PSSP134", PSSDRUGN, PSSDRUG, PSSLPDX) = PSSLPD2 + "^" + PSSNLPD
    REPORT()

# Reformatted Local Possible Doses
def DOSE(PSSDOSE):
    PSSCHAR = ""
    PSSXX = ""
    PSSDOSR = ""
    for PSSXX in range(len(PSSDOSE)):
        PSSCHAR = PSSDOSE[PSSXX]
        if PSSCHAR == "." and PSSDOSE[PSSXX + 1] and not PSSDOSR[-1].isdigit():
            PSSCHAR = "0" + PSSCHAR
        if PSSDOSR and PSSDOSR[-1].isdigit() and not PSSCHAR.isdigit() and PSSCHAR not in "() -./%,":
            PSSDOSR = PSSDOSR + " " + PSSCHAR
        if PSSDOSR and not PSSDOSR[-1].isdigit() and PSSCHAR.isdigit() and PSSCHAR not in "() -./%,":
            PSSDOSR = PSSDOSR + " " + PSSCHAR
        if PSSDOSR and PSSDOSR[-1].isdigit() and not PSSCHAR.isdigit():
            PSSDOSR = PSSDOSR + PSSCHAR
        if PSSDOSR and not PSSDOSR[-1].isdigit() and not PSSCHAR.isdigit():
            PSSDOSR = PSSDOSR + PSSCHAR
        PSSDOSR = PSSDOSR + PSSCHAR
    return PSSDOSR

# Report of Local Possible Doses before and after
def REPORT():
    PSSDT = ""
    PSSXDT = ""
    PSSI = 0
    PSSXX = 4
    PSSLINE = ""
    PSSSPC = ""
    for PSSX in range(50):
        PSSLINE += "-"
        PSSSPC += " "
    PSSDRUGN = ""
    while PSSDRUGN:
        PSSDRUG = 0
        while PSSDRUG:
            ^XTMP("PSSP134R", PSSXX) = ^PSDRUG(PSSDRUG, 0) + " (#" + PSSDRUG + ")"
            PSSXX += 1
            PSSLPDX = 0
            while PSSLPDX:
                PSSLPDD = ^XTMP("PSSP134", PSSDRUGN, PSSDRUG, PSSLPDX)
                PSSLPD = PSSLPDD[0]
                PSSNLPD = PSSLPDD[1]
                ^XTMP("PSSP134R", PSSXX) = PSSSPC[:10] + PSSLPD
                ^XTMP("PSSP134R", PSSXX + 1) = PSSSPC[:10] + PSSNLPD
                ^XTMP("PSSP134R", PSSXX + 2) = ""
                PSSXX += 3
    ^XMD()

PSSP134()