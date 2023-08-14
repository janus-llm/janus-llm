def MIGR2(XOBY, PSSMSG):
    XOBY = """
        <drugMigrationResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="" xmlns="">
            <responseHeader>
                <endOfFile>0</endOfFile>
            </responseHeader>
        </drugMigrationResponse>
    """
    return XOBY


def MIGR(XOBY, PSSMSG):
    import os
    import tempfile

    U = "^"
    OUTCNT = 0
    OUT = []
    XMLFILE = {}

    def PRSTRING(XML, NWARRY):
        POS = 0
        GT = ">"
        while XML and GT in XML:
            POS = XML.index(GT) + 1
            FRNTEND = XML[:POS]
            XML = XML[POS:]
            NWARRY.append(FRNTEND)

    def DATE(Y):
        if Y:
            return str(Y)
        return ""

    def RESPONSE(PSS):
        PSSOUT = f"""
            <responseHeader>
                <endOfFile>{PSSEOF}</endOfFile>
            </responseHeader>
        """
        return PSSOUT

    def XMLBODY(PSS):
        PSSOUT = f"""
            <drugMigrationResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="" xmlns="">
                {RESPONSE(PSS)}
            </drugMigrationResponse>
        """
        return PSSOUT

    def TRASH():
        pass

    def OUT(X):
        nonlocal OUTCNT
        OUTCNT += 1
        OUT.append(X)
        PSSEOF = XMLFILE[PSS["FILE"]]["EOF"]
        FILE = FNAME
        RERR = 1
        PSS["xmlResponse"] = XMLBODY(PSS)
        XML2 = f"""
            <drugMigrationResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="" xmlns="">
                {RESPONSE(PSS)}
                <invalidRequest>{X}</invalidRequest>
            </drugMigrationResponse>
        """
        XOBY = XML2

    def GFILE():
        nonlocal FNAME
        FNAME = input("Enter Directory (path) and File Name")

    DT = tempfile.mkdtemp()
    XOBY = ""
    IEN = ""
    MIEN = ""
    CNT = 0
    OUT = []
    RCNT = 0
    XML2 = ""
    VAL = ""

    PRSTRING(PSSMSG, XMLFILE)

    for VAL in XMLFILE:
        XMLFILE[VAL] = XMLFILE[VAL]

    DOCHAND = 1
    PSS["date/time"] = DATE("")
    PSS["duz"] = ""

    PSS["body"] = 1
    PSS["bodyName"] = ""
    PSS["status"] = ""
    PSS["pepsIdNumber"] = ""

    if PSS["bodyName"] == "drugMigrationRequest":
        PSS["child"] = 2
        while PSS["child"]:
            PSS["child"] = PSS["child"] + 1
            PSS["ELE"] = ""
            if PSS["ELE"] == "ndfmsFile":
                PSS["FILE"] = XMLFILE[PSS["child"]]["T"][0]
            if PSS["ELE"] == "startingIen":
                PSS["IEN"] = XMLFILE[PSS["child"]]["T"][0]
            if PSS["ELE"] == "numElements":
                PSS["SNUM"] = XMLFILE[PSS["child"]]["T"][0]
            if PSS["ELE"] == "type":
                PSS["TYPE"] = XMLFILE[PSS["child"]]["T"][0]

    try:
        EN_PSSMIGR1(PSS["FILE"], PSS["IEN"], PSS["SNUM"], PSS["TYPE"])
    except Exception:
        pass

    RCNT = PSS["SNUM"]
    PSSEOF = XMLFILE[PSS["FILE"]]["EOF"]

    PSS["xmlResponse"] = XMLBODY(PSS)

    FILE = FNAME

    XML2 = f"""
        <drugMigrationResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="" xmlns="">
            {RESPONSE(PSS)}
        </drugMigrationResponse>
    """
    XOBY = XML2

    TRASH()

    return XOBY