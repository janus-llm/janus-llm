def PSSMIGR1(FL, IEN, RCNT, TYPE):
    FNAME = "drugMigrationResponse.XML"
    if FL == "" or IEN == "" or RCNT == "" or TYPE == "":
        OUT(" Error... Missing required data")
        return
    XST, CNT = 0, 0
    if IEN != 0:
        IEN = IEN - 1
    if FL == 50.607:
        DUNI()
        return
    if FL == 50.416:
        DING()
        return
    if FL == 50.6:
        VAGN()
        return
    if FL == 50.64:
        VADU()
        return
    if FL == 50.605:
        VADC()
        return
    if FL == 50.606:
        DSFO(IEN, RCNT, TYPE)
        return
    if FL == 50.68:
        VAPD(IEN, RCNT, TYPE)
        return
    OUT(" Error... Invalid File Number")


def DUNI():
    IND, NAME, PS0, XIEN, XTYPE, XIND = "", "", "", "", "", ""
    TMP_607 = {}
    CNT = 0
    TMP_607["EOF"] = 0
    FNAME = "drugMigrationResponse_DrugUnits.XML"
    FNUM = 50.607
    FNAME1 = "drugUnits"
    if IEN < 0:
        OUT(" Error... Invalid IEN")
        return
    if RCNT < 1:
        OUT(" Error... Invalid Number of Elements")
        return
    if TYPE > 1 or TYPE < 0:
        OUT(" Error... Invalid TYPE")
        return
    while True:
        IEN = $ORDER(^PS(50.607, IEN))
        if IEN == "B":
            TMP_607["EOF"] = 1
            XST = 1
            break
        if RCNT == CNT:
            XST = 1
            break
        PS0 = ^PS(50.607, IEN, 0)
        NAME = $PIECE(PS0, "^")
        IND = $PIECE(PS0, "^", 2)
        XTYPE = 0 if +IND else 1
        if +IND:
            IND = $$FMTHL7^XLFDT(IND)
        XIEN = "<drugUnitsIen>" + IEN + "</drugUnitsIen>"
        XNAME = "<name>" + NAME + "</name>" if NAME != "" else ""
        XIND = "<inactivationDate>" + IND + "</inactivationDate>" if IND != "" else ""
        TMP_607[XTYPE][IEN] = XIEN + XNAME + XIND
        if XTYPE == TYPE:
            CNT += 1


def VADU():
    CNT, IND, NAME, PS0, XIEN, XTYPE, XIND = 0, "", "", "", "", "", ""
    TMP_64 = {}
    TMP_64["EOF"] = 0
    FNAME = "drugMigrationResponse_vaDispenseUnits.XML"
    FNUM = 50.64
    FNAME1 = "vaDispenseUnit"
    if IEN < 0:
        OUT(" Error... Invalid IEN")
        return
    if RCNT < 1:
        OUT(" Error... Invalid Starting Record Number")
        return
    if TYPE > 1 or TYPE < 0:
        OUT(" Error... Invalid TYPE")
        return
    while True:
        IEN = $ORDER(^PSNDF(50.64, IEN))
        if IEN == "B":
            TMP_64["EOF"] = 1
            XST = 1
            break
        if RCNT == CNT:
            XST = 1
            break
        PS0 = ^PSNDF(50.64, IEN, 0)
        NAME = $PIECE(PS0, "^")
        IND = $PIECE(PS0, "^", 2)
        XTYPE = 0 if +IND else 1
        if +IND:
            IND = $$FMTHL7^XLFDT(IND)
        XIEN = "<dispenseUnitsIen>" + IEN + "</dispenseUnitsIen>"
        XNAME = "<name>" + NAME + "</name>" if NAME != "" else ""
        XIND = "<inactivationDate>" + IND + "</inactivationDate>" if IND != "" else ""
        TMP_64[XTYPE][IEN] = XIEN + XNAME + XIND
        if XTYPE == TYPE:
            CNT += 1


