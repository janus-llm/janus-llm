def PSSMIGRE():
    pass

def MAN():
    X = None
    Y = None
    DIC = None
    DA = None
    DR = None
    DIE = None
    IEN = None
    NAME = None
    RTYPE = None
    IDATE = None

    if PSS["NAME"] == "":
        OUT^PSSMIGRC(" Error...Missing Required NAME")
        return

    NAME = PSS["NAME"]
    IEN = PSS["IEN"]
    RTYPE = PSS["RTYPE"]
    IDATE = PSS["IDATE"].replace("T", "").replace("-", "")
    IDATE = HL7TFM^XLFDT(IDATE)

    FNAME = "syncResponse.XML"
    FNUM = 55.95
    FNAME1 = "Manufacturer"

    if RTYPE == "ADD":
        L = L + ^PS(55.95):5
        if L:
            OUT^PSSMIGRC(" Another USER editing Manufacturer file")
            return

        ^TMP("AJF LAYGO",$J) = ^DD(55.95,.01,"LAYGO",.01,0)
        if ^TMP("AJF LAYGO",$J) != "":
            del ^DD(55.95,.01,"LAYGO",.01,0)

        X = NAME
        DIC = 55.95
        DIC(0) = "LMXZ"
        DIC(A,X,Y) = ^DIC
        DA,PSS("IEN") = +Y

        if Y < 1:
            DA = $O(^PS(55.95,"B",NAME,""))
            if not $L(DA):
                OUT^PSSMIGRC(" Error...Cannot obtain an IEN for "_NAME)
                if ^TMP("AJF LAYGO",$J) != "":
                    ^DD(55.95,.01,"LAYGO",.01,0) = ^TMP("AJF LAYGO",$J)
                L - ^PS(55.95)
                return

        PSS("IEN") = DA
        DIE = DIC
        K DIC
        DR = "2///^S X=IDATE"

        D ^DIE

        if ^TMP("AJF LAYGO",$J) != "":
            ^DD(55.95,.01,"LAYGO",.01,0) = ^TMP("AJF LAYGO",$J)
        L - ^PS(55.95)

    if ERROR == 1:
        return

    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = 55.95
        PS5 = ^PS(55.95,DA,0)
        DR = ""
        PQ = ""

        if $P(PS5,"^",1) != NAME:
            DR = ".01///^S X=NAME"
            PQ = ";"

        DR = DR_PQ_"2///"_$S(IDATE != "":"^S X=IDATE",1:"@")

        D ^DIE

    XMESS = "<message>  Updated Manufactrer: "_NAME_" </message>"
    XIEN = "<ien>"_PSS("IEN")_"</ien>"
    K DIC,DA,DR,DIE,^TMP("AJF LAYGO",$J)
    return

def PTYP():
    X = None
    Y = None
    DIC = None
    DA = None
    DR = None
    DIE = None
    IEN = None
    NAME = None
    RTYPE = None
    IDATE = None

    if PSS["NAME"] == "":
        OUT^PSSMIGRC(" Error...Missing Required NAME")
        return

    NAME = PSS["NAME"]
    IEN = PSS["IEN"]
    RTYPE = PSS["RTYPE"]
    IDATE = PSS["IDATE"].replace("T", "").replace("-", "")
    IDATE = HL7TFM^XLFDT(IDATE,"L")

    FNAME = "syncResponse.XML"
    FNUM = 50.608
    FNAME1 = "packageType"

    if RTYPE == "ADD":
        L = L + ^PS(50.608):5
        if L:
            OUT^PSSMIGRC(" Another USER editing PACKAGE TYPE file")
            return

        ^TMP("AJF LAYGO",$J) = ^DD(50.608,.01,"LAYGO",.01,0)
        if ^TMP("AJF LAYGO",$J) != "":
            del ^DD(50.608,.01,"LAYGO",.01,0)

        X = NAME
        DIC = 50.608
        DIC(0) = "LMXZ"
        DIC(A,X,Y) = ^DIC
        DA,PSS("IEN") = +Y

        if Y < 1:
            OUT^PSSMIGRC(" Error...Cannot obtain an IEN for NAME")
            if ^TMP("AJF LAYGO",$J) != "":
                ^DD(50.608,.01,"LAYGO",.01,0) = ^TMP("AJF LAYGO",$J)
            L - ^PS(50.608)
            return

        PSS("IEN") = DA
        DIE = DIC
        K DIC
        DR = "1///^S X=IDATE"

        D ^DIE

        if ^TMP("AJF LAYGO",$J) != "":
            ^DD(50.608,.01,"LAYGO",.01,0) = ^TMP("AJF LAYGO",$J)
        L - ^PS(50.608)

    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = 50.608
        PS5 = ^PS(50.608,DA,0)
        DR = ""
        PQ = ""

        if $P(PS5,"^",1) != NAME:
            DR = ".01///^S X=NAME"
            PQ = ";"

        DR = DR_PQ_"1///"_$S(IDATE != "":"^S X=IDATE",1:"@")

        D ^DIE

    XMESS = "<message>  Updated Package Type: "_NAME_" </message>"
    XIEN = "<ien>"_PSS("IEN")_"</ien>"
    K DIC,DA,DR,DIE,^TMP("AJF LAYGO",$J)
    return

