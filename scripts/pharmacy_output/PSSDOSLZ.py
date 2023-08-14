def PSSDOSLZ():
    # BIR/RTR-Dosage edit
    # 10/24/01
    # 1.0;PHARMACY DATA MANAGEMENT;**49**;9/30/97

    # Reference to ^PS(50.607 supported by DBIA 2221

    # x-ref on Dispense Unit per Dose to set Dose field
    PSSUNIT = ""
    PSSUNITV = ""
    PSSDOSEV = 0
    PSS2 = ""
    PSS1 = ""
    PSS3 = ""
    PSSU1 = ""
    PSSUNITA = ""
    PSSUNITB = ""
    PSSUSL = ""
    PSSUST = ""
    PSSU50 = ""
    PSSUSL2 = ""
    PSSUSL3 = ""
    PSSUSL4 = ""
    PSSUSL5 = ""
    PSSUZ = ""
    PSSUZ1 = ""
    PSSUZD = ""

    PSSDOSEV = int(X) * int(PSSDRUG[PSSIEN]["DOS"])
    PSSUNIT = PSS(50.607[PSSDRUG[PSSIEN]["DOS"][2]][0])
    PSSUSL = 0
    if "/" in PSSUNIT:
        PSSUST = PSJST(PSDRUG[PSSIEN]["ND"], PSDRUG[PSSIEN]["ND"][3])
        PSSUST = int(PSSUST[2])
        if PSSUST and PSSU50 and int(PSSUST) != int(PSSU50):
            PSSUSL = 1
        
        PSSUNITA = PSSUNIT.split("/")[0]
        PSSUNITB = PSSUNIT.split("/")[1]
        PSS1 = int(PSSUNITA)
        PSSU1 = int(PSSUNITB)
        
        if PSSUSL:
            PSSUSL2 = PSSU50 / PSSUST
            PSSUSL3 = PSSUSL2 * X
            PSSUSL4 = PSSUSL3 * (PSSU1 if PSSU1 else 1)
            PSSUSL5 = PSSUSL4 + PSSUNITB if not PSSU1 else PSSUSL4 + PSSUNITB[PSSU1:]

        PSSUNITV = (PSS1 * PSSDOSEV) + PSSUNITA + "/" + (PSSUSL5 if PSSUSL else X + PSSUNITB)
    else:
        PSSUNITV = PSSDOSEV + PSSUNIT
    
    if "/." in PSSUNITV:
        PSSUZD = PSSUNITV
        PSSUZ = PSSUZD.split("/.")[0]
        PSSUZ1 = PSSUZD.split("/.")[1]
        PSSUNITV = PSSUZ + "/0." + PSSUZ1
    
    X = ("0" + PSSUNITV) if PSSUNITV[0] == "." else PSSUNITV
    return X