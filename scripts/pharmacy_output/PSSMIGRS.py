def PSSMIGRS(XOBY,PSSMSG):
    # Entry point into routine
    def PRSTRING(XML, NWARRY):
        # Parses the incoming XML string from PEPS
        if not XML:
            OUT("Error... Invalid XML string")
            return
        POS = 0
        GT = ">"
        CNT = 0
        while XML and (">" in XML):
            POS = XML.find(GT) + 1
            FRNTEND = XML[:POS-1]
            XML = XML[POS:]
            NWARRY.append(FRNTEND)
            CNT += 1

    U = "^"
    INPUT = ""
    OUTCNT = 0
    DATE = DT
    PST = ""

    OUT = {}
    XMLFILE = {}
    PSS = {}
    RERR = {}
    PSNDC = {}
    PSUPN = {}
    PSMAN = {}
    PSTNAME = {}
    PSPNAME = {}
    PSSIZE = {}
    PSTYPE = {}
    PSOTC = {}
    NIEN = {}
    MIEN = {}
    TIEN = {}
    SIEN = {}
    PSCNT = {}
    PSNUM = {}
    D = {}
    DA = {}
    DATE = {}
    DIC = {}
    DIE = {}
    DLAYGO = {}
    DOCHAND = {}
    DR = {}
    DT = {}
    FILE = {}
    FRMTENT = {}
    GT = {}
    IMPUT = {}
    LEN = {}
    MIEN = {}
    NIEN = {}
    NWARRY = {}
    OUT = {}
    PS0 = {}
    PSNDC1 = {}
    XML2 = {}
    PSIADT = {}
    NIEN2 = {}
    PNIEN = {}
    DIK = {}
    PNT = {}

    DT^DICRW()
    U = "^"
    INPUT = ""
    OUTCNT = 0
    DATE = DT
    PST = ""

    OUT = []
    TMP_J_OUT = {}
    TMP_J_XML_OUT = {}
    TMP_J_NDC1 = {}
    TMP_J_NDC1["START"] = DATE
    TMP_J_NDC1["XML"] = PSSMSG

    PRSTRING(PSSMSG, XMLFILE)

    VAL = ""
    for VAL in XMLFILE:
        TMP_J_XML_OUT[VAL] = XMLFILE[VAL]

    DOCHAND = EN^MXMLDOM(TMP_J_XML_OUT, "VO")
    PSS["date/time"] = NOW^XLFDT()
    PSS["duz"] = DUZ
    PSUPN = MIEN = PSTNAME = PNIEN = SIEN = TIEN = PSOTC = PSIADT = ""

    PSS["body"] = PARENT^MXMLDOM(DOCHAND, 2)
    PSS["bodyName"] = NAME^MXMLDOM(DOCHAND, PSS["body"])
    PSS["status"] = VALUE^MXMLDOM(DOCHAND, PSS["body"], "status")
    PSS["pepsIdNumber"] = VALUE^MXMLDOM(DOCHAND, PSS["body"], "pepsIdNumber")

    if PSS["bodyName"] == "ndcMigrationSynchRequest":
        PSS["child"] = 1
        PSS["FILE"] = 50.67
        PSSTITLE = "ndcMigrationSynchResponse"
        PST = "ndc"
        while PSS["child"] in ^TMP("MXMLDOM", DOCHAND):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "ndc":
                PSNDC = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ndcIen":
                NIEN = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "upn":
                PSUPN = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "manufacturer":
                PSMAN = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "manufacturerIen":
                MIEN = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "tradeName":
                PSTNAME = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "productName":
                PSPNAME = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "productIen":
                PIEN = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "packageSize":
                PSSIZE = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "inactivationDate":
                PSIADT = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "packageType":
                PSTYPE = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "packageTypeIen":
                PKIEN = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "otcRxIndicator":
                PSOTC = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "status":
                PSTATUS = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "manufacturerMigrationSyncRequest":
        PSS["child"] = 1
        PSS["FILE"] = 55.95
        PSSTITLE = "manufacturerMigrationSynchResponse"
        PST = "manufacturer"
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 1, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "manufacturer":
                PSS["NAME"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "NDCNumber":
                PSS["NDCNUM"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "inactivationDate":
                PSS["IDATE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "packageTypeMigrationSyncRequest":
        PSS["child"] = 1
        PSS["FILE"] = 50.608
        PSSTITLE = "packageTypeMigrationSynchResponse"
        PST = "packageType"
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 1, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "packageType":
                PSS["NAME"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "inactivationDate":
                PSS["IDATE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "drugUnitSyncRequest":
        PSS["child"] = 1
        PSS["FILE"] = 50.607
        PSSTITLE = "drugUnitMigrationSynchResponse"
        PST = "drugUnit"
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 1, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "drugUnitName":
                PSS["NAME"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "inactivationDate":
                PSS["IDATE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "drugIngredientsSyncRequest":
        PSS["child"] = 2
        PSS["FILE"] = 50.416
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 2, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "genericNameSyncRequest":
        PSS["child"] = 2
        PSS["FILE"] = 50.6
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 2, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "dispenseUnitSyncRequest":
        PSS["child"] = 2
        PSS["FILE"] = 50.64
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 2, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "drugClassSyncRequest":
        PSS["child"] = 2
        PSS["FILE"] = 50.605
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 2, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "dosageFormSyncRequest":
        PSS["child"] = 2
        PSS["FILE"] = 50.606
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 2, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    if PSS["bodyName"] == "productSyncRequest":
        PSS["child"] = 2
        PSS["FILE"] = 50.68
        while PSS["child"] in CHILD^MXMLDOM(DOCHAND, 2, PSS["child"]):
            PSS["ELE"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)
            if PSS["ELE"] == "ien":
                PSS["IEN"] = ^TMP("MXMLDOM", DOCHAND, PSS["child"], "T", 1)

    # Date conversion
    # PSIADT = PSIADT.replace("T", "").replace("-", "")
    # PSIADT = HL7TFM^XLFDT(PSIADT)

    # Check for Migration Status
    if PSTATUS == "Start":
        X = 0
        while X in ^PSNDF(50.67):
            if not $P(^PSNDF(50.67,X,0), "^", 7):
                TMP_J_NDC[X] = ""
            X += 1
        XMESS = "Started"
        XIEN = ""
        XMLR()

    if PSTATUS == "Stop":
        X = 0
        while X in ^TMP($J, "NDC", X):
            if not $D(^PSNDF(50.67,X,0)):
                continue
            $P(^PSNDF(50.67,X,0), "^", 7) = DATE
        XMESS = "Stop"
        XIEN = ""
        XMLR()

    MIGR()
    
    # Process sync request

    return

def PRSTRING(XML, NWARRY):
    if not XML:
        OUT("Error... Invalid XML string")
        return
    POS = 0
    GT = ">"
    CNT = 0
    while XML and (">" in XML):
        POS = XML.find(GT) + 1
        FRNTEND = XML[:POS-1]
        XML = XML[POS:]
        NWARRY.append(FRNTEND)
        CNT += 1

def XMLR():
    # Generate XML response message
    
    PSS["xmlResponse"] = XMLBODY(PSS)

    # Store value in VistALink return parameter

    # Write the XML response message to a new file
    FILE = PSSTITLE + ".XML"
    XML2 = PSS["xmlHeader"] + "<" + PSSTITLE + PSS["xmlns:xsi"]
    XML2 = XML2 + PSS["xmlns"] + ">" + "<responseType>" + "<status>Success</status>"
    XML2 = XML2 + XMESS + "</responseType>" + XIEN
    XOBY = XML2 + "</" + PSSTITLE + ">"
    TMP_J_NDC1["XOBY"] = XOBY

def OUT(X):
    FILE = PSSTITLE + ".XML"
    RERR = 1
    PSS["xmlResponse"] = XMLBODY(PSS)
    XML2 = PSS["xmlHeader"] + "<" + PSSTITLE + PSS["xmlns:xsi"]
    XML2 = XML2 + PSS["xmlns"] + "><responseType><status>Failure</status>"
    XML2 = XML2 + "<message>" + X + "</message></responseType></" + PSSTITLE + ">"
    XOBY = XML2
    TMP_J_NDC1["OUT"] = XOBY
    Q1()

def Q1():
    # Exit and clean-up
    # K ^TMP("MXMLDOM",$J)
    return

def RESPONSE(PSS):
    # Check to see if current XML message was successfully written to the PEPS QUEUE file (#54.5)
    PSSOUT = ""
    if PSS["ERR"]:
        PSS["response"] = "Failure"
        PSS["attribValue"] = "<response status=\"" + PSS["response"] + "\">Unable to queue message. Reason: " + PSS["ERR"].split("^")[1] + "</response>"
    elif PSS["pepsIdNumber"] in ^PSSPEPS("B"):
        PSS["response"] = "Queued"
        PSS["attribValue"] = "<response status=\"" + PSS["response"] + "\">Message " + PSS["pepsIdNumber"] + " is queued.</response>"
    else:
        PSS["response"] = "Failure"
        PSS["attribValue"] = "<response status=\"" + PSS["response"] + "\">Unable to queue message " + PSS["pepsIdNumber"] + ". Reason: " + PSS["ERR"].split("^")[1] + "</response>"
    PSSOUT = XMLBODY(PSS)
    return PSSOUT

def XMLBODY(PSS):
    # Generates response XML message
    PSS["xmlHeader"] = XMLHDR^MXMLUTL()
    PSS["xmlns:xsi"] = " xmlns:xsi=\"http://www.w3.org/2001/XMLSchema\""
    PSS["xmlns"] = " xmlns=\"gov/va/med/pharmacy/peps/external/common/vo/inbound/migration/" + PST + "/response\""
    PSSOUT = PSS["xmlHeader"]
    PSSOUT = PSSOUT + "<" + PSSTITLE
    PSSOUT = PSSOUT + " " + PSS["xmlns:xsi"]
    PSSOUT = PSSOUT + " " + PSS["xmlns"]
    return PSSOUT

PSSMIGRS(XOBY, PSSMSG)