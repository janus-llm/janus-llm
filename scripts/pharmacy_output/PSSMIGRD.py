def PSSMIGRD(PSS):
    FNAME = "SyncResponse.XML"
    FL = PSS.get("FILE", "")
    if FL == "":
        OUT(" Error... Missing required data")
        return
    XST = 0
    CNT = 0
    if FL == 50.607:
        DUNI()
        return
    if FL == 50.416:
        DING()
        return
    if FL == 50.605:
        VADC()
        return
    if FL == 50.606:
        DSFO()
        return
    if FL == 50.6:
        VAGN()
        return
    if FL == 50.64:
        VADU()
        return
    if FL == 55.95:
        MAN()
        return
    if FL == 50.608:
        PTYP()
        return
    if FL == 50.67:
        NDC()
        return
    if FL == 50.68:
        VAPD()
        return
    OUT(" Error... Invalid File Number")


def DUNI():
    NAME = PSS.get("NAME", "")
    IEN = PSS.get("IEN", "")
    RTYPE = PSS.get("RTYPE", "")
    IDATE = PSS.get("IDATE", "").replace("T", "")
    IDATE = HL7TFM(IDATE, "L")
    FNAME = "syncResponse.XML"
    FNUM = 50.607
    FNAME1 = "drugUnits"
    if RTYPE == "ADD":
        L.acquire()
        TMP = DD(50.607, ".01", "LAYGO", ".01", 0)
        if TMP:
            DD(50.607, ".01", "LAYGO", ".01", 0) = TMP
        X = NAME
        DIC = 50.607
        DIC(0) = "LMXZ"
        DIC
        Y = Y + 1
        if Y < 1:
            OUT(" Error...Cannot obtain an IEN for NAME")
            if TMP:
                DD(50.607, ".01", "LAYGO", ".01", 0) = TMP
            L.release()
            return
        PSS["IEN"] = Y
        PSS["IEN"] = DA
        DIE = DIC
        DR = "1///^S X=IDATE"
        D()
        if TMP:
            DD(50.607, ".01", "LAYGO", ".01", 0) = TMP
        L.release()
    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = "^PS(50.607,"
        PS5 = ^PS(50.607, DA, 0)
        DR = ""
        PQ = ""
        if $P(PS5, "^", 1) != NAME:
            DR = ".01///^S X=NAME"
        if DR:
            PQ = ";"
        DR = DR + PQ + "1///" + (IDATE if IDATE else "@")
        D()
    XMESS = "<message>  Updated Drug Units: " + NAME + " </message>"
    XIEN = "<ien>" + str(PSS["IEN"]) + "</ien>"
    del DIC, DA, DR, DIE, ^TMP("AJF LAYGO", $J)


def VADU():
    IEN = PSS["IEN"]
    NAME = PSS["NAME"]
    RTYPE = PSS["RTYPE"]
    IDATE = PSS["IDATE"].replace("T", "")
    IDATE = HL7TFM(IDATE, "L")
    FNUM = 50.64
    FNAME = "syncResponse.XML"
    FNAME1 = "vaDispenseUnits"
    ERROR = 0
    if RTYPE == "MODIFY" and not IEN:
        OUT(" Error... Invalid IEN")
        return
    if not NAME:
        OUT(" Error...Missing Required NAME")
        return
    if RTYPE != "ADD" and RTYPE != "MODIFY":
        OUT("Error...Invalid Request Type")
        return
    if RTYPE == "ADD":
        L.acquire()
        TMP = DD(50.64, ".01", "LAYGO", ".01", 0)
        if TMP:
            DD(50.64, ".01", "LAYGO", ".01", 0) = TMP
        X = NAME
        DIC = 50.64
        DIC(0) = "LMXZ"
        DIC
        Y = Y + 1
        if Y < 1:
            ERROR = 1
            OUT(" Error...Cannot obtain an IEN for NAME")
            if TMP:
                DD(50.64, ".01", "LAYGO", ".01", 0) = TMP
            L.release()
            return
        PSS["IEN"] = Y
        PSS["IEN"] = DA
        DIE = DIC
        D()
        if TMP:
            DD(50.64, ".01", "LAYGO", ".01", 0) = TMP
        L.release()
    if ERROR == 1:
        return
    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = 50.64
        PS5 = ^PSNDF(50.64, DA, 0)
        DR = ""
        PQ = ""
        if $P(PS5, "^", 1) != NAME:
            DR = ".01///^S X=NAME"
        if DR:
            PQ = ";"
        DR = DR + PQ + "1///" + (IDATE if IDATE else "@")
        D()
    XMESS = "<message> Updated Dispense Units " + NAME + " </message>"
    XIEN = "<ien>" + str(PSS["IEN"]) + "</ien>"
    del DIC, DA, DR, DIE, ^TMP("AJF LAYGO", $J)


