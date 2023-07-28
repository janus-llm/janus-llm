# PSSCPRS1 ;BIR/ASJ-API for CPRS ;09/07/00
# 1.0;PHARMACY DATA MANAGEMENT;**38**;9/30/97
# Reference to $$CPRS^PSNAPIS supported by DBIA 2531

# PSDD - Dispense Drug, PSOI - Orderable Item, PSPK - Package
# PSDOS - Dosage, PSDUD - Dispense Units per Dosage
# RESULT(1) = Dispense Drug^Dosage^Orderable Item^Dispense Units per Dosage
# RESULT(2) = ERROR DESCRIPTION

if PSDUD > 0:
    ND()
else:
    if not PSSND1 or not PSSND3:
        RESULT[0] = -1
        RESULT[2] = "Problem in ND node!"
    else:
        X = DFSU(PSSND1, PSSND3)
        if X[4] == "":
            NNSI()
        elif X[0] != "":
            NNMI()

def ND():
    """
    I/P to O/P Transfer Rules - Numeric Dosages
    """

    # FR541
    if (not DRUG_I or DRUG_I >= DT) and (PSUSE.find("O") != -1):
        RESULT[0] = 1
        RESULT[1] = f"{PSDD}^{PSDOS}"
        RESULT[2] = "FR541"
        return

    # FR542
    PSCORR = PSNODE8[4]
    if PSCORR and (not PSCORR_I or PSCORR_I >= DT):
        PSNODE2 = DRUG[PSCORR][2]
        CP()
        for PDS in DRUG[PSCORR]["DOS1"]:
            PSDOS1 = DRUG[PSCORR]["DOS1"][PDS]
            PDOS = DRUG[PSCORR]["DOS"]
            PSSTR, PSUNT = PDOS[0], PDOS[1]
            if PSDOS and (PSDOS1[1] == PSDOS) and ("O" in PSNODE2[2]) and ("O" in PSDOS1[2]):
                if X[4] == PSDOSN[1] and X[0] == X1[0]:
                    RESULT[0] = 1
                    RESULT[1] = f"{PSCORR}^{PSDOS}"
                    RESULT[2] = "FR542"
                    return

    # FR543
    FLAG = 0
    for AA in DRUG["ASP"][PSOI]:
        if "DOS1" in DRUG[AA]:
            for PDS in DRUG[AA]["DOS1"]:
                BB = DRUG[AA]["DOS1"][PDS]
                PSNODE2 = DRUG[AA][2]
                if PSDOS and (BB[1] == PSDOS) and ("O" in PSNODE2[2]) and ("O" in BB[2]):
                    FLAG = 1
                    PSLI[AA] = ""

    if FLAG:
        for AA in PSLI:
            for PDS in DRUG[AA]["DOS1"]:
                POSDOS = DRUG[AA]["DOS1"][PDS]
                PSDPD = int(POSDOS)
                if not PSDUPD or (PSDPD < PSDUPD):
                    PSDUPD = PSDPD
        RESULT[0] = 1
        RESULT[1] = f"{AA}^{POSDOS[1]}"
        RESULT[2] = "FR543"
        FLAG = 0
        return

    # FR544
    PSCORR = PSNODE8[4]
    if PSCORR and (not PSCORR_I or PSCORR_I >= DT):
        CP()
        if X[4] == PSDOSN[1] and X[0] == X1[0]:
            RESULT[0] = 1
            RESULT[1] = PSDD
        return

    # FR545
    RESULT[0] = -1
    RESULT[2] = "All Numeric Dosage Rules failed!"
    return

def NNSI():
    """
    I/P to O/P Transfer Rules- NON-NUMERIC Single Ingredient
    """

    # FR551
    if (not DRUG_I or DRUG_I >= DT) and ("U" in PSUSE) and ("O" in PSUSE):
        RESULT[0] = 1
        RESULT[1] = f"{PSDD}^{PSDOS}^{PSOI}^{PSDUD}"
        return

    # FR552
    if "U" not in PSUSE and "O" not in PSUSE:
        PSCORR = PSNODE8[4]
        if PSCORR and (not PSCORR_I or PSCORR_I >= DT):
            CP()
            if PSSTR and PSUNT and (PSSTR == PSNDSTR) and (PSUNT == PSNDUN):
                if X[4] == PSDOSN[1] and X[0] == X1[0]:
                    RESULT[0] = 1
                    RESULT[1] = f"{PSCORR}^{PSDOS}^{PSOI}^{PSDUD}"
        return

    # FR553
    for AA in DRUG["ASP"][PSOI]:
        PSSTR = DRUG[AA]["DOS"][0]
        PSUNT = DRUG[AA]["DOS"][1]
        X = CPRS(PSSND1, PSSND3)
        PSNDSTR = X[2]
        PSNDUN = X[3]
        if PSSTR and PSUNT and (PSSTR == PSNDSTR) and (PSUNT == PSNDUN):
            RESULT[0] = 1
            RESULT[1] = f"{AA}^{PSDOS}^{PSOI}^{PSDUD}"
            return

    # FR554
    RESULT[0] = -1
    return

def NNMI():
    """
    I/P to O/P Transfer Rules- Multi-Ingredient
    """

    # FR561
    if (not DRUG_I or DRUG_I >= DT) and ("U" in PSUSE) and ("O" in PSUSE):
        RESULT[0] = 1
        RESULT[1] = f"{PSDD}^{PSDOS}^{PSOI}^{PSDUD}"
        return

    # FR562
    if "U" not in PSUSE and "O" not in PSUSE:
        PSCORR = PSNODE8[4]
        if PSCORR and (not PSCORR_I or PSCORR_I >= DT):
            CP()
            if X[4] == PSDOSN[1] and X[0] == X1[0]:
                RESULT[0] = 1
                RESULT[1] = f"{PSCORR}^{PSOD}^{PSSOP}^{PSDUD}"
        return

def CP():
    """
    Common code
    """

    PSND = DRUG[PSCORR]["ND"]
    X = CPRS(PSND[0], PSND[2])
    PSNDSTR = X[2]
    PSNDUN = X[3]
    PSDOSN = DRUG[PSDD]["DOS"]
    X1 = CPRS(PSSND1, PSSND3)