def PSSMIGRR():
    pass

def VAPD():
    X = PSS["NAME"]
    Y = PSS["MVUID"]
    DIC = None
    DA = None
    DR = None
    DIE = None
    EFFDT = None
    STATUS = None
    EDT = None
    PACK = None
    UTIEN = None
    GCNO = None
    RTYPE = None
    NAME = None
    GENNAME = None
    GENIEN = None
    DFNAME = None
    DFIEN = None
    STRGEN = None
    UNITS = None
    NFNAME = None
    PRINTNAME = None
    PRODID = None
    TRANSTC = None
    DUIEN = None
    AINAME = None
    AIIEN = None
    AISTRG = None
    AIUNAME = None
    AINAME2 = None
    AIIEN2 = None
    AIUNAME2 = None
    GCNSEQNO = None
    PVADCCODE = None
    PVADCCLASS = None
    PVADCIEN = None
    NFINDICATOR = None
    CSFSCHED = None
    SMSPROD = None
    EDDINTER = None
    CPDOSAGE = None
    MVUID = None
    VUID = None
    PRODID = None
    PDTCREATE = None
    ODFDCHKX = None
    VAPTN = None
    
    if PSS["NAME"] == "":
        OUT(" Error...Missing Required VA PRODUCT NAME")
        return
    if PSS["MVUID"] == "":
        OUT(" Error...Missing Required VA PRODUCT Master Entry VUID")
        return
    if PSS["VUID"] == "":
        OUT(" Error...Missing Required VA PRODUCT VUID")
        return
    if PSS["EFFDT"] == "":
        OUT(" Error...Missing Required VA PRODUCT EFFECTIVE DATE/TIME")
        return
    if PSS["EDTS"] == "":
        OUT(" Error...Missing Required VA PRODUCT PRODUCT EFFECTIVE DATE/TIME")
        return
    if PSS["ODFDCHKX"] == "":
        OUT(" Error...Missing Required VA PRODUCT OVERRIDE DF DOSE CHK EXCLUSION")
        return
    
    RTYPE = PSS["RTYPE"]
    NAME = PSS["NAME"]
    GENNAME = PSS["GENNAME"]
    GENIEN = PSS["GENIEN"]
    DFNAME = PSS["DFNAME"]
    DFIEN = PSS["DFIEN"]
    STRGEN = PSS["STRGEN"]
    UNITS = PSS["UNITS"]
    NFNAME = PSS["NFNAME"]
    PRINTNAME = PSS["PRINTNAME"]
    PRODID = PSS["PRODID"]
    TRANSTC = PSS["TRANSTC"]
    DUNAME = PSS["DUNAME"]
    DUIEN = PSS["DUIEN"]
    GCNO = "0000000" + PSS["GCNSEQNO"]
    GCNSEQNO = GCNO[len(GCNO) - 5:]
    PVADCCLASS = PSS["PVADCCLASS"]
    PVADCCODE = PSS["PVADCCODE"]
    PVADCIEN = PSS["PVADCIEN"]
    NFINDICATOR = PSS["NFINDICATOR"]
    CSFSCHED = PSS["CSFSCHED"]
    SMSPROG = PSS["SMSPROD"]
    EDDINTER = PSS["EDDINTER"]
    if EDDINTER != 1:
        EDDINTER = ""
    ODFDCHKX = PSS["ODFDCHKX"]
    CPDOSAGE = PSS["CPDOSAGE"]
    PDTCREATE = PSS["PDTCREATE"]
    MVUID = PSS["MVUID"]
    VUID = PSS["VUID"]
    PRODID = PSS["PRODID"]
    IDATE = PSS["INACTDATE"].replace("T", "").replace("-", "")
    IDATE = HL7TFM(IDATE)
    FNUM = 50.68
    FNAME = "syncResponse.XML"
    FNAME1 = "dosageForm"
    ACTID = PSS["ACTID"]
    EFFDT = DATE(PSS["EFFDT"])
    STATUS = PSS["EDTS"]
    FDAMG = PSS["FDAMEDGUIDE"]
    SCODE = PSS["SCODE"]
    PACK = PSS["PACK"]
    if SMSPROG == "":
        SMSPROG = "@"
    
    if len(UNITS) > 0 and UNITS not in [x["B"] for x in PS[50.607]]:
        OUT(" Error...Invaild Units Name")
        return
    
    if RTYPE == "ADD":
        TMP = DD[50.68][0]["LAYGO"][0]
        if TMP != "":
            DD[50.68][0]["LAYGO"][0] = ""
        X = NAME
        DIC = 50.68
        DIC[0] = "LMXZ"
        Y = DIC
        if Y < 1:
            if TMP != "":
                DD[50.68][0]["LAYGO"][0] = TMP
            OUT(" Error...Cannot obtain an IEN for VA PRODUCT NAME")
            return
        DIE = DIC
        DA = Y
        DR = ".05////^S X=GENIEN;1////^S X=DFIEN;2///^S X=STRGEN;17///^S X=NFINDICATOR;3///^S X=UNITS;4///^S X=NFNAME;"
        DR += "5///^S X=PRINTNAME;6///^S X=PRODID;7///^S X=TRANSTC;8///^S X=DUNAME;"
        DR += "11////^S X=GCNSEQNO;15///^S X=PVADCIEN;42///^S X=PACK;"
        DR += "19///^S X=CSFSCHED;20///^S X=SMSPROG;23///^S X=EDDINTER;31///^S X=ODFDCHKX;"
        DR += "40///^S X=CPDOSAGE;41///^S X=PDTCREATE;99.98///^S X=MVUID;99.99///^S X=VUID;"
        DR += "100///^S X=FDAMG;2000///^S X=SCODE"
        PIEN = DA
        DIE = DIC
        DA = PIEN
        DR = ".02///^S X=STATUS"
        DIC = "^PSNDF(50.68," + str(PIEN) + ",""TERMSTATUS"","
        DIC[0] = "L"
        DIC["P"] = "50.6899DA"
        DA[1] = PIEN
        DA = 1
        X = EFFDT
        FILE(DICN)
        DIE = DIC
        DR = ".02///^S X=STATUS"
        FILE(DICN)
        if TMP != "":
            DD[50.68][0]["LAYGO"][0] = TMP
        if NAME != "":
            X = NAME
            DIC = 5000.506
            DIC[0] = "LMXZ"
            FILE(DICN)
        # if IDATE != "":
        #     X = NAME
        #     DIC = 5000.2
        #     DIC[0] = "LMXZ"
        #     FILE(DICN)
    
    if RTYPE == "MODIFY":
        PIEN = PSS["IEN"]
        DA = PIEN
        DIE = 50.68
        PS0 = PSNDF(50.68)[DA][0]
        PS1 = PSNDF(50.68)[DA][1]
        NAFI = PSNDF(50.68)[DA][5]
        EDCK = PSNDF(50.68)[DA][8]
        PVDC = PSNDF(50.68)[DA][3]
        PS1 = PSNDF(50.68)[DA][1]
        OVCK = PSNDF(50.68)[DA][9][0]
        PS7 = PSNDF(50.68)[DA][7]
        DOS = PSNDF(50.68)[DA]["DOS"]
        FMG = PSNDF(50.68)[DA]["MG"][0]
        VUID0 = PSNDF(50.68)[DA]["VUID"]
        PSF0 = PSNDF(50.68)[DA]["PFS"]
        DR = ""
        PQ = ""
        
        if PS0[1] != GENIEN:
            DR = ".05////" + ("" if GENIEN == "" else "^S X=GENIEN")
            PQ = ";"
        if PS0[2] != DFIEN:
            DR += PQ + "1////" + ("" if DFIEN == "" else "^S X=DFIEN")
            PQ = ";"
        if PS0[3] != STRGEN:
            DR += PQ + "2///" + ("" if STRGEN == "" else "^S X=STRGEN")
            PQ = ";"
            X = NAME
            DIC = 5000.4
            DIC[0] = "LMXZ"
            FILE(DICN)
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        UIEN = PS0[4]
        UNT = PS[50.607][UIEN][0] if UIEN != "" else ""
        if UNT != UNITS:
            DR += PQ + "3///" + ("" if UNITS == "" else "^S X=UNITS")
            PQ = ";"
            X = NAME
            DIC = 5000.92
            DIC[0] = "LMXZ"
            FILE(DICN)
        if DOS[0] != CPDOSAGE:
            DR += PQ + "40///^S X=CPDOSAGE"
            PQ = ";"
            X = NAME
            DIC = 5000.92
            DIC[0] = "LMXZ"
            FILE(DICN)
        if DOS[2] != PACK:
            DR += PQ + "42///" + ("" if PACK == "" else "^S X=PACK")
            PQ = ";"
            X = NAME
            DIC = 5000.92
            DIC[0] = "LMXZ"
            FILE(DICN)
        if DOS[1] != PDTCREATE:
            DR += PQ + "41///" + ("" if PDTCREATE == "" else "^S X=PDTCREATE")
            X = NAME
            DIC = 5000.92
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PS0[5] != NFNAME:
            DR += PQ + "4///" + ("" if NFNAME == "" else "^S X=NFNAME")
            PQ = ";"
        VAPTN = TRIM(UP(PS1[0]))
        if VAPTN != PRINTNAME:
            DR += PQ + "5///" + ("" if PRINTNAME == "" else "^S X=PRINTNAME")
            PQ = ";"
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PS1[1] != PRODID:
            DR += PQ + "6///" + ("" if PRODID == "" else "^S X=PRODID")
            PQ = ";"
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PS1[2] != TRANSTC:
            DR += PQ + "7///" + ("" if TRANSTC == "" else "^S X=TRANSTC")
            PQ = ";"
            X = NAME
            DIC = 5000.7
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PS1[3] != DUNIEN:
            DR += PQ + "8///" + ("" if DUNAME == "" else "^S X=DUNAME")
            PQ = ";"
        if PS1[4] != GCNSEQNO:
            DR += PQ + "11////" + ("" if GCNSEQNO == "" else "^S X=GCNSEQNO")
            PQ = ";"
        if PVDC != PVADCIEN:
            DR += PQ + "15///^S X=PVADCIEN"
            PQ = ";"
            X = NAME
            DIC = 5000.507
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PS7[0] != NFINDICATOR:
            DR += PQ + "17///^S X=NFINDICATOR"
            PQ = ";"
            X = NAME
            DIC = 5000.5
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PS7[1] != CSFSCHED:
            DR += PQ + "19///^S X=CSFSCHED"
            PQ = ";"
            X = NAME
            DIC = 5000.9
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PS7[2] != SMSPROG:
            DR += PQ + "20///^S X=SMSPROG"
            PQ = ";"
        if EDCK != EDDINTER:
            if EDCK != "" and EDDINTER != 0:
                DR += PQ + "23///" + ("" if EDDINTER == 1 else "@")
            PQ = ";"
            X = NAME
            DIC = 5000.23
            DIC[0] = "LMXZ"
            FILE(DICN)
        if OVCK != ODFDCHKX:
            DR += PQ + "31///^S X=ODFDCHKX"
            PQ = ";"
            X = NAME
            DIC = 5000.608
            DIC[0] = "LMXZ"
            FILE(DICN)
        if VUID0[1] != MVUID:
            DR += PQ + "99.98///^S X=MVUID"
            PQ = ";"
        if VUID0[0] != VUID:
            DR += PQ + "99.99///^S X=VUID"
            PQ = ";"
        if PS7[3] != IDATE:
            DR += PQ + "21///" + ("" if IDATE == "" else "^S X=IDATE")
            PQ = ";"
        if FMG != FDAMG:
            DR += PQ + "100///" + ("" if FDAMG == "" else "^S X=FDAMG")
            PQ = ";"
            X = NAME
            DIC = 5000.91
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PSF0[0] != SCODE:
            DR += PQ + "2000///" + ("" if SCODE == "" else "^S X=SCODE")
            PQ = ";"
        
        DA = PSS["IEN"]
        DIE = 50.68
        FILE(DICN)
        
        if ACTID > 0:
            UAI()
        
        UTIEN = PS0[5]
        if IDATE != "" and PS7[3] == "":
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if GENIEN != PS0[1]:
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if DFIEN != PS0[2]:
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if UTIEN != PS0[5]:
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if VAPTN != PRINTNAME:
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if PRODID != PS1[2]:
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        if DUNIEN != PS1[4]:
            X = NAME
            DIC = 5000.2
            DIC[0] = "LMXZ"
            FILE(DICN)
        
        EDCK()
        PVDC()
        OVCK()
        FMG()
        
    XMESS = "<message> <![CDATA[ Updated VA Product " + NAME + " ]]> </message>"
    XIEN = "<ien>" + str(PSS["IEN"]) + "</ien>"
    DIC = None
    DA = None
    DR = None
    DIE = None
    del TMP["AJF LAYGO"][0]
    return