def DING():
    CNT, IND, MAEN, MIEN, NAME, PRIN, PS0, PST0, PSV, STA, VUID, XEDT, XIEN, XPRIN, XSTA, XTYPE, XIND, XMAEN, XVUID = 0, "", "", "", "", "", "", "", "", "", "", "", "", "", ""
    TMP_416 = {}
    TMP_416["EOF"] = 0
    FNAME = "drugMigrationResponse_DrugIngredients.XML"
    FNUM = 50.416
    FNAME1 = "drugIngredients"
    if IEN < 0:
        OUT(" Error... Invalid IEN")
        return
    if RCNT < 1:
        OUT(" Error... Invalid Starting Record Number")
        return
    if TYPE > 1 or TYPE < 0:
        OUT(" Error... Invalid TYPE")
        return
    while True:
        IEN = $ORDER(^PS(50.416, IEN))
        if +IEN == 0:
            TMP_416["EOF"] = 1
            XST = 1
            break
        if RCNT == CNT:
            XST = 1
            break
        PS0 = ^PS(50.416, IEN, 0)
        NAME = $PIECE(PS0, "^")
        PRIN = $PIECE(PS0, "^", 2)
        IND = $PIECE(^PS(50.416, IEN, 2), "^")
        if +PRIN:
            PRIN = $PIECE(^PS(50.416, PRIN, 0), "^")
        XTYPE = 0 if +IND else 1
        if +IND:
            IND = $$FMTHL7^XLFDT(IND)
        PSV = ^PS(50.416, IEN, "VUID")
        MAEN = $PIECE(PSV, "^", 2)
        VUID = $PIECE(PSV, "^")
        XIEN = "<drugIngredientsIen>" + IEN + "</drugIngredientsIen>"
        XNAME = "<name><![CDATA[" + NAME + "]]></name>" if NAME != "" else ""
        XPRIN = "<primaryIngredient><![CDATA[" + PRIN + "]]></primaryIngredient>" if PRIN != "" else ""
        XIND = "<inactivationDate>" + IND + "</inactivationDate>" if IND != "" else ""
        XMAEN = "<masterEntryForVuid>" + MAEN + "</masterEntryForVuid>"
        XVUID = "<vuid>" + VUID + "</vuid>"
        TMP_416[XTYPE][IEN] = XIEN + XNAME + XPRIN + XIND + XMAEN + XVUID
        if $DATA(^PS(50.416, IEN, "TERMSTATUS", 0)):
            MIEN = 0
            while True:
                MIEN = $ORDER(^PS(50.416, IEN, "TERMSTATUS", MIEN))
                if MIEN == "B":
                    break
                PST0 = ^PS(50.416, IEN, "TERMSTATUS", MIEN, 0)
                EDT = $PIECE(PST0, "^")
                STA = $PIECE(PST0, "^", 2)
                EDT = $$FMTHL7^XLFDT(EDT)
                XEDT = "<effectiveDateTime>" + EDT + "</effectiveDateTime>"
                XSTA = "<status>" + STA + "</status>"
                TMP_416[XTYPE][IEN, MIEN] = "<effectiveDateTime>" + XEDT + XSTA + "</effectiveDateTime>"
        if XTYPE == TYPE:
            CNT += 1


def VAGN():
    CNT, XST, PSV, XVUID, MAEN, XMAEN, XIND, XNAME, IND, MIEN, NAME, PS0, PST0, STA, VUID, XEDT, XIEN, XSTA, XTYPE = 0, 0, "", "", "", "", "", "", "", "", "", "", "", ""
    TMP_6 = {}
    TMP_6["EOF"] = 0
    FNAME = "drugMigrationResponse_VAGeneric.XML"
    FNUM = 50.6
    FNAME1 = "vaGenericName"
    if IEN < 0:
        OUT(" Error... Invalid IEN")
        return
    if RCNT < 1:
        OUT(" Error... Invalid Starting Record Number")
        return
    if TYPE > 1 or TYPE < 0:
        OUT(" Error... Invalid TYPE")
        return
    while True:
        IEN = $ORDER(^PSNDF(50.6, IEN))
        if +IEN == 0:
            TMP_6["EOF"] = 1
            XST = 1
            break
        if RCNT == CNT:
            XST = 1
            break
        PS0 = ^PSNDF(50.6, IEN, 0)
        NAME = $PIECE(PS0, "^")
        IND = $PIECE(PS0, "^", 2)
        XTYPE = 0 if +IND else 1
        if +IND:
            IND = $$FMTHL7^XLFDT(IND)
        PSV = ^PSNDF(50.6, IEN, "VUID")
        MAEN = $PIECE(PSV, "^", 2)
        VUID = $PIECE(PSV, "^")
        XIEN = "<vaGenericIen>" + IEN + "</vaGenericIen>"
        XNAME = "<name><![CDATA[" + NAME + "]]></name>" if NAME != "" else ""
        XIND = "<inactivationDate>" + IND + "</inactivationDate>" if IND != "" else ""
        XMAEN = "<masterEntryForVuid>" + MAEN + "</masterEntryForVuid>"
        XVUID = "<vuid>" + VUID + "</vuid>"
        TMP_6[XTYPE][IEN] = XIEN + XNAME + XIND + XMAEN + XVUID
        if $DATA(^PSNDF(50.6, IEN, "TERMSTATUS", 0)):
            MIEN = 0
            while True:
                MIEN = $ORDER(^PSNDF(50.6, IEN, "TERMSTATUS", MIEN))
                if MIEN == "B":
                    break
                PST0 = ^PSNDF(50.6, IEN, "TERMSTATUS", MIEN, 0)
                EDT = $PIECE(PST0, "^")
                STA = $PIECE(PST0, "^", 2)
                EDT = $$FMTHL7^XLFDT(EDT)
                XEDT = "<effectiveDateTime>" + EDT + "</effectiveDateTime>"
                XSTA = "<status>" + STA + "</status>"
                TMP_6[XTYPE][IEN, MIEN] = "<effectiveDateTime>" + XEDT + XSTA + "</effectiveDateTime>"
        if XTYPE == TYPE:
            CNT += 1


