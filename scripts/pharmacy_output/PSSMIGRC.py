def PSSMIGRC(XOBY, PSSMSG):
    # Variable Definitions
    X, Y, DIR, PATH, FILE, DOCHAND, PSSFDA, XMLFILE, VAL, LEN, INPUT, XFILE, OUTCNT, PSS, PSTATUS, ERROR, PSNDC, PSUPN, PSMAN, PSTNAME, PSPNAME, PSSIZE, PSTYPE, PSOTC, NIEN, MIEN, TIEN, SIEN, PSCNT, PSNUM, D, DA, DATE, DIC, DIE, DLAYGO, DOCHAND, DOCHAND1, DR, DT, FILE, FRMTENT, GT, INPUT, LEN, MIEN, NIEN, NWARRY, OUT, PS0, PSNDC1, XML2, PSIADT, NIEN2, PNIEN, DIK, PNT, BNAME, PSSTITLE, PST, XMESS, XIEN, JOB

    DT^DICRW()
    U = "^"
    INPUT = ""
    ERROR = 0
    OUTCNT = 0
    DATE = DT
    PST = ""
    DUZ(0) = "@"

    OUT = ^UTILITY($J,"OUT")
    K ^UTILITY($J), ^TMP($J,"XML OUT")
    ^TMP($J,"NDC1","START") = DATE
    ^TMP($J,"NDC1","XML") = PSSMSG

    PRSTRING(PSSMSG, XMLFILE)

    VAL = ""
    while VAL != "":
        ^TMP($J,"XML OUT",VAL) = XMLFILE(VAL)

    DOCHAND = $$EN^MXMLDOM($NA(^TMP($J,"XML OUT")),"VO")
    PSS("date/time") = $$NOW^XLFDT
    PSS("duz") = DUZ
    PSS("FILE") = ""
    PSUPN, MIEN, PSTNAME, PNIEN, SIEN, TIEN, PSOTC, PSIADT, PSSTITLE = ""
    
    PSS("body") = $$PARENT^MXMLDOM(DOCHAND, 2)
    PSS("bodyName") = $$NAME^MXMLDOM(DOCHAND, PSS("body"))
    PSS("status") = $$VALUE^MXMLDOM(DOCHAND, PSS("body"), "status")
    PSS("pepsIdNumber") = $$VALUE^MXMLDOM(DOCHAND, PSS("body"), "pepsIdNumber")
    JOB = $J

    BNAME = PSS("bodyName")
    if BNAME != "":
        if BNAME == "ndcSyncRequest":
            NDC()
        elif BNAME == "manufacturerSyncRequest":
            MAN()
        elif BNAME == "packageTypeSyncRequest":
            PACK()
        elif BNAME == "drugUnitSyncRequest":
            DRU()
        elif BNAME == "vaDispenseUnitSyncRequest":
            DIS()
        elif BNAME == "drugIngredientSyncRequest":
            DRUI()
        elif BNAME == "vaGenericNameSyncRequest":
            VAG()
        elif BNAME == "drugClassSyncRequest":
            DRUC()
        elif BNAME == "dosageFormSyncRequest":
            DOF()
        elif BNAME == "vaProductSyncRequest":
            VAP()

    if PSS("FILE") == "":
        OUT(" Error...Missing Required START TAG")
        return

    if PSS("RTYPE") != "ADD" and PSS("RTYPE") != "MODIFY":
        OUT("Error...Invalid Request Type")
        return

    if PSS("RTYPE") == "MODIFY" and not PSS("IEN"):
        OUT(" Error... Missing Required IEN")
        return

    MIGR()

