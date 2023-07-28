def PSSPOI():
    # BIR/RLW-CREATE PHARMACY ORDERABLE ITEMS ; 09/01/98 7:10
    # 1.0;PHARMACY DATA MANAGEMENT;**15**;9/30/97

    def EN():
        # variable prefixes: ADD=iv additive file SOL=iv solution file
        # PD=primary drug file DD=dispense drug file
        # NDF=national drug file DF=NDF dosage form
        # SPD=pharmacy orderable item file SYN=synonym

        def LIVE():
            # populate PHARMACY ORDERABLE ITEM file, tie dispense drug to it
            # loop thru ^TMP global to build 50.7
            J, ADDIEN, ADDNAME, DDIEN, DDNAME, PDIEN, PDNAME, PDNAMEDF, NDF, NDFVA, DF, DFNAME, SPDNAME, X, PSMATCH, SOLIEN, SOLNAME, SPD, SPDFN, SYNIEN, SYNONYM = (
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
            )
            PDNAMEDF = ""
            while True:
                PDNAMEDF = next(iter(TMP["PSSD"]), None)
                if PDNAMEDF is None:
                    break
                DFNAME = PDNAMEDF.split("~")[1]
                PDNAME = PDNAMEDF.split("~")[0]
                if DFNAME == "":
                    continue
                DF = next(iter(PS[50.606]["B"]), None)
                I = len(PDNAME)
                while I >= 1:
                    if PDNAME[I-1] != " ":
                        break
                    I = I - 1
                SPDNAME = PDNAME[:I]
                SPD = None
                if SPDNAME not in PS[50.7]["ADF"][DF]:
                    SPD = {
                        ".01": SPDNAME,
                        ".02": DF
                    }
                    SPDIEN = ADD(50.7, SPD)
                else:
                    SPDIEN = next(iter(PS[50.7]["ADF"][DF][SPDNAME]))
                SYNIEN = 0
                while True:
                    PDIEN = next(iter(PS[50.3]["B"][PDNAME]), None)
                    if PDIEN is None:
                        break
                    Y = next(iter(PS[50.3][PDIEN][1]["B"]["U"]), None)
                    if Y:
                        Y = PS[50.3][PDIEN][1][Y]
                        PS[50.7][SPDIEN][X:8] = Y[X:8]
                    SYNIEN = next(iter(PS[50.3][PDIEN][2]), None)
                    if not SYNIEN:
                        PS[50.7][SPDIEN][2][1] = PS[50.3][PDIEN][2][SYNIEN]
                        J = 1
                        PS[50.7][SPDIEN][2]["B"][PS[50.3][PDIEN][2][SYNIEN]] = J
                    while True:
                        SYNIEN = next(iter(PS[50.3][PDIEN][2]), None)
                        if not SYNIEN:
                            break
                        J = J + 1
                        PS[50.7][SPDIEN][2][J] = PS[50.3][PDIEN][2][SYNIEN]
                        PS[50.7][SPDIEN][2]["B"][PS[50.3][PDIEN][2][SYNIEN]] = J
                        PS[50.7][SPDIEN][2][3:4] = [J, J]
                while True:
                    DDNAME = next(iter(TMP["PSSD"][PDNAMEDF]), None)
                    if DDNAME is None:
                        break
                    DDIEN = next(iter(PSDRUG["B"][DDNAME]), None)
                    if not DDIEN:
                        continue
                    PS[50.7][SPDIEN][2.1] = SPDIEN
        # end of LIVE()

    def IVADD():
        # populate IV Additives, Solutions
        X1 = DT
        X2 = -365
        X = C(X1, X2)
        ADDIEN = 0
        while True:
            ADDIEN = next(iter(PS[52.6]), None)
            if ADDIEN is None:
                break
            DDIEN = int(PS[52.6][ADDIEN][0][2])
            if not DDIEN or not DDIEN in PS[PSDRUG]:
                continue
            NDND = PS[PSDRUG][DDIEN]["ND"]
            if not NDND[0] or not NDND[2]:
                continue
            DA = NDND[0]
            K = NDND[2]
            X = PSNAPIS(DA, K)
            if not X:
                continue
            DFPTR = X[0]
            if not DFPTR or not DFPTR in PS[50.606]:
                continue
            ADDNAME = PS[52.6][ADDIEN][0][0]
            if not ADDNAME:
                continue
            PDT = PS[52.6][ADDIEN][0][15]
            if PDT and PDT < X:
                continue
            AAAFLAG = 0
            for AAA in PS[50.7]["ADF"][ADDNAME][DFPTR]:
                if PS[50.7][AAA][2]:
                    AAAFLAG = 1
                    break
            if AAAFLAG:
                continue
            SPD = {
                ".01": ADDNAME,
                ".02": DFPTR,
                ".03": 1
            }
            SPDIEN = ADD(50.7, SPD)
            if not SPDIEN:
                continue
            PS[52.6][ADDIEN][0][15] = SPDIEN
            AAACT = 0
            for AAA in PS[52.6][ADDIEN][3]:
                SYNONYM = AAA[0]
                if SYNONYM and SYNONYM not in PS[50.7][SPDIEN][2]["B"]:
                    AAACT = AAACT + 1
                    PS[50.7][SPDIEN][2][AAACT] = SYNONYM
                    PS[50.7][SPDIEN][2]["B"][SYNONYM] = AAACT
            if AAACT:
                PS[50.7][SPDIEN][2]["0"] = f"^{AAACT}^{AAACT}"
        X1 = None
        X2 = None

    def IVSOL():
        # DO SAME AS ADDITIVES, BUT IF DATAISIN ADF WITH A ONE, MATCH AND DO SYN, IF NOT CREATE,MATCH AND DO SYN
        SOLIEN = 0
        while True:
            SOLIEN = next(iter(PS[52.7]), None)
            if SOLIEN is None:
                break
            DDIEN = int(PS[52.7][SOLIEN][0][2])
            if not DDIEN or not DDIEN in PS[PSDRUG]:
                continue
            NDND = PS[PSDRUG][DDIEN]["ND"]
            if not NDND[0] or not NDND[2]:
                continue
            DA = NDND[0]
            K = NDND[2]
            X = PSNAPIS(DA, K)
            if not X:
                continue
            DFPTR = X[0]
            if not DFPTR or not DFPTR in PS[50.606]:
                continue
            SOLNAME = PS[52.7][SOLIEN][0][0]
            if not SOLNAME:
                continue
            AAAFLAG = 0
            AAAMATCH = 0
            for AAA in PS[50.7]["ADF"][SOLNAME][DFPTR]:
                if PS[50.7][AAA][2]:
                    AAAFLAG = 1
                    AAAMATCH = AAA
                    break
            if AAAFLAG:
                PS[52.7][SOLIEN][0][9] = AAAMATCH
                for AAA in PS[52.7][SOLIEN][3]:
                    SYNONYM = AAA[0]
                    if SYNONYM and SYNONYM not in PS[50.7][AAAMATCH][2]["B"]:
                        AAACT = AAACT + 1
                        PS[50.7][AAAMATCH][2][AAACT] = SYNONYM
                        PS[50.7][AAAMATCH][2]["B"][SYNONYM] = AAACT
                ATOTAL = 0
                for AAACT in PS[50.7][AAAMATCH][2]:
                    ATOTAL = ATOTAL + 1
                if AAACT:
                    PS[50.7][AAAMATCH][2]["0"] = f"^{ATOTAL}^{ATOTAL}"
            else:
                SPD = {
                    ".01": SOLNAME,
                    ".02": DFPTR,
                    ".03": 1
                }
                SPDIEN = ADD(50.7, SPD)
                if not SPDIEN:
                    continue
                PS[52.7][SOLIEN][0][9] = SPDIEN
                AAACT = 0
                for AAA in PS[52.7][SOLIEN][3]:
                    SYNONYM = AAA[0]
                    if SYNONYM:
                        AAACT = AAACT + 1
                        PS[50.7][SPDIEN][2][AAACT] = SYNONYM
                        PS[50.7][SPDIEN][2]["B"][SYNONYM] = AAACT
                if AAACT:
                    PS[50.7][SPDIEN][2]["0"] = f"^{AAACT}^{AAACT}"

    def XREF():
        # do next line to xref whole file after looping thru ^TMP to populate
        pass

    def DUPL():
        # see if there's already an orderable item with the same name and dosage form
        OLDDF = None
        SPDIEN = None
        for SPDIEN in PS[50.7]["B"]:
            if PS[50.7][SPDIEN][0][0] == SOLNAME and PS[50.7][SPDIEN][0][1] == DF:
                PS[50.7]["AIV"][1][SOLIEN] = ""
                break

    return EN