def NDC():
    X = None
    Y = None
    DIC = None
    DA = None
    DR = None
    DIE = None
    IEN = None
    NAME = None
    RTYPE = None
    IDATE = None
    TNAME = None
    MNAME = None
    MIEN = None
    PNAME = None
    PIEN = None
    PSIZE = None
    PTYPE = None
    PTIEN = None
    PSOTC = None
    NIEN = None
    PSO = None
    SCK = None
    SIEN = None
    UPN = None
    VAPRO = None

    if PSS["NAME"] == "":
        OUT^PSSMIGRC(" Error...Missing Required NAME")
        return

    NAME = PSS["NAME"]
    IEN = PSS["IEN"]
    RTYPE = PSS["RTYPE"]
    IDATE = PSS["IDATE"].replace("T", "").replace("-", "")
    IDATE = HL7TFM^XLFDT(IDATE,"L")
    MNAME = PSS["MNAME"]
    MIEN = PSS["MIEN"]
    PNAME = PSS["PNAME"]
    PIEN = PSS["PIEN"]
    PSIZE = PSS["PSIZE"]
    PTYPE = PSS["PTYPE"]
    PTIEN = PSS["PTIEN"]
    PSOTC = PSS["PSOTC"]
    UPN = PSS["UPN"]
    FNAME = "syncResponse.XML"
    FNUM = 50.67
    FNAME1 = "NDC"
    NAME = NAME.replace("-", "")

    if PSIZE != "":
        SIEN = ""
        SCK = 0
        while SIEN != "":
            SIEN = $O(^PS(50.609,"B",PSIZE,SIEN))
            if SIEN != "":
                if $P(^PS(50.609,SIEN,0),"^",2) == "":
                    SCK = 1

        if SIEN == "":
            PSNUM = $P(^PS(50.609,0),"^",3)+1
            PSNUM = $P(^PS(50.609,0),"^",4)+1
            $P(^PS(50.609,0),"^",3) = PSNUM
            $P(^PS(50.609,0),"^",4) = PSNUM
            SIEN = PSNUM
            DA = SIEN
            DIE = "^PS(50.609,"
            DR = ".01///^S X=PSIZE"
            D ^DIE

    if RTYPE == "ADD":
        NIEN = $O(^PSNDF(50.67,"NDC",NAME,""))

        if NIEN == "":
            L = L + ^PSNDF(50.67):5
            if L:
                OUT^PSSMIGRC(" Another USER editing NDC file")
                return

            PSNUM = $P(^PSNDF(50.67,0),"^",3)+1
            $P(^PSNDF(50.67,0),"^",3) = PSNUM
            L - ^PSNDF(50.67,0)

            X = PSNUM
            DIC = 50.67
            DIC(0) = "LMXZ"
            DIC(A,X,Y) = ^DIC
            DA = $P(Y,"^")

        ^TMP("AJF LAYGO",$J) = ^DD(50.67,.01,"LAYGO",.01,0)
        if ^TMP("AJF LAYGO",$J) != "":
            del ^DD(50.67,.01,"LAYGO",.01,0)

        if NIEN == "":
            if DA == "":
                OUT^PSSMIGRC(" Error... Unable To Create NEW IEN")
                if ^TMP("AJF LAYGO",$J) != "":
                    ^DD(50.67,.01,"LAYGO",.01,0) = ^TMP("AJF LAYGO",$J)
                L - ^PSNDF(50.67)
                return

        if NIEN == "":
            NDF0 = ^PSNDF(50.67,DA,0)
            DR = ""
            PQ = ""

            if $P(NDF0,"^",2) != NAME:
                DR = "1///^S X=NAME"
                PQ = ";"

            DR = DR_PQ_"2///"_$S(UPN != "":"^S X=UPN",1:"@")
            DR = DR_PQ_"3///^S X=MIEN"
            DR = DR_PQ_"4///"_$S(TNAME != "":"^S X=TNAME",1:"@")
            DR = DR_PQ_"5///^S X=PIEN"
            DR = DR_PQ_"7///"_$S(IDATE != "":"^S X=IDATE",1:"@")
            DR = DR_PQ_"8///"_$S(SIEN != "":"^S X=SIEN",1:"@")
            DR = DR_PQ_"9///"_$S(PTIEN != "":"^S X=PTIEN",1:"@")
            DR = DR_PQ_"10///"_$S(PSOTC != "":"^S X=PSOTC",1:"@")

            D ^DIE

        NIEN2 = NIEN
        while NIEN2 != "":
            DA = NIEN2
            DIE = 50.67
            IDATE = DT
            DR = ""
            DR = DR_"7///^S X=IDATE"
            NDF0 = ^PSNDF(50.67,DA,0)

            if $P(NDF0,"^",2) != NAME:
                DR = DR_";1///^S X=NAME"

            DR = DR_";2///"_$S(UPN != "":"^S X=UPN",1:"@")
            DR = DR_";3///^S X=MIEN"
            DR = DR_";4///"_$S(TNAME != "":"^S X=TNAME",1:"@")
            DR = DR_";5///^S X=PIEN"
            DR = DR_";8///"_$S(SIEN != "":"^S X=SIEN",1:"@")
            DR = DR_";9///"_$S(PTIEN != "":"^S X=PTIEN",1:"@")
            DR = DR_";10///"_$S(PSOTC != "":"^S X=PSOTC",1:"@")

            D ^DIE
            NIEN2 = $O(^PSNDF(50.67,"NDC",NAME,NIEN2))

        if ^TMP("AJF LAYGO",$J) != "":
            ^DD(50.67,.01,"LAYGO",.01,0) = ^TMP("AJF LAYGO",$J)
        L - ^PSNDF(50.67)

    if ERROR == 1:
        return

    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = 50.67
        NDF0 = ^PSNDF(50.67,DA,0)
        DR = ""
        PQ = ""

        if $P(NDF0,"^",2) != NAME:
            DR = "1///^S X=NAME"
            PQ = ";"

        DR = DR_PQ_"2///"_$S(UPN != "":"^S X=UPN",1:"@")
        DR = DR_PQ_"3///^S X=MIEN"
        DR = DR_PQ_"4///"_$S(TNAME != "":"^S X=TNAME",1:"@")
        DR = DR_PQ_"5///^S X=PIEN"
        DR = DR_PQ_"7///"_$S(IDATE != "":"^S X=IDATE",1:"@")
        DR = DR_PQ_"8///"_$S(SIEN != "":"^S X=SIEN",1:"@")
        DR = DR_PQ_"9///"_$S(PTIEN != "":"^S X=PTIEN",1:"@")
        DR = DR_PQ_"10///"_$S(PSOTC != "":"^S X=PSOTC",1:"@")

        D ^DIE

    XMESS = "<message>  Updated NDC: "_NAME_" </message>"
    XIEN = "<ien>"_PSS("IEN")_"</ien>"
    K DIC,DA,DR,DIE,^TMP("AJF LAYGO",$J)
    return

