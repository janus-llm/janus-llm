def PSSNDSU():
    return

def QUE():
    ZTRTN = "EN^PSSNDSU"
    ZTDESC = "Medications Dosage Form NDS Master File Associations"
    ZTDTH = NOW()
    ZTIO = ""
    ZTLOAD()

def EN():
    XUMF = 1
    PSSFL = int(HEADER.split("**")[1].split("*")[0])
    if not PSSFL:
        return
    UPDATE(PSSFL)

def UPDATE(OFILE):
    SCANM(OFILE)
    SCANO(OFILE)

def SCANM(OFILE):
    FIELD = DID(OFILE, 90, "", "POINTER")
    MGLO = FIELD["POINTER"]
    MGLO = "^" + MGLO
    MFILE = int(MGLO.split("(")[1])
    ASSOC = ""
    while True:
        ASSOC = ORDERED_DICT_KEY(MGLO + '"""AC"",ASSOC)')
        if not ASSOC:
            break
        MIEN = 0
        while True:
            MIEN = ORDERED_DICT_KEY(MGLO + '"""AC"",ASSOC,MIEN)')
            if not MIEN:
                break
            OFILIEN = FIND1(OFILE, "", "O", ASSOC, "", "", "PSERR")
            if OFILIEN:
                UPDPTR(ASSOC, MIEN, "ADD", OFILE)

def SCANO(OFILE):
    OGLO = FILE(GLO(OFILE))
    MGLO = DID(OFILE, 90, "", "POINTER")["POINTER"]
    MGLO = "^" + MGLO
    MFILE = int(MGLO.split("(")[1])
    OFILIEN = 0
    while True:
        OFILIEN = ORDERED_DICT_KEY(OGLO + OFILIEN + ")")
        if not OFILIEN:
            break
        MPTR = OGLO + OFILIEN + "," + """MASTER"""
        if not MPTR:
            continue
        RSLT = FIND(OFILE, "", "@;.01", "A", OFILIEN)
        ONAME = RSLT["DILIST"]["ID"][1][.01]
        RSLT = FIND(MFILE, "", "@;.01", "A", MPTR)
        MNAME = RSLT["DILIST"]["ID"][1][.01]
        MFILESUB = str(MFILE) + "901"
        RSLT = FIND(MFILESUB, "," + MPTR + ",", ".01", "", ONAME)
        if not RSLT["DILIST"][2][1]:
            UPDPTR(ONAME, MPTR, "DEL", OFILE)

def UPDPTR(PSSVANAM, PSSMIEN, PSSACT, PSSFILE):
    PSSMGLO = DID(PSSFILE, 90, "", "POINTER")["POINTER"]
    PSSMGLO = "^" + PSSMGLO
    PSSMFILE = int(PSSMGLO.split("(")[1])
    if not (PSSMFILE == 50.60699):
        return
    PSSGLO = FILE(GLO(PSSFILE))
    PSSMSUB = str(PSSMFILE) + "901"
    PSSIEN = 0
    while True:
        PSSIEN = ORDERED_DICT_KEY(PSSGLO + '"""B"",PSSVANAM,PSSIEN)')
        if not PSSIEN:
            break
        if PSSACT == "ADD":
            if PSSGLO + PSSIEN + "," + """MASTER""" == PSSMIEN:
                continue
            PSSFDA = {"FIELD": {PSSFILE: {PSSIEN + ",90": int(PSSMIEN)}}}
            FILE(PSSFDA)
        if PSSACT == "DEL":
            if not PSSIEN:
                continue
            PSSFDA = {"FIELD": {PSSFILE: {PSSIEN + ",90": "@"}}}
            FILE(PSSFDA)

def FILE():
    return int(HEADER.split("*")[1])

PSSNDSU()