def NDC():
    if PSS("bodyName") == "ndcSyncRequest":
        PSS("child") = 1
        PSS("FILE") = 50.67
        PSSTITLE = "syncResponse"

        while PSS("child") != 0:
            PSS("ELE") = $$NAME^MXMLDOM(DOCHAND, PSS("child"))
            if PSS("ELE") == "RequestType":
                PSS("RTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "ndcName":
                PSS("NAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "ndcIen":
                PSS("IEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "upn":
                PSS("UPN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "tradeName":
                PSS("TNAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "manufacturer":
                DOCHAND1 = PSS("child")
                PSS("child1") = 1
                while PSS("child1") != 0:
                    PSS("ELE1") = $$NAME^MXMLDOM(DOCHAND,PSS("child1"))
                    if PSS("ELE1") == "manufacturerName":
                        PSS("MNAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    elif PSS("ELE1") == "manufacturerIen":
                        PSS("MIEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    PSS("child1") = $$CHILD^MXMLDOM(DOCHAND,DOCHAND1,PSS("child1"))

            elif PSS("ELE") == "product":
                DOCHAND1 = PSS("child")
                PSS("child1") = 1
                while PSS("child1") != 0:
                    PSS("ELE1") = $$NAME^MXMLDOM(DOCHAND,PSS("child1"))
                    if PSS("ELE1") == "productName":
                        PSS("PNAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    elif PSS("ELE1") == "productIen":
                        PSS("PIEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    PSS("child1") = $$CHILD^MXMLDOM(DOCHAND,DOCHAND1,PSS("child1"))

            elif PSS("ELE") == "packageSize":
                PSS("PSIZE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "inactivationDate":
                PSS("IDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "packageType":
                DOCHAND1 = PSS("child")
                PSS("child1") = 1
                while PSS("child1") != 0:
                    PSS("ELE1") = $$NAME^MXMLDOM(DOCHAND,PSS("child1"))
                    if PSS("ELE1") == "packageTypeName":
                        PSS("PTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    elif PSS("ELE1") == "packageTypeIen":
                        PSS("PTIEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    PSS("child1") = $$CHILD^MXMLDOM(DOCHAND,DOCHAND1,PSS("child1"))

            elif PSS("ELE") == "otcRxIndicator":
                PSS("PSOTC") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)

def MAN():
    if PSS("bodyName") == "manufacturerSyncRequest":
        PSS("child") = 1
        PSS("FILE") = 55.95
        PSSTITLE = "syncResponse"

        while PSS("child") != 0:
            PSS("ELE") = $$NAME^MXMLDOM(DOCHAND, PSS("child"))
            if PSS("ELE") == "RequestType":
                PSS("RTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "manufacturerIen":
                PSS("IEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "manufacturerName":
                PSS("NAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "NDCNumber":
                PSS("NDCNUM") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "inactivationDate":
                PSS("IDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)

def PACK():
    if PSS("bodyName") == "packageTypeSyncRequest":
        PSS("child") = 1
        PSS("FILE") = 50.608
        PSSTITLE = "syncResponse"

        while PSS("child") != 0:
            PSS("ELE") = $$NAME^MXMLDOM(DOCHAND, PSS("child"))
            if PSS("ELE") == "RequestType":
                PSS("RTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "packageTypeIen":
                PSS("IEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "packageTypeName":
                PSS("NAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "inactivationDate":
                PSS("IDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)

def DRU():
    if PSS("bodyName") == "drugUnitSyncRequest":
        PSS("child") = 1
        PSS("FILE") = 50.607
        PSSTITLE = "syncResponse"

        while PSS("child") != 0:
            PSS("ELE") = $$NAME^MXMLDOM(DOCHAND, PSS("child"))
            if PSS("ELE") == "RequestType":
                PSS("RTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "drugUnitIen":
                PSS("IEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "drugUnitName":
                PSS("NAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "inactivationDate":
                PSS("IDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)

def DIS():
    if PSS("bodyName") == "vaDispenseUnitSyncRequest":
        PSS("child") = 1
        PSS("FILE") = 50.64
        PSSTITLE = "syncResponse"

        while PSS("child") != 0:
            PSS("ELE") = $$NAME^MXMLDOM(DOCHAND, PSS("child"))
            if PSS("ELE") == "RequestType":
                PSS("RTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "vaDispenseUnitIen":
                PSS("IEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "vaDispenseUnitName":
                PSS("NAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "inactivationDate":
                PSS("IDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)

def DRUI():
    if PSS("bodyName") == "drugIngredientSyncRequest":
        PSS("child") = 1
        PSS("FILE") = 50.416
        PSSTITLE = "syncResponse"

        while PSS("child") != 0:
            PSS("ELE") = $$NAME^MXMLDOM(DOCHAND, PSS("child"))
            if PSS("ELE") == "RequestType":
                PSS("RTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "drugIngredientName":
                PSS("NAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "ingredientIen":
                PSS("IEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "primaryIngredient":
                PSS("PRIMARY") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "inactivationDate":
                PSS("INACTDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "masterEntryForVuid":
                PSS("MASTERVUID") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "vuid":
                PSS("VUID") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "effectiveDateTimeRecord":
                DOCHAND1 = PSS("child")
                PSS("child1") = 1
                while PSS("child1") != 0:
                    PSS("ELE1") = $$NAME^MXMLDOM(DOCHAND,PSS("child1"))
                    if PSS("ELE1") == "effectiveDateTime":
                        PSS("EFFDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    elif PSS("ELE1") == "status":
                        PSS("STATUS") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    PSS("child1") = $$CHILD^MXMLDOM(DOCHAND,DOCHAND1,PSS("child1"))

def VAG():
    if PSS("bodyName") == "vaGenericNameSyncRequest":
        PSS("child") = 1
        PSS("FILE") = 50.6
        PSSTITLE = "syncResponse"

        while PSS("child") != 0:
            PSS("ELE") = $$NAME^MXMLDOM(DOCHAND, PSS("child"))
            if PSS("ELE") == "RequestType":
                PSS("RTYPE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "vaGenericNameIen":
                PSS("IEN") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "vaGenericNameName":
                PSS("NAME") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "masterEntryForVuid":
                PSS("MASTERVUID") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "inactivationDate":
                PSS("INACTDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "vuid":
                PSS("VUID") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child"),"T",1)
            elif PSS("ELE") == "effectiveDateTimeRecord":
                DOCHAND1 = PSS("child")
                PSS("child1") = 1
                while PSS("child1") != 0:
                    PSS("ELE1") = $$NAME^MXMLDOM(DOCHAND,PSS("child1"))
                    if PSS("ELE1") == "effectiveDateTime":
                        PSS("EFFDATE") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    elif PSS("ELE1") == "status":
                        PSS("STATUS") = ^TMP("MXMLDOM",$J,DOCHAND,PSS("child1"),"T",1)
                    PSS("child1") = $$CHILD^MXMLDOM(DOCHAND,DOCHAND1,PSS("child1"))

def MIGR():
    EN^PSSMIGRD(.PSS)

    if ERROR == 1:
        return

    XMLR()

def XMLR():
    PSS("xmlResponse") = XMLBODY(.PSS)

    FILE = PSSTITLE_".XML"
    XML2 = PSS("xmlHeader")_"<"_PSSTITLE+PSS("xmlns")
    XML2 = XML2+PSS("xmlns:xsi")_">"_"<syncResponseType>"_"<status>Success</status>"
    XML2 = XML2+XMESS+"</syncResponseType>"+XIEN
    XOBY = XML2+"</"_PSSTITLE+">"
    ^TMP($J,"NDC1","XOBY") = XOBY

Q1():
    # Clean-up
    #K ^TMP("MXMLDOM",$J),^TMP($J)

def OUT(X):
    # Error message
    FILE = PSSTITLE_".XML"
    ERROR = 1
    PSS("xmlResponse") = XMLBODY(.PSS)
    XML2 = PSS("xmlHeader")_"<syncResponse "+PSS("xmlns")
    XML2 = XML2+PSS("xmlns:xsi")+"><syncResponseType><status>Failure</status>"
    XML2 = XML2+"<message>"+X+"</message></syncResponseType></syncResponse>"
    XOBY = XML2
    ^TMP($J,"NDC1","OUT") = XOBY
    ERROR = 1
    Q1()