def UAI():
    DIC = None
    DA = None
    DR = None
    DIE = None
    CNT = 0
    PIEN = PSS["IEN"]
    DA = None
    while CNT is not None:
        DIE = "^PSNDF(50.68," + str(PIEN) + ",2,"
        DA[1] = PIEN
        DA = CNT
        DR = ".01///@"
        FILE(DICN)
        CNT = None
    
    CNT = 1
    while CNT <= ACTID:
        if "AIIEN" + str(CNT) in PSS and PSS["AIIEN" + str(CNT)] is not None:
            DIC = "^PSNDF(50.68," + str(PIEN) + ",2,"
            DIC[0] = "L"
            DIC["P"] = "50.6814P"
            AIIEN = PSS["AIIEN" + str(CNT)]
            AISTRG = PSS["AISTRG" + str(CNT)]
            AINAME = PSS["AIUNAME" + str(CNT)]
            DA[1] = PIEN
            DA = AIIEN
            X = AIIEN
            FILE(DICN)
            DIE = DIC
            DR = "1///^S X=AISTRG;2///^S X=AINAME"
            FILE(DICN)
        CNT += 1
    return

def EDCK():
    DIC = None
    DA = None
    DR = None
    DIE = None
    X = None
    Y = None
    DIC = "^PSNDF(50.68," + str(DA) + ",2,"
    DIC[0] = "LMXZ"
    FILE(DICN)
    DIE = DIC
    DA = +Y
    DR = "1///" + ("" if EDDINTER == "" else "^S X=EDDINTER")
    FILE(DICN)
    return

