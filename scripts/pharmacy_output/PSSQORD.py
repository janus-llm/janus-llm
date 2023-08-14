def PSSQORD(PSS1, PSS2):
    PSSNW = None
    PSSNEWIT = None
    PSSDT = None
    PSSLA = None
    PSSLS = None
    PSSOFLAG = None
    PSSDR = None

    if not PSS1 and not PSS2:
        return -1

    if PSS2:
        PSSNEWIT = int((^PSDRUG(PSS2, 2)).split("^")[0])
        return AC()

    if not (^PS(50.7, PSS1, 0)):
        return -1

    if not int((^PS(50.7, PSS1, 0)).split("^", 3)[2]):
        PSSNEWIT = PSS1
        return AC()

    PSSNW = 0
    PSSOFLAG = 0

    while (PSSLS := next(iter(^XTMP("PSSCONS", PSS1, PSSLS)), 0)) and not PSSOFLAG:
        if not PSSNW:
            PSSNW = int(PSSLS.split("^")[0])
            continue
        if PSSNW and PSSNW != int(PSSLS.split("^")[0]):
            PSSOFLAG = 1

    if PSSOFLAG:
        return -1

    while (PSSLA := next(iter(^XTMP("PSSCONA", PSS1, PSSLA)), 0)) and not PSSOFLAG:
        if not PSSNW:
            PSSNW = int(PSSLA.split("^")[0])
            continue
        if PSSNW and PSSNW != int(PSSLA.split("^")[0]):
            PSSOFLAG = 1

    if PSSOFLAG:
        return -1

    if not PSSNW:
        return -1

    PSSNEWIT = PSSNW
    return AC()

def AC():
    if not PSSNEWIT:
        return -1

    if not (^PS(50.7, PSSNEWIT, 0)):
        return -1

    PSSDT = int((^PS(50.7, PSSNEWIT, 0)).split("^")[3])

    if PSSDT:
        return f"{PSSNEWIT}^0^{PSSDT}"
    
    return f"{PSSNEWIT}^1"