def PSSOUTSC():
    # BIR/RTR-Outpatient Schedule processor
    # 08/21/00
    # 1.0;PHARMACY DATA MANAGEMENT;**38**;9/30/97

    def EN(PSSJSCHZ):
        if PSSJSCHZ == "":
            return
        if PSSJSCHZ.find('"') != -1 or ord(PSSJSCHZ[0]) == 45 or PSSJSCHZ.isprintable() or len(PSSJSCHZ.split(" ")) > 3 or len(PSSJSCHZ) > 20 or len(PSSJSCHZ) < 1:
            PSSJSCHZ = None

    def EN1():
        # called from schedule field of Pharmacy Orderable Item File
        PSSTRI = 0
        PSSTRO = 0
        PSSTLP = ""
        for PSSTLP in range(len(^PSDRUG("ASP", DA))):
            if ^PSDRUG(PSSTLP, "I") != "" and ^("I") <= DT:
                continue
            if ^PSDRUG(PSSTLP, 2, 3) == "O":
                PSSTRO = 1
            if ^PSDRUG(PSSTLP, 2, 3) == "I" or ^PSDRUG(PSSTLP, 2, 3) == "U":
                PSSTRI = 1
        if PSSTRI:
            PASS()
        for PSSTLP in range(len(^PS(52.6, "AOI", DA))):
            if ^PS(52.6, PSSTLP, "I") != "" and ^("I") <= DT:
                continue
            PSSTRI = 1
        if PSSTRI:
            PASS()
        for PSSTLP in range(len(^PS(52.7, "AOI", DA))):
            if ^PS(52.7, PSSTLP, "I") != "" and ^("I") <= DT:
                continue
            PSSTRI = 1
        PASS() if PSSTRI else None
        if PSSTRO and not PSSTRI:
            OUT()

    def OUT():
        # Outpatient Input Transform and echo of Outpatient expansion
        SCH = X
        OUTZ()
        if SCHEX != "":
            print("Outpatient Expansion:")
            print(SCHEX)
            print(" ")

    def OUTZ():
        SQFLAG = 0
        SCLOOP = 0
        SCLP = 0
        SCLPS = ""
        SCLHOLD = ""
        SCIN = 0
        SODL = ""
        SST = 0
        SCHEX = ""
        if SCH == "":
            SCHEX = ""
            return
        SCLOOP = len(^PS(51.1, "B", SCH))
        while SCLOOP or SQFLAG:
            if ^PS(51.1, SCLOOP, 0) != "" and ^("0", 8) != "":
                SCHEX = ^("0", 8)
                SQFLAG = 1
        if ^PS(51, "A", SCH) != "" and ^("A", SCH) != "":
            SCHEX = ^("A", SCH)
        SCLOOP = 0
        for SCLP in range(len(SCH)):
            SCLPS = SCH[SCLP]
            if SCLPS == " ":
                SCLOOP += 1
        if SCLOOP == 0:
            SCHEX = SCH
            return
        SCLOOP += 1
        SCLHOLD = [None] * SCLOOP
        for SCIN in range(SCLOOP):
            SODL = SCH.split(" ")[SCIN]
            if SODL != "":
                SQFLAG = 0
                SST = len(^PS(51.1, "B", SODL))
                while SST or SQFLAG:
                    if ^PS(51.1, SST, 0) != "" and ^("0", 8) != "":
                        SCLHOLD[SCIN] = ^("0", 8)
                        SQFLAG = 1
                if ^PS(51, "A", SODL) != "" and ^("A", SODL) != "":
                    SCLHOLD[SCIN] = ^("A", SODL)
        SCHEX = ""
        SQFLAG = 0
        for SST in range(SCLOOP):
            SCHEX = SCHEX + (" " if SQFLAG else "") + SCLHOLD[SST]
            SQFLAG = 1

    EN(PSSJSCHZ)