def VAGN():
    X = None
    Y = None
    DIC = None
    DA = None
    DR = None
    DIE = None
    IEN = None
    NAME = None
    RTYPE = None
    IDATE = None
    MVUID = None
    VUID = None
    EFFDT = None
    STATUS = None
    CMVUID = None

    NAME = PSS["NAME"]
    IEN = PSS["IEN"]
    RTYPE = PSS["RTYPE"]
    IDATE = PSS["INACTDATE"].replace("T", "").replace("-", "")
    IDATE = HL7TFM^XLFDT(IDATE,"L")
    MVUID = PSS["MASTERVUID"]
    VUID = PSS["VUID"]
    EFFDT = PSS["EFFDATE"]
    STATUS = PSS["STATUS"]
    FNUM = 50.6
    FNAME = "syncResponse.XML"
    FNAME1 = "vaGenericName"

    if NAME == "":
        OUT^PSSMIGRC(" Error...Missing Required NAME")
        return

    if MVUID == "":
        OUT^PSSMIGRC(" Error...Missing Required MASTER VUID")
        return

    if VUID == "":
        OUT^PSSMIGRC(" Error...Missing Required VUID")
        return

    if EFFDT == "":
        OUT^PSSMIGRC(" Error...Missing Required EFFECTIVE DATE")
        return

    if STATUS == "":
        OUT^PSSMIGRC(" Error...Missing Required STATUS")
        return

    EFFDT = DATE^PSSMIGRD(PSS["EFFDATE"])

    if RTYPE == "ADD":
        L = L + ^PSNDF(50.6):5
        if L:
            OUT^PSSMIGRC(" Another USER editing VA Generic Name file")
            return

        ^TMP("AJF LAYGO",$J) = ^DD(50.6,.01,"LAYGO",.01,0)
        if ^TMP("AJF LAYGO",$J) != "":
            del ^DD(50.6,.01,"LAYGO",.01,0)

        X = NAME
        DIC = 50.6
        DIC(0) = "LMXZ"
        DIC(A,X,Y) = ^DIC
        DA = $P(Y,"^")

        DIE = DIC
        DR = "1///^S X=IDATE;99.98///^S X=MVUID;99.99///^S X=VUID"

        D ^DIE

        DIC = "^PSNDF(50.6,"_DA_",""TERMSTATUS"","
        DIC(0) = "L"
        DIC("P") = "50.6009DA"
        DA(1) = DA
        DA = 1
        X = EFFDT

        FILE^DICN

        DIE = DIC
        DR = ".02///^S X=STATUS"

        D ^DIE

        if IDATE != "":
            X = NAME
            DIC = 5000.3
            DIC(0) = "LMXZ"

            D ^DIC

            VAPRO = ""
            while VAPRO != "":
                X = VAPRO
                DIC = 5000.2
                DIC(0) = "LMXZ"

                D ^DIC

    if RTYPE == "MODIFY":
        DA = PSS["IEN"]
        DIE = 50.6
        PS5 = ^PSNDF(50.6,DA,0)
        PSMV = ^PSNDF(50.6,DA,"VUID")
        DR = ""
        PQ = ""

        if $P(PS5,"^",2) != IDATE:
            DR = "1///^S X=IDATE"
            PQ = ";"

        if $P(PSMV,"^",2) != MVUID:
            DR = DR_PQ_"99.98///^S X=MVUID"
            PQ = ";"

        if $P(PSMV,"^",1) != VUID:
            DR = DR_PQ_"99.99///^S X=VUID"

        D ^DIE

    XMESS = "<message>  Updated VA Generic: "_NAME_" </message>"
    XIEN = "<ien>"_PSS["IEN"]_"</ien>"
    K DIC,DA,DR,DIE,^TMP("AJF LAYGO",$J)
    return