def VADC():
    CNT, CODE, CODE1, CLASS, CLASS1, EDT, MAEN, MIEN, PCLS, PS0, PS01, PS10, PST0, PSV, STA, TYP, VUID, XCLASS, XCLASS1, XCODE, XCODE1, XEDT, XIEN, XIEN1, XIEN1, XIEN1, XMIEN, XPCLS, XSTA, XTMP, XTYP, XMAEN, XVUID = 0, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
    TMP_605 = {}
    TMP_605["EOF"] = 0
    FNAME = "drugMigrationResponse_DrugClass.XML"
    FNUM = 50.605
    FNAME1 = "vaDrugClass"
    if IEN < 0:
        OUT(" Error... Invalid IEN")
        return
    if RCNT < 1:
        OUT(" Error... Invalid Starting Record Number")
        return
    if TYPE > 3 or TYPE < 0:
        OUT(" Error... Invalid TYPE")
        return
    while True:
        IEN = $ORDER(^PS(50.605, IEN))
        if +IEN == 0:
            TMP_605["EOF"] = 1
            XST = 1
            break
        if RCNT == CNT:
            XST = 1
            break
        PS0 = ^PS(50.605, IEN, 0)
        CODE = $PIECE(PS0, "^")
        CLASS = $PIECE(PS0, "^", 2)
        PCLS = $PIECE(PS0, "^", 3)
        TYP = $PIECE(PS0, "^", 4)
        if TYP == "":
            TYP = 3
        PSV = ^PS(50.605, IEN, "VUID")
        MAEN = $PIECE(PSV, "^", 2)
        VUID = $PIECE(PSV, "^")
        XTMP = ""
        if +PCLS, $DATA(^PS(50.605, PCLS, 0)):
            PS01 = ^PS(50.605, PCLS, 0)
            CODE1 = $PIECE(PS01, "^")
            CLASS1 = $PIECE(PS01, "^", 2)
            XIEN1 = "<vaDrugClassIen>" + PCLS + "</vaDrugClassIen>"
            XCODE1 = "<code>" + CODE1 + "</code>" if CODE1 != "" else ""
            XCLASS1 = "<classification>" + CLASS1 + "</classification>" if CLASS1 != "" else ""
            XTMP = XIEN1 + XCODE1 + XCLASS1
        XIEN = "<vaDrugClassIen>" + IEN + "</vaDrugClassIen>"
        XCODE = "<code>" + CODE + "</code>" if CODE != "" else ""
        XCLASS = "<classification>" + CLASS + "</classification>" if CLASS != "" else ""
        XPCLS = "<parentClass>" + XTMP + "</parentClass>" if PCLS != "" else ""
        XTYP = "<type>" + TYP + "</type>" if TYP != "" else ""
        XMAEN = "<masterEntryForVuid>" + MAEN + "</masterEntryForVuid>"
        XVUID = "<vuid>" + VUID + "</vuid>"
        TMP_605[TYP][IEN] = XIEN + XCODE + XCLASS + XPCLS + XTYP + XMAEN + XVUID
        if $DATA(^PS(50.605, IEN, "TERMSTATUS", 0)):
            MIEN = 0
            while True:
                MIEN = $ORDER(^PS(50.605, IEN, "TERMSTATUS", MIEN))
                if MIEN == "B":
                    break
                PST0 = ^PS(50.605, IEN, "TERMSTATUS", MIEN, 0)
                EDT = $PIECE(PST0, "^")
                STA = $PIECE(PST0, "^", 2)
                EDT = $$FMTHL7^XLFDT(EDT)
                XEDT = "<effectiveDateTime>" + EDT + "</effectiveDateTime>"
                XSTA = "<status>" + STA + "</status>"
                TMP_605[TYP][IEN, MIEN] = "<effectiveDateTime>" + XEDT + XSTA + "</effectiveDateTime>"
        if $DATA(^PS(50.605, IEN, 1, 0)):
            MIEN = 0
            while True:
                MIEN = $ORDER(^PS(50.605, IEN, 1, MIEN))
                if MIEN == "":
                    break
                PS10 = ^PS(50.605, IEN, 1, MIEN, 0)
                XMIEN = "4" + MIEN
                TMP_605[TYP][IEN, XMIEN] = "<description>" + PS10 + "</description>"
        if TYP == TYPE:
            CNT += 1