def DING():
    IEN = PSS["IEN"]
    NAME = PSS["NAME"]
    RTYPE = PSS["RTYPE"]
    PRIMARY = PSS["PRIMARY"]
    MVUID = PSS["MASTERVUID"]
    VUID = PSS["VUID"]
    EFFDT = PSS["EFFDATE"]
    STATUS = PSS["STATUS"]
    IDATE = PSS["INACTDATE"].replace("T", "")
    IDATE = HL7TFM(IDATE, "L")
    FNUM = 50.416
    FNAME = "syncResponse.XML"
    FNAME1 = "drugIngredients"
    if NAME == "":
        OUT(" Error...Missing Required NAME")
        return
    if MVUID == "":
        OUT(" Error...Missing Required MASTER VUID")
        return
    if VUID == "":
        OUT(" Error...Missing Required VUID")
        return
    if EFFDT == "":
        OUT(" Error...Missing Required EFFECTIVE DATE")
        return
    if STATUS == "":
        OUT(" Error...Missing Required STATUS")
        return
    if RTYPE == "MODIFY" and not IEN:
        OUT(" Error... Invalid IEN")
        return
    EFFDT = DATE(EFFDT)
    if RTYPE == "ADD":
        L.acquire()
        TMP = DD(50.416, ".01", "LAYGO", ".01", 0)
        if TMP:
            DD(50.416, ".01", "LAYGO", ".01", 0) = TMP
        X = NAME
        DIC = 50.416
        DIC(0) = "LMXZ"
        DIC
        Y = Y + 1
        if Y < 1:
            OUT(" Error...Cannot obtain an IEN for NAME")
            if TMP:
                DD(50.416, ".01", "LAYGO", ".01", 0) = TMP
            L.release()
            return
        PSS["IEN"] = Y
        PSS["IEN"] = DA
        DIE = DIC
        DR = "2///^S X=PRIMARY;3///^S X=IDATE;99.98///^S X=MVUID;99.99///^S X=VUID"
        D()
        DIC = "^PS(50.416," + PIEN + ',"TERMSTATUS",'
        DIC(0) = "L"
        DIC("P") = "50.4169A"
        DA(1) = PIEN
        DA = 1
        X = EFFDT
        FILE()
        DIE = DIC
        DR = ".02///^S X=STATUS"
        D()
        L.release()
    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = 50.416
        PS5 = ^PS(50.416, DA, 0)
        DR = ""
        PQ = ""
        if $P(PS5, "^", 2) != IDATE:
            DR = "3///" + (IDATE if IDATE else "@")
        if DR:
            PQ = ";"
        PSX = $P(^PS(50.416, DA, 2), "^", 1)
        PSX = ("NO" if PSX == 0 else "YES")
        if PSX != EXCLUDE:
            DR = DR + PQ + "11///" + (EXCLUDE if EXCLUDE else "@")
        D()
    XMESS = "<message>  Updated Drug Ingredients: " + NAME + " </message>"
    XIEN = "<ien>" + str(PSS["IEN"]) + "</ien>"
    del DIC, DA, DR, DIE, ^TMP("AJF LAYGO", $J)