def PVDC():
    DIC = None
    DA = None
    DR = None
    DIE = None
    X = None
    Y = None
    DIC = "^PSNDF(50.68," + str(DA) + ",2,"
    DIC[0] = "LMXZ"
    FILE(DICN)
    DIE = DIC
    DA = +Y
    DR = "2///^S X=PVDC;3///^S X=PVADCIEN"
    FILE(DICN)
    DIC = "^PSNDF(50.68," + str(DA) + ",2,"
    DIC[0] = "LMXZ"
    Y = DIC
    DIE = DIC
    DA = +Y
    DR = "1///^S X=PVDC;2///^S X=PVADCIEN;3///^S X=GENIEN"
    FILE(DICN)
    return

def OVCK():
    DIC = None
    DA = None
    DR = None
    DIE = None
    X = None
    Y = None
    DIC = "^PSNDF(50.68," + str(DA) + ",2,"
    DIC[0] = "LMXZ"
    FILE(DICN)
    DIE = DIC
    DA = +Y
    DR = "1///^S X=OVCK;2///^S X=ODFDCHKX"
    FILE(DICN)
    return

def FMG():
    DIC = None
    DA = None
    DR = None
    DIE = None
    X = None
    Y = None
    DIC = "^PSNDF(50.68," + str(PSS["IEN"]) + ",2,"
    DIC[0] = "LMXZ"
    FILE(DICN)
    (X, DINUM) = (PSS["IEN"], PSS["IEN"])
    DIC = 5000.91
    DIC[0] = "LMXZ"
    FILE(DICN)
    FAMG = "A" if FMG == "" else "E" if FDAMG != "" else "D"
    DIE = DIC
    DA = +Y
    DR = "1///^S X=FAMG"
    FILE(DICN)
    return

def UP(X):
    return X.upper()