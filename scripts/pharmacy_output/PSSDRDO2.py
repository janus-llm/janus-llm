def CLEFF(PSSVAPRD):
    # Retrieve and write Clinical Effects of Drug fields
    # input:  PSSVAPRD = IEN for VA Product file (#50.68)
    
    # Clinical Effects of Drug fields
    if not PSSVAPRD:
        return
    
    PSSNIEN = PSSVAPRD
    ^TMP($J,"PSSVAPR") = {}
    DATA^PSN50P68(PSSVAPRD, "", "PSSVAPR")  # using the PRE encapuslation API
    
    PSSCLEF = {}
    if PSSNIEN in ^TMP($J,"PSSVAPR"):
        PSSII = 0
        PSSIII = 0
        while PSSII != "":
            PSSPKG = ""
            PSSOMIT = ""
            PSSEXLMT = ""
            while PSSIII != "":
                if PSSIII == .01:
                    PSSPKG = ^TMP($J,"PSSVAPR",PSSNIEN,108,PSSII,PSSIII)
                if PSSIII == 1:
                    PSSOMIT = ^TMP($J,"PSSVAPR",PSSNIEN,108,PSSII,PSSIII)
                if PSSIII == 2:
                    PSSEXLMT = ^TMP($J,"PSSVAPR",PSSNIEN,108,PSSII,PSSIII)
            if PSSPKG != "":
                PSSCLEF[PSSPKG] = PSSOMIT + "^" + PSSEXLMT
    
    print("\nCLINICAL EFFECT DURATION: " + ("YES" if ^TMP($J,"PSSVAPR",PSSNIEN,108) else "NO"))
    
    # If package IO is defined only show it, otherwise show all packages
    if "IO" in PSSCLEF:
        PSSPKG = "IO"
        CLEFFS()
        CLEFFW(PSSPKG, PSSOMIT, PSSEXLMT)
        return
    
    PSSPKG = ""
    while PSSPKG != "":
        CLEFFS()
        CLEFFW(PSSPKG, PSSOMIT, PSSEXLMT)
    
def CLEFFS():
    PSSOMIT = ""
    PSSEXLMT = ""
    PSSOMIT = PSSCLEF[PSSPKG].split("^")[0]
    PSSEXLMT = PSSCLEF[PSSPKG].split("^")[1]
    
def CLEFFW(PSSPKG, PSSOMIT, PSSEXLMT):
    PSSPACK2 = ""
    PSSOMIT = ""
    PSSEXLMT = ""
    PSSOMIT = PSSCLEF[PSSPKG].split("^")[0]
    PSSEXLMT = PSSCLEF[PSSPKG].split("^")[1]
    
    PSSPACK2 = "INPATIENT" if PSSPKG == "I" else ("OUTPATIENT" if PSSPKG == "O" else ("BOTH INPATIENT AND OUTPATIENT" if PSSPKG == "IO" else ""))
    print("\n" + " " * 3 + PSSPACK2 + " DURATION LIMIT: " + (PSSEXLMT if PSSOMIT == 0 else ""))
    print(" " * 6 + "OMIT EXP/DC ORDER CHECK: " + ("YES" if PSSOMIT == 1 else ("NO" if PSSOMIT == 0 else "")))

CLEFF(PSSVAPRD)