def VADC():
    DA = PSS.get("PCIEN", "")
    DIE = "^PS(50.605,"
    DR = ""
    PQ = ""
    if $P(^PS(50.605, DA, 0), "^", 3) != PCIEN:
        DR = "2///" + (PCIEN if PCIEN else "@")
    if DR:
        PQ = ";"
    if $P(^PS(50.605, DA, 0), "^", 4) != TYPE:
        DR = DR + PQ + "3///" + (TYPE if TYPE else "@")
    if DR:
        PQ = ";"
    if $P(^PS(50.605, DA, 1), "^", 1) != DESC:
        DR = DR + PQ + "4///" + (DESC if DESC else "@")
    if DR:
        PQ = ";"
    PSX = $P(^PS(50.605, DA, "VUID"), "^", 2)
    PSX = ("YES" if PSX == 1 else "NO")
    if PSX != MVUID:
        DR = DR + PQ + "99.98///^S X=MVUID"
    if DR:
        PQ = ";"
    if $P(^PS(50.605, DA, "VUID"), "^", 1) != VUID:
        DR = DR + PQ + "99.99///^S X=VUID"
    if DR:
        PQ = ";"
    D()
    XMESS = "<message>  Updated Drug Class " + CODE + " </message>"
    XIEN = "<ien>" + str(PSS["IEN"]) + "</ien>"
    del DIC, DA, DR, DIE, ^TMP("AJF LAYGO", $J)


def DSFO():
    NAME = PSS["NAME"]
    EXCLUDE = PSS["EXCLUDE"]
    RTYPE = PSS["RTYPE"]
    IDATE = PSS["INACTDATE"].replace("T", "")
    IDATE = HL7TFM(IDATE, "L")
    PERDOSE = PSS["PERDOSE"]
    PDPACKAGE = PSS["PDPACKAGE"]
    UNIT = PSS["UNITS"]
    PACKAGE = PSS["PACKAGE"]
    FNUM = 50.606
    FNAME = "syncResponse.XML"
    FNAME1 = "dosageForm"
    if NAME == "":
        OUT(" Error...Missing Required DOSAGE FORM NAME")
        return
    if EXCLUDE == "":
        OUT(" Error...Missing Required Exclude From Dosage Checks FLAG")
        return
    if RTYPE != "ADD" and RTYPE != "MODIFY":
        OUT("Error...Invalid Request Type")
        return
    if RTYPE == "ADD":
        L.acquire()
        TMP = DD(50.606, ".01", "LAYGO", ".01", 0)
        if TMP:
            DD(50.606, ".01", "LAYGO", ".01", 0) = TMP
        X = NAME
        DIC = 50.606
        DIC(0) = "LMXZ"
        DIC
        Y = Y + 1
        if Y < 1:
            OUT(" Error...Cannot obtain an IEN for NAME")
            if TMP:
                DD(50.606, ".01", "LAYGO", ".01", 0) = TMP
            L.release()
            return
        PSS["IEN"] = Y
        PSS["IEN"] = DA
        DIE = DIC
        DR = "7///^S X=IDATE;11///^S X=EXCLUDE"
        D()
        if TMP:
            DD(50.606, ".01", "LAYGO", ".01", 0) = TMP
        L.release()
    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = 50.606
        PS5 = ^PS(50.606, DA, 0)
        DR = ""
        PQ = ""
        if $P(PS5, "^", 2) != IDATE:
            DR = "7///" + (IDATE if IDATE else "@")
        if DR:
            PQ = ";"
        PSX = $P(^PS(50.606, DA, 1), "^", 1)
        PSX = ("NO" if PSX == 0 else "YES")
        if PSX != EXCLUDE:
            DR = DR + PQ + "11///" + (EXCLUDE if EXCLUDE else "@")
        if DR:
            PQ = ";"
        D()
    XMESS = "<message> <![CDATA[ Updated Dosage Form " + NAME + " ]]> </message>"
    XIEN = "<ien>" + str(PSS["IEN"]) + "</ien>"
    del DIC, DA, DR, DIE, ^TMP("AJF LAYGO", $J)


def DATE(DT):
    if len(DT) == 0:
        return ""
    FDT = DT.replace("-", "")
    FDT = HL7TFM(FDT, "L")
    return FDT